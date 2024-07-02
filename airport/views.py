from datetime import datetime

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    FlightSerializer,
    OrderSerializer,
    TicketSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    OrderListSerializer
)


class AirportViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return self.serializer_class


class CrewViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return self.serializer_class


class FlightViewSet(
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    viewsets.GenericViewSet
):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        route_id_str = self.request.query_params.get("route")
        departure_date = self.request.query_params.get("departure_date")
        arrival_date = self.request.query_params.get("arrival_date")

        queryset = self.queryset

        if route_id_str:
            queryset = queryset.filter(route_id=int(route_id_str))
        if departure_date:
            departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=departure_date)
        if arrival_date:
            arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date=arrival_date)

        return queryset


class TicketViewSet(
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    viewsets.GenericViewSet
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return self.serializer_class


class OrderViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
