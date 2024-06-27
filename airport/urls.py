from django.urls import path, include
from rest_framework import routers

from airport.views import AirportViewSet, RouteViewSet

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [
    path("", include(router.urls))
]
