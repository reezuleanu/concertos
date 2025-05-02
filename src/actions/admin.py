from django.contrib import admin
from .models import Device, CustomVariable

# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "event_id", "type", "address", "port"]


class CustomVariableAdmin(admin.ModelAdmin):
    list_display = ["event_id", "user_id", "name", "value"]


admin.site.register(Device, DeviceAdmin)
admin.site.register(CustomVariable, CustomVariableAdmin)
