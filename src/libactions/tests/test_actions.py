from ..action import Action
from ..trigger import (
    ValueTrigger,
    DateTrigger,
    CaptainTrigger,
    TimeTrigger,
    TriggerSequence,
)
from ..observer import Observer
from ..device import Device
from ..command import HardwareCommand
from ..firework_launcher import launch
from ..lights import change_color
import pytest
import os
from datetime import datetime, timedelta


"""Testing trigger class"""


def test_init_value_trigger() -> None:
    """Test creating a ValueTrigger object"""

    trigger = ValueTrigger(
        "var",
        "=",
        4,
    )

    del trigger


def test_init_value_trigger_exception() -> None:
    """Test creating a ValueTrigger object with bad arguments"""

    with pytest.raises(Exception) as e:
        trigger = ValueTrigger("var", "invalid", 1)
        del trigger

    assert str(e.value) == "Invalid condition"


def test_meet_value_trigger() -> None:
    """Test if the trigger returns true if the conditions are met"""

    trigger = ValueTrigger(
        "var",
        "=",
        4,
    )

    assert trigger.val("var", 1) is False
    assert trigger.val("not_var", 4) is None
    assert trigger.val("var", 4) is True


"""Testing different functions"""


def test_launch() -> None:
    """Test if the fireworks launch action actually works"""

    device = Device(0, "Fireworks launcher", "firework_launcher", "127.0.0.1", 2727)
    command = HardwareCommand("Welcome Fireworks", launch, [None], device)
    action = Action("actiune", None, [command])
    action.exec()


def test_change_color() -> None:
    """Test if the lights change color"""

    device = Device(0, "wifi lights", "lights", "127.0.0.2", 2727)
    command = HardwareCommand("Welcome lights", change_color, ["#fff"], device)
    action = Action("actiune", None, [command])
    action.exec()


"""Testing Action class"""


def test_action_value_trigger() -> None:
    """Test triggering action with value trigger"""

    trigger = ValueTrigger("var", "=", 5)
    device = Device(0, "wifi lights", "lights", "127.0.0.2", 2727)
    command = HardwareCommand("Welcome lights", change_color, ["#fff"], device)
    action = Action("test", trigger, [command])
    observer = Observer()

    observer.add_action("event", action)

    v = 0

    assert observer._dict["event"][0].conditions.val("var", v) is False

    v = 5

    assert observer._dict["event"][0].conditions.val("var", v) is True

    v = 6

    assert observer._dict["event"][0].conditions.val("var", v) is False


def test_multiple_commands():
    """Test action with multiple functions and devices"""
    device1 = Device(0, "Fireworks launcher", "firework_launcher", "127.0.0.1", 2727)
    command1 = HardwareCommand("welcome fireworks", launch, [None], device1)
    device2 = Device(0, "wifi lights", "lights", "127.0.0.2", 2727)
    command2 = HardwareCommand("Welcome lights", change_color, ["#fff"], device2)

    action = Action("test", None, [command1, command2])

    assert (
        action.commands[0].function is command1.function
        and action.commands[0].args == [None]
        and action.commands[0].device.name == "Fireworks launcher"
        and action.commands[0].device.type == "firework_launcher"
    )

    assert (
        action.commands[1].function is change_color
        and action.commands[1].args == ["#fff"]
        and action.commands[1].device.name == "wifi lights"
        and action.commands[1].device.type == "lights"
    )


"""Testing Observer Class"""


def test_init_observer_noload() -> None:
    """Test creating an observer object, with no actions to be loaded"""

    observer = Observer()

    del observer


def test_observer_add_action() -> None:
    """Test adding an action to the observer"""

    observer = Observer()

    trigger = ValueTrigger("var", "=", 5)
    device = Device(0, "fireworks launcher", "launcher", "127.0.0.1", 2727)
    command = HardwareCommand("launch fireworks", launch, [None], device)
    action = Action("test", trigger, [command])

    observer.add_action("event", action)

    assert (
        len([action for action in observer._dict["event"] if action.name == "test"]) > 0
    )
    assert observer._dict["event"][0].name == action.name


