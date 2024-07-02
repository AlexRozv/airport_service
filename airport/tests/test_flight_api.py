import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Route, Airport, Airplane, AirplaneType, Crew, Flight
from airport.serializers import FlightListSerializer, FlightDetailSerializer

FLIGHT_URL = reverse("airport:flight-list")


def sample_airport(**params):
    defaults = {
        "name": "Test airport",
        "closest_big_city": "Test city"
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    airport_from = sample_airport()
    airport_to = sample_airport(name="Airport 2", closest_big_city="City 2")
    defaults = {
        "source": airport_from,
        "destination": airport_to,
        "distance": 1000,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = Airplane.objects.create(
        name="test airplane",
        rows=30,
        seats_in_row=8,
        airplane_type=AirplaneType.objects.create(name="test airplane type"),
    )
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2024-01-01T12:30:00Z",
        "arrival_time": "2024-01-02T14:00:00Z",
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        sample_flight()
        sample_flight()

        res = self.client.get(FLIGHT_URL)

        flights = Flight.objects.order_by("id")
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_flights_by_route(self):
        route1 = sample_route(source=sample_airport(name="airport 1"))
        route2 = sample_route(source=sample_airport(name="airport 2"))
        flight1 = sample_flight(route=route1)
        flight2 = sample_flight(route=route2)

        res = self.client.get(
            FLIGHT_URL, {"route": f"{route1.id}"}
        )

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filter_flights_by_date(self):
        flight1 = sample_flight(departure_time="2024-11-11T11:11:00Z", arrival_time="2024-12-12T12:12:00Z")
        flight2 = sample_flight(departure_time="2024-05-05T05:05:00Z", arrival_time="2024-06-06T06:06:00Z")
        flight3 = sample_flight(departure_time="2024-02-02T02:02:00Z", arrival_time="2024-03-03T03:03:00Z")

        res1 = self.client.get(
            FLIGHT_URL, {"departure_date": "2024-11-11"}
        )
        res2 = self.client.get(
            FLIGHT_URL, {"arrival_date": "2024-06-06"}
        )

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertIn(serializer1.data, res1.data)
        self.assertIn(serializer2.data, res2.data)
        self.assertNotIn(serializer3.data, res2.data)

    def test_retrieve_flight_detail(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        res = self.client.get(url)

        serializer = FlightDetailSerializer(flight)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_forbidden(self):
        route = sample_route()
        airplane = Airplane.objects.create(
            name="test airplane",
            rows=30,
            seats_in_row=8,
            airplane_type=AirplaneType.objects.create(name="test airplane type"),
        )
        payload = {
            "route": route,
            "airplane": airplane,
            "departure_time": "2024-01-01T12:30:00Z",
            "arrival_time": "2024-01-02T14:00:00Z",
        }
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self):
        route = sample_route()
        airplane = Airplane.objects.create(
            name="test airplane",
            rows=30,
            seats_in_row=8,
            airplane_type=AirplaneType.objects.create(name="test airplane type"),
        )
        crew = Crew.objects.create(first_name="test first", last_name="test last")
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2024-01-01T12:30:00Z",
            "arrival_time": "2024-01-02T14:00:00Z",
            "crew_members": [crew.id]
        }
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        flight = Flight.objects.get(id=res.data["id"])
        self.assertEqual(route, flight.route)
        self.assertEqual(airplane, flight.airplane)
        self.assertIn(crew, flight.crew_members.all())
