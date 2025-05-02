from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Trigger(ABC):
    """Abstract class for trigger objects, all different trigger types will
    inherit from this"""

    @abstractmethod
    def val(self) -> bool:
        """Check if trigger conditions are met

        Returns:
            bool: conditions met
        """
        pass

    def __add__(self, other) -> object:
        """Add two trigger objects into a trigger sequence object in an OR logic relation"""

        if not issubclass(type(other), Trigger):
            raise TypeError("You can only add other trigger objects")

        return TriggerSequence([[self, other]])

    def __mul__(self, other) -> object:
        """Multiply two trigger objects into a trigger sequence object in an AND logic relation"""

        if not issubclass(type(other), Trigger):
            raise TypeError("You can only multiply with other trigger objects")

        return TriggerSequence([[self], [other]])


class ValueTrigger(Trigger):
    """Trigger type that is fulfilled based on a relation between a variable and a target
    variable"""

    def __init__(self, variable_name: str, condition: str, target_value: int) -> None:

        conditions = [">", "<", "=", ">=", "<=", "!"]
        self.variable_name = variable_name
        self.target_value = int(target_value)

        if condition not in conditions:
            raise Exception("Invalid condition")

        self.condition = condition

    def val(self, variable_name, variable_value) -> bool:
        if variable_name != self.variable_name:
            return None

        match self.condition:
            case ">":
                val = variable_value > int(self.target_value)
            case "<":
                val = variable_value < self.target_value
            case "=":
                val = variable_value == self.target_value
            case ">=":
                val = variable_value >= self.target_value
            case "<=":
                val = variable_value <= self.target_value
            case "!":
                val = variable_value != self.target_value
            case _:
                val = False

        return val


class CaptainTrigger(Trigger):
    """Trigger that is activated manually from the platform, by the admin"""

    def __init__(self, variable_name: str, **kwargs) -> None:

        self.variable_name = variable_name

    def val(self, variable_name, variable_value) -> bool:
        if variable_name != self.variable_name:
            return None

        return variable_value


class TimeTrigger(Trigger):
    """Trigger that is activated when a certain amount of time has passed"""

    def __init__(self, variable_name: str, condition: str, target_value: int) -> None:

        self.variable_name = "time"
        self.time_created = datetime.now()
        self.target_value = target_value
        self.condition = ">="

    def val(self, variable_name: str, variable_value: datetime) -> bool:

        return variable_value >= self.time_created + timedelta(
            seconds=int(self.target_value)
        )


class DateTrigger(Trigger):
    """Trigger that is activated at a certain date and time"""

    def __init__(self, variable_name: str, condition: str, target_value: int) -> None:

        conditions = [">", "<", "=", ">=", "<=", "!"]
        self.variable_name = "date"
        self.target_value = datetime.fromisoformat(target_value)

        if condition not in conditions:
            raise Exception("Invalid condition")

        self.condition = condition

    def val(self, variable_name: str, variable_value: datetime) -> bool:
        # adjust timezone
        variable_value = variable_value + timedelta(hours=3)
        # print(variable_value, self.target_value)
        match self.condition:
            case ">":
                val = variable_value > self.target_value
            case "<":
                val = variable_value < self.target_value
            case "=":
                val = variable_value == self.target_value
            case ">=":
                val = variable_value >= self.target_value
            case "<=":
                val = variable_value <= self.target_value
            case "!":
                val = variable_value != self.target_value
            case _:
                val = False

        return val


class TriggerSequence:

    def __init__(self, trigger_sequence: list[list[Trigger]]) -> None:

        # list of triggers, mantaining their logic structure
        self._triggers: list[list[Trigger]] = trigger_sequence

        # list of the states of the triggers, mantaining their logic structure
        self._states: list[list[bool]] = []

        # on initialization, copy the logic structure of the triggers
        # to the states, and set all states to False
        for i in range(len(self._triggers)):
            self._states.append([])
            for state in self._triggers[i]:
                self._states[i].append(False)

    def __add__(self, other: Trigger) -> None:
        """Add a trigger object to the trigger sequence in an OR logic relation.
        The added trigger will be added at the end of the sequence.

        Args:
            other (Trigger): trigger object to add

        Raises:
            TypeError: if the added object is not a subclass of Trigger
        """

        if not issubclass(type(other), Trigger):
            raise TypeError("You can only add trigger objects to a trigger sequence")
        self._triggers[-1].append(other)
        self._states[-1].append(False)
        return self

    def __mul__(self, other: Trigger) -> None:
        """Add a trigger object to the trigger sequence in an AND logic relation.


        Args:
            other (Trigger): trigger to add to the sequence

        Raises:
            TypeError: if the added object is not a subclass of Trigger
        """

        if not issubclass(type(other), Trigger):
            raise TypeError(
                "You can only multiply trigger objects with a trigger sequence"
            )
        self._triggers.append([other])
        self._states.append([False])
        return self

    def _val(self) -> bool:
        """Check if the sequence is fulfilled"""

        result = 1
        for pair in self._states:
            result = result * max(pair)

        return bool(result)

    def update_state(
        self, trigger_type: str, variable_name: str, variable_value: int
    ) -> bool:
        """Call the triggers val method to update the sequence states.
        If at least one state becomes True, check if the sequence is fulfilled.

        Args:
            trigger_type (str): the type of trigger to update
            variable_name (str): the name of the provided variable
            variable_value (int): variable value

        Returns:
            bool: Returns true if all conditions in the sequence are
            satisfied
        """

        # dict containing string class pairs for the triggers
        types = {
            "value": ValueTrigger,
            "date": DateTrigger,
            "time": TimeTrigger,
            "captain": CaptainTrigger,
        }

        if trigger_type not in types.keys():
            raise Exception("Invalid trigger type")
        trigger_type = types[trigger_type]

        triggered_once = False
        for i in range(len(self._triggers)):
            pair = self._triggers[i]
            for j in range(len(pair)):
                trigger = pair[j]
                if type(trigger) is trigger_type:
                    if trigger.variable_name != variable_name:
                        continue
                    value = trigger.val(variable_name, variable_value)
                    if value is not None:
                        self._states[i][j] = bool(value)

                    if self._states[i][j] is True:
                        triggered_once = True

        if triggered_once:
            return self._val()

        return triggered_once
