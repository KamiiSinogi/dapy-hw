from dataclasses import dataclass, field
from typing import Sequence

from dapy.core import Algorithm, Event, Message, Pid, Signal, State
from dapy.core import ProcessSet


@dataclass(frozen=True)
class PIF_State(State):
    father: Pid | None = None
    children: set[Pid] = field(default_factory=set)
    neighbors: ProcessSet = field(default_factory=ProcessSet)
    count_back: int = 0


@dataclass(frozen=True)
class PIF_START(Signal):
    pass


@dataclass(frozen=True)
class PIF_GO(Message):
    pass


@dataclass(frozen=True)
class PIF_BACK(Message):
    pass


@dataclass(frozen=True)
class PIF_Algorithm(Algorithm[PIF_State]):
    algorithm_name: str | None = "hw1_PIF"

    def initial_state(self, pid: Pid) -> PIF_State:
        neighbor_set = self.system.topology.neighbors_of(pid)
        return PIF_State(
            pid = pid,
            father = pid if pid==Pid(1) else None,
            children = set(),
            neighbors = neighbor_set,
            count_back = len(neighbor_set))

    def on_event(self, old_state, event):
        match event:
            case PIF_START(_):
                events = [PIF_GO(target=node, sender=old_state.pid) 
                    for node in old_state.neighbors]
                return old_state, events
            
            case PIF_GO(_, sender):
                if old_state.father is not None:
                    return old_state, [PIF_BACK(target=sender, sender=old_state.pid)]
                events = [PIF_GO(target=node, sender=old_state.pid) 
                    for node in old_state.neighbors]
                new_state = old_state.cloned_with(father=sender)
                return new_state, events
            
            case PIF_BACK(_, sender):
                new_count_back = old_state.count_back - 1
                new_children = old_state.children | {sender}
                new_state = old_state.cloned_with(
                    children = new_children,
                    count_back = new_count_back)
                if new_count_back == 0:
                    if old_state.father != old_state.pid:
                        return new_state, [PIF_BACK(target=old_state.father, sender=old_state.pid)]
                    else:
                        print(f"Process {old_state.pid} is the root and has completed the PIF algorithm.")
                return new_state, []
            
            case _:
                return old_state, []
