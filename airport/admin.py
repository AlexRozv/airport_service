from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Flight,
    Order,
    Ticket,
)

admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(get_user_model(), UserAdmin)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    ordering = ("name",)
    search_fields = ("name", "closest_big_city")


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    ordering = ("name",)
    search_fields = ("name",)
    list_filter = ("airplane_type",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    ordering = ("source__name", "destination__name")
    search_fields = ("source__name", "destination__name")
    list_filter = ("source", "destination")


@admin.register(Crew)
class RouteAdmin(admin.ModelAdmin):
    ordering = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
