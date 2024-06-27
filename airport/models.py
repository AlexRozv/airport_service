from django.contrib.auth import get_user_model
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=63)
    closest_big_city = models.CharField(max_length=63)


class Route(models.Model):
    source = models.ForeignKey(
        to=Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    destination = models.ForeignKey(
        to=Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    distance = models.IntegerField()


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)


class AirplaneType(models.Model):
    name = models.CharField(max_length=63)


class Airplane(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        to=AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )


class Flight(models.Model):
    route = models.ForeignKey(
        to=Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        to=Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew_members = models.ManyToManyField(to=Crew, related_name="flights")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders"
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        to=Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
