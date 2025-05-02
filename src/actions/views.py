from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
import threading
from libactions.action import ActionFactory
from libactions.observer import Observer
from libactions.firework_launcher import funcs as firework_launcher_funcs
from libactions.lights import funcs as lights_funcs
from libactions.software import funcs as database_funcs
from libactions.rgb_lights import funcs as rgb_lights_funcs
from libactions.trigger import CaptainTrigger
import actions.models as DB
from actions.serializers import DeviceSerializer, CustomVariableSerializer

# initialize observer
observer = Observer("observer_actions/")

functions = {
    "fireworks_launcher": firework_launcher_funcs,
    "lights": lights_funcs,
    "rgb_lights": rgb_lights_funcs,
    "database": database_funcs,
}

# initialize Action Factory
action_factory = ActionFactory(
    0, DB.Device, DB.CustomVariable, DeviceSerializer, functions
)

t1 = threading.Thread(target=observer.datetime_thread, args=(1,), daemon=True)
t1.start()


@api_view(["GET"])
def download_test(request) -> FileResponse:

    file = open("actions/image.png", "rb")
    return FileResponse(file, as_attachment=True, filename="image.png")


@api_view(["POST", "GET"])
def post_action(request, eventid: int) -> Response:
    """Post new action with POST, or get all action names with GET

    Args:
        request (any): http request
        eventid (int): the id of the event

    Returns:
        Response: operation result
    """
    match request.method:
        case "POST":
            action_data = request.data["triggers"]
            action_name = request.data["action_name"]
            # print(action_data[0])
            if observer.get_action(eventid, action_name) is not None:
                if len(observer.get_all_actions(eventid)) >= 50:
                    return Response(
                        f"You reached the Actions limit for Event {eventid}"
                    )
            action_factory.eventid = eventid
            action = action_factory.parse(action_data, action_name)
            # print([command.name for command in action.commands])
            # print(action_factory.deparse(action))
            observer.add_action(eventid, action)
            observer.serialize_actions(eventid)

            return Response(f"Action added to {eventid} successfully", 200)

        case "GET":
            try:
                data = {
                    action.name: action.name
                    for action in observer.get_all_actions(eventid)
                }
            # except TypeError:
            #     return Response({})
            except (KeyError, TypeError):
                return Response("Event does not exist or has no actions set up", 404)

            return Response(data)


@api_view(["GET", "PUT", "DELETE"])
def get_action(request, eventid: int, action_name: str) -> Response:
    """Execute operations upon specific action

    Args:
        request (Request): http request
        eventid (int): id of the event
        action_name (str): name of the action

    Returns:
        Response: operation result
    """
    try:
        action = observer.get_action(eventid, action_name)
    except KeyError:
        return Response("Event does not have actions set up", 404)

    if action is None:
        return Response(f"Action not found within event {eventid}", 404)

    match request.method:
        # get action data with GET
        case "GET":

            data = action_factory.deparse(action)
            # print(data)

            return Response(data)

        # update action name with PUT
        case "PUT":
            try:
                new_name = request.data["new_name"]
            except KeyError:
                return Response("No name provided in request body", 400)

            observer.edit_action(eventid, action.name, new_name)
            observer.serialize_actions(eventid)

            return Response("Action edited successfully")

        # delete action from observer with DELETE
        case "DELETE":
            observer.delete_action(eventid, action_name)
            observer.serialize_actions(eventid)

            return Response("Action deleted successfully")


@api_view(["GET"])
def get_all_global_variables(request, eventid: int) -> Response:
    """FRONTEND ENDPOINT

    Get custom variable names for a specific id

    Args:
        request (Request): http request
        eventid (int): id of the event

    Returns:
        Response: dict containing name:name pairs (it's
        for the front end)
    """

    # fetch variables for that event
    variables = {
        variable.name: variable.name
        for variable in DB.CustomVariable.objects.filter(event_id=eventid)
    }

    return Response(variables)


@api_view(["GET"])
def get_all_personal_variables(request, eventid: int) -> Response:

    variables = {
        variable.name: variable.name
        for variable in DB.CustomVariable.objects.filter(event_id=eventid, user_id=0)
    }

    return Response(variables)


@api_view(["GET", "PUT", "DELETE"])
def global_variable(request, eventid: int, variable_name: str) -> Response:
    """Get, update, or delete a global custom variable value for an event

    Args:
        request (Request): http request
        eventid (int): id of the event
        variable_name (str): name of the variable

    Returns:
        Response: request response
    """
    try:
        variable = DB.CustomVariable.objects.get(event_id=eventid, name=variable_name)
        # print("variable found ", variable_name)
    except DB.CustomVariable.DoesNotExist:
        return Response("Could not find variable", 404)
        # print("variable not found")
    if variable.user_id is not None:
        return Response("Requested variable is not global", 400)

    match request.method:
        case "GET":

            return Response(variable.value)

        case "PUT":
            # get new data from request body
            new_data = request.data
            if "value" not in new_data.keys():
                return Response("Bad variable data", 400)
            if "mode" not in new_data.keys():
                mode = "set"
            else:
                mode = request.data["mode"]
            if type(new_data["value"]) is not int:
                return Response("Invalid variable value", 400)

            # if updating name, check if name's already taken in the event
            if "name" in new_data.keys():
                try:
                    DB.CustomVariable.objects.get(
                        event_id=eventid, name=new_data["name"]
                    )
                    return Response("Variable name already taken within event", 400)
                except DB.CustomVariable.DoesNotExist:
                    variable.name = new_data["name"]
                    if not CustomVariableSerializer(data=variable).is_valid():
                        return Response("Invalid variable name", 400)
            if mode == "add":
                variable.value += new_data["value"]
            if mode == "set":
                variable.value = new_data["value"]
            variable.save()

            # update observer
            observer.check_triggers(eventid, "value", variable.name, variable.value)

            return Response(CustomVariableSerializer(variable).data)

        case "DELETE":
            variable.delete()
            return Response("Variable deleted successfully")