def test_observer_serialize_actions() -> None:
    """Test serializing actions in memory"""

    observer = Observer()

    trigger = ValueTrigger("var", "=", 5)
    device = Device(0, "fireworks launcher", "firework_launcher", "127.0.0.1", 2727)
    command = HardwareCommand("welcome fireworks", launch, [None], device)
    action = Action("test", trigger, [command])
    action2 = Action("test2", trigger, [command])

    observer.add_action("event", action)
    observer.add_action("event", action2)

    assert len(observer._dict["event"]) == 2

    observer.serialize_actions("event")


def test_init_observer_load() -> None:
    """Test creating an observer object and having it load saved actions
    into memory"""

    observer = Observer()

    assert "event" in observer._dict.keys()
    assert len(observer._dict["event"]) == 2

    action_names = [action.name for action in observer._dict["event"]]
    assert "test" in action_names
    assert "test2" in action_names


def test_cleanup() -> None:
    """Clean up any serialized data"""

    serialized_actions = [file for file in os.listdir() if file.endswith(".act")]
    for file in serialized_actions:
        os.remove(file)


def test_observer() -> None:
    """Test the overall functionality of the library, for value triggers"""

    observer = Observer()

    trigger1 = ValueTrigger("variabila", ">", 20)
    trigger2 = ValueTrigger("variabila", "<", 30)

    sequence = trigger1 * trigger2

    device = Device(0, "wifi lights", "lights", "127.0.0.1", 2727)
    command = HardwareCommand("welcome lights", change_color, ["#fff"], device)
    action = Action("actiune", sequence, [command])

    observer.add_action("event1", action)

    observer.check_triggers("event1", "value", "variabila", 10)
    assert observer.get_all_actions("event1")[0].conditions._states == [[False], [True]]

    observer.check_triggers("event1", "value", "variabila", 21)
    assert observer.get_all_actions("event1")[0].conditions._states == [[True], [True]]

    observer.check_triggers("event1", "value", "variabila", 30)
    assert observer.get_all_actions("event1")[0].conditions._states == [[True], [False]]


def test_datetime() -> None:

    date_target = (datetime.now() + timedelta(hours=3)).isoformat()
    # time_target = (datetime.now() + timedelta(hours=1)).isoformat()
    device = Device(0, "wifi lights", "lights", "127.0.0.1", 2727)
    command = HardwareCommand("test wifi", change_color, ["#d9d9d9"], device)

    trigger1 = DateTrigger("date", ">=", date_target)
    trigger2 = TimeTrigger("time", ">=", 3600)

    action = Action("action", TriggerSequence([[trigger1, trigger2]]), [command])

    observer = Observer()
    observer.add_action("event", action)

    observer.check_triggers(
        "event", "date", "date", datetime.now() - timedelta(hours=3)
    )
    assert action.conditions._states == [[False, False]]

    observer.check_triggers(
        "event",
        "date",
        "date",
        datetime.now() - timedelta(hours=3) + timedelta(minutes=30),
    )
    observer.check_triggers(
        "event", "time", "time", datetime.now() + timedelta(minutes=30)
    )
    assert action.conditions._states == [[False, False]]

    observer.check_triggers(
        "event",
        "date",
        "date",
        datetime.now() - timedelta(hours=3) + timedelta(hours=1),
    )
    observer.check_triggers(
        "event", "time", "time", datetime.now() + timedelta(hours=1)
    )
    assert action.conditions._states == [[False, True]]

    observer.check_triggers(
        "event",
        "date",
        "date",
        datetime.now() - timedelta(hours=3) + timedelta(hours=3),
    )
    observer.check_triggers(
        "event", "time", "time", datetime.now() + timedelta(hours=3)
    )
    assert action.conditions._states == [[True, True]]

    observer.check_triggers(
        "event",
        "date",
        "date",
        datetime.now() - timedelta(hours=3) + timedelta(hours=3),
    )
    observer.check_triggers("event", "time", "time", datetime.now())
    assert action.conditions._states == [[True, False]]


def test_captain_trigger() -> None:

    observer = Observer()
    trigger = CaptainTrigger("test button")
    action = Action("action", TriggerSequence([[trigger]]), [])
    observer.add_action("event", action)

    observer.captain_trigger("event", "test button")
    assert action.conditions._states == [[False]]
