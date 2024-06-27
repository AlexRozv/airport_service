from django.urls import path, include
from rest_framework import routers

from airport.views import AirportViewSet

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)

urlpatterns = [
    path("", include(router.urls))
]
