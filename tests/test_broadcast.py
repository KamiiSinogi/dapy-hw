"""Tests for the broadcast example."""

from dapy.core import Asynchronous, Pid, Ring, System
from dapy.sim import Settings, Simulator

from broadcast.algo.algorithm import BroadcastAlgorithm, BroadcastState, Start


def test_broadcast_reaches_all_processes() -> None:
    system = System(topology=Ring.of_size(5), synchrony=Asynchronous())
    algorithm = BroadcastAlgorithm(system)
    settings = Settings(enable_trace=False)

    sim = Simulator.from_system(system, algorithm, settings=settings)
    sim.start()

    sim.schedule(event=Start(target=Pid(1)))
    sim.run_to_completion()

    for pid in sim.system.processes():
        state = sim.current_configuration[pid]
        assert isinstance(state, BroadcastState)
        assert state.has_sent
        assert state.value == 42
