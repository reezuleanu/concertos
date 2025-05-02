from .models import Device, CustomVariable
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class CustomVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomVariable
        fields = "__all__"
