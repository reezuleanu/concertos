from django.urls import path, include
from . import views

# events app urls
urlpatterns = [
    path("", views.get_all_firmwares, name="get_all_firmwares"),
    path("<int:firmware_id>/", views.get_firmware, name="get_firmware"),
    path(
        "<int:firmware_id>/download", views.download_firmware, name="download_firmware"
    ),
]
