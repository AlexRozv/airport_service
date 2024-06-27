from django.urls import path, include
from rest_framework import routers

from airport.views import AirportViewSet, RouteViewSet, CrewViewSet, AirplaneTypeViewSet, AirplaneViewSet

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crew", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls))
]
