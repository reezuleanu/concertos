import os
import pickle
from .action import Action
from datetime import datetime
from time import sleep
import threading


class Observer:
    """Class for observer object, responsible for overseeing the backend and calling actions
    when their trigger conditions are met"""

    def __init__(self, path="") -> None:

        # dictionary containing the data, should not be accessed directly
        self._dict: dict[int, list[Action]] = {}
        self.path: str = path

        # load serialized triggers and actions
        if self.path != "":
            files = [file for file in os.listdir(path) if file.endswith(".act")]
        else:
            files = [file for file in os.listdir() if file.endswith(".act")]
        # print(files)
        # files = [file for file in os.listdir(path) if file.endswith(".act")]

        for file in files:
            try:
                event_name = file.split(".")[0]
                with open(f"{path}{file}", "rb") as fp:
                    self._dict[event_name] = pickle.load(fp)

            except Exception:
                print(f"Could not load actions for {event_name}, motive: {Exception}")

    def get_events(self) -> list[str]:
        """Method that returns a list with the names
        of all the events that have actions set up"""

        return [event for event in self._dict.keys()]

    def get_all_actions(self, event_id: int) -> list[Action]:
        """Method that returns a list of all the action for
        a specific event"""
        try:
            return self._dict[event_id]
        except KeyError:
            print(f"{event_id}: Event does not have actions set up or does not exist")

    def check_triggers(
        self, event_id: int, trigger_type: str, variable_name: str, variable_value: int
    ) -> None:
        """Update TriggerSequence states for a specific trigger type

        Args:
            event_id (int): name of the event to check for
            variable_name (str): name of the custom variable
            variable_value (int): value of the custom variable
        """

        if event_id not in self._dict.keys():
            raise Exception(
                f"{event_id}: Event has no actions set up or does not exist"
            )

        for action in self._dict[event_id]:
            if not action.conditions:
                continue
            if action.conditions.update_state(
                trigger_type, variable_name, variable_value
            ):
                # print(trigger_type, variable_name, variable_value, "True")
                t = threading.Thread(target=action.exec)
                t.start()
            else:
                # print(trigger_type, variable_name, variable_value, "False")
                pass

    def _add_event(self, event_name: str) -> None:
        """Method that adds an event in the dict if it doesn't already
        exist. If it does, return. Should only be called inside class
        methods.

        Args:
            event_name (str): name of event to add
        """

        if event_name not in self._dict.keys():
            self._dict[event_name] = []

    def add_action(self, event_name: str, action: Action) -> None:
        """Method that adds an action to an event in the
        observer.

        Args:
            event_name (str): name of event to add to
            action (Action): Action object
        """

        self._add_event(event_name)

        # check for duplicate name. if found, update action data
        query = [act for act in self._dict[event_name] if act.name == action.name]
        if len(query) > 0:
            index = self._dict[event_name].index(query[0])
            self._dict[event_name][index] = action
            return

        self._dict[event_name].append(action)

    def get_action(self, event_id: int, action_name: str) -> Action:
        """Get an action's data from the event via name

        Args:
            event_id (int): id of the event
            action_name (str): name of the action

        Returns:
            Action: action data
        """

        try:
            action = [
                action for action in self._dict[event_id] if action.name == action_name
            ][0]
        except (IndexError, KeyError):
            return None

        return action

    def edit_action(self, event_id: int, action_name: str, new_name: str) -> None:
        """Update an action name

        Args:
            event_id (int): id of the event
            action_name (str): name of the action
            new_name (str): new name for the action
        """
        try:
            action = [
                action for action in self._dict[event_id] if action.name == action_name
            ][0]
        except KeyError:
            raise Exception(f"Event {event_id} does not have any actions set up")
        except IndexError:
            raise Exception(f"Action not found in event {event_id}")

        action_index = self._dict[event_id].index(action)
        action.name = new_name

        print(self._dict[event_id][action_index])

    def delete_action(self, event_id: int, action_name: str) -> None:
        """Remove an action from an event via action name

        Args:
            event_name (int): event id to remove from
            action_name (str): name of action to remove
        """
        try:
            action = [
                action for action in self._dict[event_id] if action.name == action_name
            ]
            index = self._dict[event_id].index(action[0])
            self._dict[event_id].pop(index)

        except KeyError:
            raise Exception(f"{event_id} does not have any actions set up")
        except IndexError:
            raise Exception(f"Could not find action within for event {event_id}")

    def serialize_actions(self, event_id: int) -> None:
        """Method for serializing all actions for an event in
        a personal .act file.

        Args:
            event_id (int): id of event to serialize
        """

        # if event_id not in self._dict.keys():
        #     print(f"{event_id} does not exist!")
        #     return

        try:
            with open(f"{self.path}{event_id}.act", "wb") as fp:
                pickle.dump(self._dict[event_id], fp)
        except KeyError:
            raise Exception(f"Event {event_id} does not have actions set up")

    def captain_trigger(self, eventid: int, variable_name: str) -> None:
        self.check_triggers(eventid, "captain", variable_name, 1)
        self.check_triggers(eventid, "captain", variable_name, 0)

    def datetime_thread(self, interval: int = 1) -> None:
        """Function that checks DateTrigger and TimeTrigger objects for events at a fixed interval of time

        Args:
            interval (int, optional): Interval in seconds between each execution. Defaults to 1.
        """

        while True:
            try:
                for event in self._dict.keys():
                    date = datetime.now()
                    # try:
                    self.check_triggers(event, "date", "date", date)
                    self.check_triggers(event, "time", "time", date)
                    # print("got it")
                    # except AttributeError:
                    # print("problem")
                sleep(interval)
            except:
                pass
