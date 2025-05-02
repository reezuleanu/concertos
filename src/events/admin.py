from django.contrib import admin
from .models import Event

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "owner_id", "country", "city"]


admin.site.register(Event, EventAdmin)
