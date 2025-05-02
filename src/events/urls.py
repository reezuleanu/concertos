from django.urls import path, include
from . import views

# events app urls
urlpatterns = [
    path("countries/", views.get_countries, name="get_countries"),
    path("cities/<int:country>", views.get_cities, name="get_cities"),
    path(
        "<str:eventid>/devices/hardware",
        views.get_hardware_devices,
        name="get_hardware_devices",
    ),
    path(
        "<str:eventid>/devices/hardware/expanded",
        views.get_hardware_devices_expanded,
        name="get_hardware_devices_expanded",
    ),
    path(
        "<str:eventid>/devices/software",
        views.get_software_devices,
        name="get_software_devices",
    ),
    path("<str:eventid>/devices/<int:deviceid>/", views.get_device, name="get_device"),
    path("<str:eventid>/actions/", include("actions.urls")),
    path("<int:eventid>/", views.get_event, name="get_event"),
]
