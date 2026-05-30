"""
Flooding Broadcast Algorithm - Example

A simple flooding broadcast where an initiator
broadcasts a value to all processes in the network.
"""

from dataclasses import dataclass, field
from typing import Sequence

from dapy.core import Algorithm, Event, Message, Pid, Signal, State


@dataclass(frozen=True)
class BroadcastState(State):
    """State of each process in the broadcast algorithm."""

    has_sent: bool = False
    value: int | None = None
    received_from: set[Pid] = field(default_factory=set)


@dataclass(frozen=True)
class BroadcastMsg(Message):
    """Message for broadcasting a value."""

    value: int


@dataclass(frozen=True)
class Start(Signal):
    """Signal to initiate the broadcast."""
    pass


@dataclass(frozen=True)
class BroadcastComplete(Signal):
    """Signal indicating this process has completed broadcasting."""

    value: int


@dataclass(frozen=True)
class BroadcastAlgorithm(Algorithm):
    """Simple flooding broadcast algorithm."""

    @property
    def name(self) -> str:
        return "Flooding Broadcast"

    def initial_state(self, pid: Pid) -> BroadcastState:
        return BroadcastState(pid=pid)

    def on_event(
        self,
        old_state: BroadcastState,
        event: Event,
    ) -> tuple[BroadcastState, Sequence[Event]]:
        match event:
            case Start(_):
                return self._initiate_broadcast(old_state, value=42)

            case BroadcastMsg(_, sender, value):
                if old_state.has_sent:
                    return old_state, []

                new_state = old_state.cloned_with(
                    has_sent=True,
                    value=value,
                    received_from=old_state.received_from | {sender},
                )

                neighbors = self.system.topology.neighbors_of(old_state.pid)
                messages = [
                    BroadcastMsg(target=neighbor, sender=old_state.pid, value=value)
                    for neighbor in neighbors
                    if neighbor != sender
                ]

                complete_signal = BroadcastComplete(
                    target=old_state.pid,
                    value=value,
                )

                return new_state, [*messages, complete_signal]

            case BroadcastComplete(_, value):
                print(f"Process {old_state.pid} completed broadcast with value {value}")
                return old_state, []

            case _:
                raise NotImplementedError(
                    f"Event {type(event).__name__} not handled by {self.name}"
                )

    def _initiate_broadcast(
        self,
        state: BroadcastState,
        value: int,
    ) -> tuple[BroadcastState, Sequence[Event]]:
        new_state = state.cloned_with(
            has_sent=True,
            value=value,
        )

        neighbors = self.system.topology.neighbors_of(state.pid)
        messages = [
            BroadcastMsg(target=neighbor, sender=state.pid, value=value)
            for neighbor in neighbors
        ]

        return new_state, messages
