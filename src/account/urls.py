from django.urls import path
from . import views


urlpatterns = [
    path("", views.hello, name="index"),
    path("<str:dedication>/", views.hello_dedication, name="dedication"),
]
