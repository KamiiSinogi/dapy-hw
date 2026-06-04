from dataclasses import dataclass, field

from dapy.core import Algorithm, Message, Pid, Signal, State
from dapy.core import ProcessSet


@dataclass(frozen=True)
class CV_State(State):
    dfn: int | None = None
    min_dfn: int | None = None
    min_child_dfn: int | None = None
    parent: Pid | None = None
    neighbors: ProcessSet = field(default_factory=ProcessSet)
    count_children: int | None = None
    count_back: int | None = None


@dataclass(frozen=True)
class CV_START(Signal):
    pass


@dataclass(frozen=True)
class CV_GO(Message):
    depth: int | None = None


@dataclass(frozen=True)
class CV_BACK(Message):
    children: bool | None = None
    depth: int | None = None


@dataclass(frozen=True)
class CV_Algorithm(Algorithm[CV_State]):
    algorithm_name: str | None = "hw2_cutVert"

    def initial_state(self, pid: Pid) -> CV_State:
        neighbor_set = self.system.topology.neighbors_of(pid)
        return CV_State(
            pid = pid,
            dfn = 1 if pid==Pid(1) else None,
            min_dfn = 20070831,
            min_child_dfn = 20070831,
            parent = pid if pid==Pid(1) else None,
            neighbors = neighbor_set,
            count_children = 0,
            count_back = len(neighbor_set))

    def on_event(self, old_state, event):
        match event:
            case CV_START(_):
                node = next(iter(old_state.neighbors))
                new_neighbors = set(old_state.neighbors) - {node}
                events = [CV_GO(target=node, sender=old_state.pid, depth=2)]
                new_state = old_state.cloned_with(neighbors=new_neighbors)
                return new_state, events
            
            case CV_GO(_, sender):
                if old_state.parent is not None:
                    return old_state, [CV_BACK(target=sender, sender=old_state.pid, depth=old_state.dfn, children=False)]
                new_neighbors = set(old_state.neighbors) - {sender}
                new_count_back = old_state.count_back - 1
                if new_count_back == 0:
                    events = [CV_BACK(target=sender, sender=old_state.pid, depth=old_state.min_dfn, children=True)]
                else:
                    node = next(iter(new_neighbors))
                    new_neighbors -= {node}
                    events = [CV_GO(target=node, sender=old_state.pid, depth=event.depth+1)]
                new_state = old_state.cloned_with(
                    dfn = event.depth,
                    parent = sender,
                    neighbors = new_neighbors,
                    count_back = new_count_back)
                return new_state, events
            
            case CV_BACK(_, sender):
                new_min_dfn = min(old_state.min_dfn, event.depth)
                if event.children:
                    new_min_child_dfn = min(old_state.min_child_dfn, event.depth)
                else:
                    new_min_child_dfn = old_state.min_child_dfn
                new_count_children = old_state.count_children + bool(event.children)
                new_count_back = old_state.count_back - 1
                if new_count_back !=0:
                    node = next(iter(old_state.neighbors))
                    new_neighbors = set(old_state.neighbors) - {node}
                    new_state = old_state.cloned_with(
                        min_dfn = new_min_dfn,
                        min_child_dfn = new_min_child_dfn,
                        neighbors = new_neighbors,
                        count_children = new_count_children,
                        count_back = new_count_back)
                    events = [CV_GO(target=node, sender=old_state.pid, depth=old_state.dfn+1)]
                else:
                    new_state = old_state.cloned_with(
                        min_dfn = new_min_dfn,
                        min_child_dfn = new_min_child_dfn,
                        count_children = new_count_children,
                        count_back = new_count_back)
                    if old_state.parent != old_state.pid:
                        events = [CV_BACK(target=old_state.parent, sender=old_state.pid, depth=new_min_dfn, children=True)]
                        if new_count_children > 0 and new_min_child_dfn >= old_state.dfn:
                            print(f"Process {old_state.pid} is a cut vertex.")
                    else:
                        events = []
                        if new_count_children > 1:
                            print(f"Process {old_state.pid} is a cut vertex.")
                        print("Search complete.")
                return new_state, events
            
            case _:
                return old_state, []
