# data.py

import warnings
import datetime as dt
import time
from abc import ABCMeta, abstractmethod
import threading
from itertools import chain
from typing import Any

from looperator import Operator

from represent import represent

from crypto_screening.foundation.state import WaitingState

__all__ = [
    "DataCollector"
]

TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

def extract_attributes(data: Any, /) -> dict[str, Any]:
    """
    Gets all attributes of an object.

    :param data: The object.

    :return: The attributes of the object.
    """

    return {
        **(data.__dict__ if hasattr(data, '__dict__') else {}),
        **(
            {
                key: getattr(data, key)
                for key in chain.from_iterable(
                    getattr(cls, '__slots__', [])
                    for cls in type(data).__mro__
                ) if hasattr(data, key)
            } if hasattr(data, '__slots__') else {}
        )
    }
# end extract_attributes

@represent
class DataCollector(metaclass=ABCMeta):
    """A class to represent an abstract parent class of data collectors."""

    LOCATION = "datasets"

    DELAY = 0
    CANCEL = 0

    __slots__ = (
        "location", "delay", "cancel", "_screening",
        "_blocking", "_saving", "_updating", "_screening_process",
        "_timeout_process", "_saving_process", "_updating_process"
    )

    def __init__(
            self,
            location: bool = None,
            cancel: TimeDestination = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        if delay is None:
            delay = self.DELAY
        # end if

        if cancel is None:
            cancel = self.CANCEL
        # end if

        self.cancel = cancel
        self.delay = delay

        self.location = location or self.LOCATION

        self._screening = False
        self._blocking = False
        self._saving = False
        self._updating = False

        self._timeout_process = Operator(termination=self.stop, loop=False)

        self._screening_process: threading.Thread | None = None
        self._saving_process: threading.Thread | None = None
        self._updating_process: threading.Thread | None = None
    # end __init__

    def __getstate__(self) -> dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = extract_attributes(self)

        for key, value in data.items():
            if isinstance(value, threading.Thread):
                data[key] = None
            # end if
        # end for

        return data
    # end __getstate__

    @property
    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._blocking
    # end blocking

    @property
    def screening(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._screening
    # end screening

    @property
    def saving(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._saving
    # end saving

    @property
    def updating(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._updating
    # end updating

    @property
    def timeout(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._timeout_process.timeout
    # end timeout

    def screening_loop(self) -> None:
        """Runs the process of the price screening."""
    # end screening_loop

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""
    # end saving_loop

    def update_loop(self) -> None:
        """Updates the state of the screeners."""
    # end update_loop

    def timeout_loop(self, duration: TimeDestination) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        self._timeout_process.timeout_loop(duration=duration)
    # end timeout_loop

    @abstractmethod
    def await_initialization(
            self,
            stop: bool | int = False,
            delay: TimeDuration = None,
            cancel: TimeDestination = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """
    # end base_wait_for_initialization

    @abstractmethod
    def await_update(
            self,
            stop: bool | int = False,
            delay: TimeDuration = None,
            cancel: TimeDestination = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """
    # end base_wait_for_update

    def start_blocking(self) -> None:
        """Starts the blocking process."""

        if self.blocking:
            warnings.warn(
                f"Blocking process of "
                f"{repr(self)} is already running."
            )

            return
        # end if

        self._blocking = True

        while self.blocking:
            time.sleep(0.005)
        # end while
    # end start_blocking

    def start_screening(self) -> None:
        """Starts the screening process."""

        if self.screening:
            warnings.warn(
                f"Screening process of "
                f"{repr(self)} is already running."
            )

            return
        # end if

        self._screening = True

        self._screening_process = threading.Thread(
            target=self.screening_loop
        )

        self._screening_process.start()
    # end start_screening

    def start_saving(self) -> None:
        """Starts the saving process."""

        if self.saving:
            warnings.warn(
                f"Saving process of "
                f"{repr(self)} is already running."
            )

            return
        # end if

        self._saving = True

        self._saving_process = threading.Thread(
            target=self.saving_loop
        )

        self._saving_process.start()
    # end start_saving

    def start_updating(self) -> None:
        """Starts the updating process."""

        if self.updating:
            warnings.warn(
                f"Updating process of "
                f"{repr(self)} is already running."
            )

            return
        # end if

        self._updating = True

        self._updating_process = threading.Thread(
            target=self.update_loop
        )

        self._updating_process.start()
    # end start_updating

    def start_waiting(self, wait: bool | TimeDestination) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if wait is True:
            self.await_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if
    # end start_waiting

    def start_timeout(self, duration: TimeDestination) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        self._timeout_process.start_timeout(duration=duration)
    # end start_timeout

    def pause_timeout(self) -> None:
        """Pauses the timeout process."""

        self._timeout_process.pause()
    # end pause_timeout

    def unpause_timeout(self) -> None:
        """Pauses the timeout process."""

        self._timeout_process.unpause()
    # end unpause_timeout

    def run(
            self,
            screen: bool = True,
            save: bool = True,
            block: bool = False,
            update: bool = True,
            wait: bool | TimeDestination = False,
            timeout: TimeDestination = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param screen: The value to start the screening.
        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param update: The value to update the screeners.
        :param timeout: The valur to add a start_timeout to the process.
        """

        if screen:
            self.start_screening()
        # end if

        if save:
            self.start_saving()
        # end if

        if update:
            self.start_updating()
        # end if

        if timeout:
            self.start_timeout(timeout)
        # end if

        if wait:
            self.start_waiting(wait)
        # end if

        if block:
            self.start_blocking()
        # end if
    # end run

    def stop_screening(self) -> None:
        """Stops the screening process."""

        if self.screening:
            self._screening = False
        # end if

        if (
            isinstance(self._screening_process, threading.Thread) and
            self._screening_process.is_alive()
        ):
            self._screening_process = None
        # end if
    # end stop_screening

    def stop_saving(self) -> None:
        """Stops the screening process."""

        if self.saving:
            self._saving = False
        # end if
        if (
            isinstance(self._saving_process, threading.Thread) and
            self._saving_process.is_alive()
        ):
            self._saving_process = None
        # end if
    # end stop_saving

    def stop_updating(self) -> None:
        """Stops the screening process."""

        if self.updating:
            self._updating = False
        # end if
        if (
            isinstance(self._updating_process, threading.Thread) and
            self._updating_process.is_alive()
        ):
            self._updating_process = None
        # end if
    # end stop_updating

    def stop_timeout(self) -> None:
        """Stops the screening process."""

        self._timeout_process.stop_timeout()
    # end stop_timeout

    def stop_blocking(self) -> None:
        """Stops the screening process."""

        if self.blocking:
            self._blocking = False
        # end if
    # end stop_blocking

    def stop(self) -> None:
        """Stops the screening process."""

        self.stop_screening()
        self.stop_saving()
        self.stop_blocking()
        self.stop_updating()
        self.stop_timeout()
    # end stop
# end DataCollector