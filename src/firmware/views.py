from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Firmware
from .serializers import FirmwareSerializer
from django.http import FileResponse


# Create your views here.
@api_view(["GET"])
def get_all_firmwares(request) -> Response:
    return Response([firmware.id for firmware in Firmware.objects.all()])


@api_view(["GET"])
def get_firmware(request, firmware_id: int) -> Response:
    try:
        firmware = Firmware.objects.get(id=firmware_id)
    except Firmware.DoesNotExist:
        return Response("Firmware not found", 404)
    return Response(FirmwareSerializer(firmware).data)


@api_view(["GET"])
def download_firmware(request, firmware_id: int) -> Response:
    try:
        path = Firmware.objects.get(id=firmware_id).path
    except Firmware.DoesNotExist:
        return Response("Firmware not found", 404)

    fp = open(path, "rb")
    return FileResponse(fp, as_attachment=True)
