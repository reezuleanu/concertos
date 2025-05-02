from rest_framework.response import Response
from rest_framework.decorators import api_view
from actions.models import Device
from .models import Event
from .serializers import EventSerializer
from actions.serializers import DeviceSerializer
from cities_light.models import Country, City


# Create your views here.
@api_view(["GET"])
def get_countries(request) -> Response:
    """Get list of countries and their id

    Args:
        request (Request): http request

    Returns:
        Response: country.name:country.id pair
    """
    countries = {country.name: country.id for country in Country.objects.all()}
    return Response(countries)


@api_view(["GET"])
def get_cities(request, country: int) -> Response:
    """Get list of cities and their id for a respective country

    Args:
        request (Request): http request
        country (int): country id

    Returns:
        Response: city.name:city.id pair
    """
    cities = {city.name: city.id for city in City.objects.filter(country=country)}
    return Response(cities)


@api_view(["GET", "POST"])
def get_hardware_devices(request, eventid: int) -> Response:
    """Return a list of all devices for the event

    Args:
        request (any): http request
        eventid (str): event id

    Returns:
        Response: dictionary of device name : device id
    """

    # get names of devices registered for the event
    match request.method:
        case "GET":
            try:
                devices = {
                    device.name: device.id
                    for device in Device.objects.filter(event_id=eventid)
                }
            except Device.DoesNotExist:
                return Response("No devices associated with this event", 404)

            return Response(devices)

        case "POST":
            device_data = request.data
            device_data["event_id"] = eventid
            device = DeviceSerializer(data=device_data)
            if not device.is_valid():
                return Response("Invalid device data", 400)

            device.save()
            # return Response(DeviceSerializer(device).data)
            return Response(device_data)


@api_view(["GET"])
def get_hardware_devices_expanded(request, eventid: int) -> Response:
    """Return a list of device ids and their respective data

    Args:
        request (Request): http request
        eventid (int): id of the event

    Returns:
        Response: list of dicts {device.id: {device.name, device.address, device.port}}
    """

    devices = {
        device.id: {
            "name": device.name,
            "type": device.type,
            "address": device.address,
            "port": device.port,
        }
        for device in Device.objects.filter(event_id=eventid)
    }

    return Response(devices)


# ! Only returns the database
@api_view(["GET"])
def get_software_devices(request, eventid: int) -> Response:
    """Return all software devices for the event

    Args:
        request (Request): http request
        eventid (int): id of the event (UNUSED)

    Returns:
        Response: device_name:device_id pair
    """

    devices = {"Database": 0}

    return Response(devices)


@api_view(["GET", "PUT", "DELETE"])
def get_device(request, eventid: str, deviceid: str) -> Response:
    """Return all device data

    Args:
        request (any): http request
        eventid (str): id of the event
        deviceid (str): id of the device in the event

    Returns:
        Response: device data
    """
    try:
        device = Device.objects.get(event_id=eventid, id=deviceid)
    except Device.DoesNotExist:
        return Response("Device not found", 404)

    match request.method:
        case "GET":

            device = DeviceSerializer(device).data
            return Response(device)

        case "PUT":

            new_data = request.data
            try:
                device.name = new_data["name"]
                device.type = new_data["type"]
                device.address = new_data["address"]
                device.port = new_data["port"]
            except KeyError:
                return Response("Invalid device data", 400)

            device.save()
            return Response(DeviceSerializer(device).data)

        case "DELETE":
            device.delete()
            return Response(f"Device {id} deleted successfully")


@api_view(["GET"])
def get_event(request, eventid: int) -> Response:

    # get action data
    try:
        event = Event.objects.get(id=eventid)
    except Event.DoesNotExist:
        return Response(404)

    return Response(EventSerializer(event).data)
