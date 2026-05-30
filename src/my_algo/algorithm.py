"""
Template algorithm implementation.

Replace MyAlgorithm, MyState, MyMessage, and MySignal with your own types.
"""

from dataclasses import dataclass
from typing import Sequence

from dapy.core import Algorithm, Event, Message, Pid, Signal, State


@dataclass(frozen=True)
class MyState(State):
    """State of a process in the algorithm."""

    # Add your fields here, for example:
    # counter: int = 0
    pass


@dataclass(frozen=True)
class MyMessage(Message):
    """Message exchanged between processes."""

    # Add your message fields here
    pass


@dataclass(frozen=True)
class MySignal(Signal):
    """Local signal delivered to a process."""

    # Add your signal fields here
    pass


@dataclass(frozen=True)
class MyAlgorithm(Algorithm[MyState]):
    """Describe your algorithm here."""

    def initial_state(self, pid: Pid) -> MyState:
        return MyState(pid=pid)

    def on_event(self, old_state: MyState, event: Event) -> tuple[MyState, Sequence[Event]]:
        # Implement your algorithm logic here
        new_state = old_state
        new_events: list[Event] = []
        return new_state, new_events
