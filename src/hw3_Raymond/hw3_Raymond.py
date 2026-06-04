from dataclasses import dataclass, field

from dapy.core import Algorithm, Message, Pid, Signal, State
from dapy.core import ProcessSet


@dataclass(frozen=True)
class RN_State(State):
    parent: Pid | None = None
    neighbors: ProcessSet = field(default_factory=ProcessSet)
    count_back: int | None = None
    request_list: tuple[Pid, ...] = field(default_factory=tuple)
    request_queue: tuple[Pid, ...] = field(default_factory=tuple)
    interested: bool | None = None
    object: bool | None = None


@dataclass(frozen=True)
class RN_TG_START(Signal):
    request_list: tuple[Pid, ...] = field(default_factory=tuple)
    pass


@dataclass(frozen=True)
class RN_TG_GO(Message):
    pass


@dataclass(frozen=True)
class RN_TG_BACK(Message):
    pass


@dataclass(frozen=True)
class RN_START(Signal):
    pass


@dataclass(frozen=True)
class RN_REQUEST(Message):
    pass


@dataclass(frozen=True)
class RN_RELEASE(Signal):
    pass


@dataclass(frozen=True)
class RN_OBJECT(Message):
    request: bool | None = None


@dataclass(frozen=True)
class RN_Algorithm(Algorithm[RN_State]):
    algorithm_name: str | None = "hw3_Raymond"

    def initial_state(self, pid: Pid) -> RN_State:
        neighbor_set = self.system.topology.neighbors_of(pid)
        return RN_State(
            pid = pid,
            parent = pid if pid==Pid(1) else None,
            neighbors = neighbor_set,
            count_back = len(neighbor_set),
            request_list = tuple(),
            request_queue = tuple(),
            interested = False,
            object = True if pid==Pid(1) else False)

    def on_event(self, old_state, event):
        match event:
            case RN_TG_START(_):
                events = [RN_TG_GO(target=node, sender=old_state.pid) 
                    for node in old_state.neighbors]
                new_state = old_state.cloned_with(request_list = event.request_list)
                return new_state, events
            
            case RN_TG_GO(_, sender):
                if old_state.parent is not None:
                    return old_state, [RN_TG_BACK(target=sender, sender=old_state.pid)]
                print(f"Process {old_state.pid} has set its parent to process {sender}.")
                new_state = old_state.cloned_with(parent=sender)
                events = [RN_TG_GO(target=node, sender=old_state.pid) 
                    for node in old_state.neighbors]
                return new_state, events
            
            case RN_TG_BACK(_, sender):
                new_count_back = old_state.count_back - 1
                new_state = old_state.cloned_with(count_back = new_count_back)
                if new_count_back == 0:
                    if old_state.parent != old_state.pid:
                        return new_state, [RN_TG_BACK(target=old_state.parent, sender=old_state.pid)]
                    else:
                        print(f"Process {old_state.pid} is the root and has completed the Tree-generation.")
                        return new_state, [RN_START(target=node) for node in old_state.request_list]
                return new_state, []

            case RN_START(_):
                print(f"Process {old_state.pid} has received the start signal for request.")
                new_interested = True
                if old_state.object:
                    new_request_queue = old_state.request_queue
                    events = [RN_RELEASE(target=old_state.pid)]
                elif old_state.request_queue:
                    new_request_queue = old_state.request_queue + (old_state.pid,)
                    events = []
                else:
                    new_request_queue = (old_state.pid,)
                    events = [RN_REQUEST(target=old_state.parent, sender=old_state.pid)]
                new_state = old_state.cloned_with(
                    interested = new_interested,
                    request_queue = new_request_queue)
                return new_state, events
            
            case RN_REQUEST(_, sender):
                if old_state.request_queue:
                    new_request_queue = old_state.request_queue + (sender,)
                    events = []
                elif old_state.object:
                    new_request_queue = (sender,)
                    events = [RN_RELEASE(target=old_state.pid)]
                else:
                    new_request_queue = (sender,)
                    events = [RN_REQUEST(target=old_state.parent, sender=old_state.pid)]
                new_state = old_state.cloned_with(request_queue = new_request_queue)
                return new_state, events

            case RN_RELEASE(_):
                if old_state.interested:
                    print(f"Process {old_state.pid} has ended its request for the object.")
                if old_state.request_queue:
                    new_parent = old_state.request_queue[0]
                    new_request_queue = old_state.request_queue[1:]
                    new_object = False
                    events = [RN_OBJECT(target=new_parent, sender=old_state.pid, request=new_request_queue)]
                else:
                    new_parent = old_state.parent
                    new_request_queue = old_state.request_queue
                    new_object = old_state.object
                    events = []
                new_state = old_state.cloned_with(
                    parent = new_parent,
                    request_queue = new_request_queue,
                    interested = False,
                    object = new_object)
                return new_state, events
             
            case RN_OBJECT(_, sender):
                new_request_queue = old_state.request_queue[1:]
                if event.request:
                    new_request_queue += (sender,)
                if old_state.request_queue[0] == old_state.pid:
                    new_parent = old_state.pid
                    new_object = True
                    events = [RN_RELEASE(target=old_state.pid)]
                else:
                    new_parent = old_state.request_queue[0]
                    new_object = old_state.object
                    events = [RN_OBJECT(target=new_parent, sender=old_state.pid, request=new_request_queue)]
                new_state = old_state.cloned_with(
                    parent = new_parent,
                    request_queue = new_request_queue,
                    object = new_object)
                return new_state, events
             
            case _:
                return old_state, []