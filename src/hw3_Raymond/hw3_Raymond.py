from dataclasses import dataclass, field

from dapy.core import Algorithm, Message, Pid, Signal, State
from dapy.core import ProcessSet


@dataclass(frozen=True)
class RN_State(State):
    parent: Pid | None = None
    neighbors: ProcessSet = field(default_factory=ProcessSet)


@dataclass(frozen=True)
class RN_TG_START(Signal):
    pass


@dataclass(frozen=True)
class RN_TG_GO(Message):
    pass


@dataclass(frozen=True)
class RN_TG_BACK(Message):
    pass


@dataclass(frozen=True)
class RN_Algorithm(Algorithm[RN_State]):
    algorithm_name: str | None = "hw3_Raymond"

    def initial_state(self, pid: Pid) -> RN_State:
        neighbor_set = self.system.topology.neighbors_of(pid)
        return RN_State(
            pid = pid,
            parent = pid if pid==Pid(1) else None,
            neighbors = neighbor_set)

    def on_event(self, old_state, event):
        match event:
            case RN_TG_START(_):
                return old_state, []
            
            case _:
                return old_state, []
