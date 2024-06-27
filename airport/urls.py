from django.urls import path, include
from rest_framework import routers

from airport.views import AirportViewSet, RouteViewSet, CrewViewSet

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crew", CrewViewSet)

urlpatterns = [
    path("", include(router.urls))
]
