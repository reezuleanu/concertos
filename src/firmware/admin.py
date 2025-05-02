from django.contrib import admin
from .models import Firmware


# Register your models here.
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ["name", "version"]


admin.site.register(Firmware, FirmwareAdmin)
