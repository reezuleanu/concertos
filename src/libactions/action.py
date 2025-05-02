import copy
from .trigger import (
    TriggerSequence,
    ValueTrigger,
    Trigger,
    DateTrigger,
    CaptainTrigger,
    TimeTrigger,
)
from .command import Command, HardwareCommand, SoftwareCommand
from .device import Device
from .utils import get_dict_key


class Action:
    """Action class, it holds a name, a trigger object, and executes a function
    upon a device when the trigger conditions are met"""

    def __init__(
        self,
        name: str,
        conditions: TriggerSequence,
        commands: list[Command],
    ) -> None:

        self.name = name  # action name
        self.conditions = conditions  # trigger sequence object
        self.commands = commands  # command objects containing devices addresses, functions, and arguments

    def exec(self) -> None:
        """Execute all commands"""

        for command in self.commands:
            command.exec()


class ActionFactory:
    """Factory for Action objects. It parses trigger and command data, and returns an action object ready
    to be added to the observer"""

    def __init__(
        self,
        eventid: int,
        dbdevice,
        dbvariables,
        dbdeviceserializer,
        functions_table: dict,
    ) -> None:
        self.eventid = eventid
        self.dbdevice = dbdevice
        self.dbvariables = dbvariables
        self.dbdeviceserializer = dbdeviceserializer
        self.functions_table = functions_table

    def parse_triggers(self, triggers: list[list[dict]]) -> TriggerSequence:
        """Take triggers from the frontend and create a trigger sequence object

        Args:
            triggers (list): list of all triggers

        Returns:
            TriggerSequence: trigger sequence object
        """

        types_table = {
            "value": ValueTrigger,
            "date": DateTrigger,
            "time": TimeTrigger,
            "captain": CaptainTrigger,
        }

        # convert all trigger data into actual trigger objects based on the type provided
        for i in range(len(triggers)):
            column = triggers[i]
            for j in range(len(column)):
                trigger = column[j]
                trigger_type = trigger.pop("type")

                trigger = types_table[trigger_type](**trigger)

                triggers[i][j] = trigger

        # combine all triggers into a trigger sequence
        sequence = None
        for i in range(len(triggers)):
            if len(triggers[i]) == 0:
                continue
            if sequence is None:
                sequence = triggers[i][0]
            else:
                sequence = sequence * triggers[i][0]

            for j in range(1, len(triggers[i])):
                sequence = sequence + triggers[i][j]
        # if there is only one trigger, convert it to a sequence
        if issubclass(type(sequence), Trigger):
            sequence = TriggerSequence([[sequence]])

        # check triggers upon creation
        if sequence is not None:
            for column in sequence._triggers:
                for trigger in column:
                    try:
                        value = self.dbvariables.objects.get(
                            event_id=self.eventid, name=trigger.variable_name
                        ).value
                        sequence.update_state(
                            "value",
                            trigger.variable_name,
                            int(value),
                        )
                    except self.dbvariables.DoesNotExist:
                        continue

        return sequence

    @staticmethod
    def parse_commands(
        eventid: int,
        commands: list[dict],
        dbdevice,
        dbdeviceserializer,
        functions_table: dict[str, dict[str, callable]],
    ) -> list[Command]:
        """Parse command data from the front end into command objects

        Args:
            commands (list[dict]): list of command data
            dbdevice (model): django model, used to query the database
            dbdeviceserializer (serializer): django model serializer, to dump
            device data into a dictionary
            functions_table (dict[str, dict[str, callable]]): dict of devices and their appropriate name:function dict

        Returns:
            list[Command]: list of command objects
        """

        command_objects: list[Command] = []
        for command in commands:

            # determine command type
            match command.pop("type"):
                case "hardware":

                    # get device data from DB
                    device_data = dbdevice.objects.get(id=command["device"])
                    # serialize data
                    device_data = dbdeviceserializer(device_data).data
                    # create device object with the data, excluding the event foreign key
                    # device_data.pop("id")
                    device_data.pop("event_id")
                    device = Device(**device_data)
                    command["device"] = device

                    # replace function name with the actual function from the functions table
                    command["function"] = functions_table[device.type][
                        command["function"]
                    ]

                    # create command
                    command = HardwareCommand(**command)

                case "software":
                    command["function"] = functions_table["database"][
                        command["function"]
                    ]
                    command.pop("device")  # remove device
                    # command["args"][0] = eventid  # add event id
                    command["args"].insert(0, eventid)  # add event id
                    command = SoftwareCommand(**command)

            command_objects.append(command)

        return command_objects

    @staticmethod
    def deparse_triggers(triggers: list[list[Trigger]]) -> list[list[dict]]:
        """Dump trigger sequence data into a list of dictionaries. Used to format data
        before sending it to the frontend

        Args:
            triggers (list[list[Trigger]]): TriggerSequence._triggers usually

        Returns:
            list[list[dict]]: formatted trigger data, identical to what the frontend sends
        """

        types = {
            ValueTrigger: "value",
            DateTrigger: "date",
            TimeTrigger: "time",
            CaptainTrigger: "captain",
        }

        # make deep copy to avoid editing by referrence
        triggers = copy.deepcopy(triggers)

        for i in range(len(triggers)):
            for j in range(len(triggers[i])):
                if type(triggers[i][j]) is CaptainTrigger:
                    triggers[i][j] = {
                        "type": types[type(triggers[i][j])],
                        "variable_name": triggers[i][j].variable_name,
                    }
                else:
                    triggers[i][j] = {
                        "type": types[type(triggers[i][j])],
                        "variable_name": triggers[i][j].variable_name,
                        "condition": triggers[i][j].condition,
                        "target_value": triggers[i][j].target_value,
                    }

        return triggers

    @staticmethod
    def deparse_commands(
        commands: list[Command],
        functions_table: dict[str, dict[str, callable]],
    ) -> list[dict]:
        """Deparse command objects into dictionaries to be loaded on the
        front end

        Args:
            commands (list[Command]): list of command objects
            functions_table (dict[str, dict[str, callable]]): list of command types and their string equivalent

        Returns:
            list[dict]: list of command objects, deparsed
        """

        # type to string dictionary
        types = {HardwareCommand: "hardware", SoftwareCommand: "software"}

        deparsed_commands = []
        # create copy of objects
        commands = copy.deepcopy(commands)

        for command in commands:
            match types[type(command)]:
                case "hardware":

                    command = {
                        "type": "hardware",
                        "name": command.name,
                        "function": get_dict_key(
                            functions_table[command.device.type], command.function
                        ),
                        "args": command.args,
                        "device": command.device.id,
                    }
                case "software":

                    command = {
                        "type": "software",
                        "name": command.name,
                        "function": get_dict_key(
                            functions_table["database"], command.function
                        ),
                        "args": command.args[
                            1:
                        ],  # first position is the event id which we don't need
                        "device": "0",
                    }

            deparsed_commands.append(command)
        return deparsed_commands

    def parse(self, data: list[list[dict]], action_name: str) -> Action:
        """Parse triggers and commands into their respective objects,
        then combine to create a single Action object

        Args:
            data (list[list[dict]]): trigger and command data from the front end

        Returns:
            Action: resulting action object
        """

        # parse triggers
        parsed_triggers = self.parse_triggers(data[:-1])

        # parse commands
        parsed_commands = self.parse_commands(
            self.eventid,
            data[-1],
            self.dbdevice,
            self.dbdeviceserializer,
            self.functions_table,
        )

        # return action object
        return Action(action_name, parsed_triggers, parsed_commands)

    def deparse(self, data: Action) -> list[list[dict]]:
        """Dump action object data to be loaded by the front end

        Args:
            data (Action): action object

        Returns:
            list[list[dict]]: serialized action data
        """

        # dump triggers
        try:
            dumped_triggers = self.deparse_triggers(data.conditions._triggers)
        except AttributeError:
            dumped_triggers = [[], [], [], []]

        # dump commands
        # try:
        #     dumped_commads = self.deparse_commands(data.commands, self.functions_table)
        # except AttributeError:
        #     dumped_commads = []
        dumped_commads = self.deparse_commands(data.commands, self.functions_table)

        # combine the two
        dumped_triggers.append(dumped_commads)

        # insert empty columns if needed
        if len(dumped_triggers) < 5:
            difference = 5 - len(dumped_triggers)
            for _ in range(difference):
                dumped_triggers.insert(-1, [])

        # return data
        return dumped_triggers