@api_view(["GET", "PUT", "DELETE"])
def personal_variable(
    request, eventid: int, variable_name: str, user_id: int
) -> Response:
    """Get a personal custom variable value for a user in an event

    Args:
        request (Request): http request
        eventid (int): id of the event
        variable_name (str): name of the personal variable
        user_id (int): id of the user

    Returns:
        Response: value of that variable for the user
    """
    try:
        variable = DB.CustomVariable.objects.get(event_id=eventid, name=variable_name)
    except DB.CustomVariable.DoesNotExist:
        return Response("Could not find variable", 404)
    if variable.user_id is None:
        return Response("Requested variable is not personal", 400)

    match request.method:
        case "GET":

            return Response(variable.value)

        case "PUT":
            # get new data from request body
            new_data = request.data
            if "value" not in new_data.keys():
                return Response("Bad variable data", 400)
            if type(new_data["value"]) is not int:
                return Response("Invalid variable value", 400)

            # if updating name, check if name's already taken in the event
            if "name" in new_data.keys():
                try:
                    DB.CustomVariable.objects.get(
                        event_id=eventid, name=new_data["name"]
                    )
                    return Response("Variable name already taken within event", 400)
                except DB.CustomVariable.DoesNotExist:
                    variable.name = new_data["name"]
                    # if not CustomVariableSerializer(data=variable).is_valid():
                    #     return Response("Invalid variable name", 400)

            variable.value += new_data["value"]
            variable.save()

            # update observer
            observer.check_triggers(eventid, "value", variable.name, variable.value)

            return Response(CustomVariableSerializer(variable).data)

        case "DELETE":
            variable.delete()
            return Response("Variable deleted successfully")


@api_view(["POST"])
def post_variable(request, eventid: str) -> Response:
    """Post a custom variable for an event.
    Whether it's global or personal is determined by the presence
    of an user id

    Args:
        request (Request): http request
        eventid (str): id of the event

    Returns:
        Response: request response
    """

    # validate request data
    variable = request.data
    if not CustomVariableSerializer(data=variable).is_valid():
        return Response("Incorrect variable info", 400)

    variable = DB.CustomVariable(**variable)

    # sanitize event id
    variable.event_id = eventid
    variable.save()

    return Response(CustomVariableSerializer(variable).data)


@api_view(["POST"])
def captain_trigger(request, eventid: int, button_name: str) -> Response:

    match request.method:
        case "POST":
            try:
                observer.captain_trigger(eventid, button_name)
            except AttributeError:
                return Response("Captain button does not exist", 400)
            return Response(f"{button_name} Captain Trigger was... triggered...")


@api_view(["GET"])
def get_captain_buttons(request, eventid: int) -> Response:
    match request.method:
        case "GET":
            buttons = []
            try:
                for action in observer._dict[str(eventid)]:
                    try:
                        for column in action.conditions._triggers:
                            for trigger in column:
                                if type(trigger) is CaptainTrigger:
                                    buttons.append(trigger.variable_name)
                    except AttributeError:
                        continue
            except KeyError:
                return Response([], 404)

            return Response(buttons)


@api_view(["GET"])
def get_funcs(request, deviceid: int) -> Response:

    if deviceid == 0:
        return Response({"Edit Variable": "edit_variable"})

    try:
        device_type = DB.Device.objects.get(id=deviceid).type
    except DB.Device.DoesNotExist:
        return Response("Device does not exist", 404)
    data = {function: function for function in list(functions[device_type].keys())}
    return Response(data)


# ! Soon to be deprecated
@api_view(["GET"])
def get_trigger_types(request) -> Response:
    """Get available trigger types

    Returns:
        Response: dictionary containing name-value pairs
    """

    types = {
        "Value Trigger": "value",
        "Time Trigger": "time",
        "Date Trigger": "date",
        "Captain Trigger": "captain",
    }

    return Response(types, 200)


# ! DEPRECATED
@api_view(["GET"])
def get_html(request) -> Response:

    # function = request.GET.get("function")

    # html = """
    # <div>hello there</div>
    # """
    # select = """
    # <select value={data.arg} id=arg>
    #     <option value="none">None</option>
    #     <option value="something">Something</option>
    #     <option value="sure">Sure</option>
    # </select>
    # """
    # functions = {"test": html, "select": select}

    # return Response(functions[function])
    return Response("Deprecated endpoint", 501)
