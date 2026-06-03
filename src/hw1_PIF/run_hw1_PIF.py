from pathlib import Path

from dapy.core import Asynchronous, Pid, System
from dapy.core import Ring, CompleteGraph, Star
from dapy.sim import Settings, Simulator

from .hw1_PIF import PIF_Algorithm, PIF_START


def main() -> None:
    # 1. Create the system with its topology and synchrony.
    system = System(
        topology=Ring.of_size(5),
        synchrony=Asynchronous(),
    )

    print("=" * 60)
    print("Distributed Algorithm Simulation")
    print("=" * 60)
    print("Topology: Ring of 5 processes")
    print(f"Synchrony: {type(system.synchrony).__name__}")
    print()

    # 2. Instantiate the algorithm
    algorithm = PIF_Algorithm(system)
    print(f"Algorithm: {algorithm.name}")
    print()

    # 3. Create the simulator (e.g., with trace enabled)
    settings = Settings(enable_trace=True)
    sim = Simulator.from_system(system, algorithm, settings=settings)

    # 4. Start the simulator (initializes processes' states)
    sim.start()

    # 5. Create and schedule the initial event that starts the broadcast from process p1
    initiator = Pid(1)
    initial_event = PIF_START(target=initiator)

    print(f"Initiating broadcast from process {initiator}")
    sim.schedule(event=initial_event)
    print()

    # 6. Run the simulation to completion (until no more events are left)
    print("Running simulation...")
    sim.run_to_completion()
    print()

    # The simulator can also be run step-by-step if needed:
    # while not sim.is_complete():
    #     sim.step()

    # 7. Optionally, save the trace to a file for later visualization
    traces_dir = Path("traces")
    traces_dir.mkdir(exist_ok=True)
    trace_file = traces_dir / "PIF_trace.pkl"

    with open(trace_file, "wb") as f:
        assert sim.trace is not None
        f.write(sim.trace.dump_pickle())

    print("=" * 60)
    print("Simulation Complete!")
    print("=" * 60)
    print(f"Trace saved to: {trace_file}")
    print()
    print("Visualize with:")
    print(f"  dapyview {trace_file}")
    print()

    print("Statistics:")
    print(f"  Total events in trace: {len(sim.trace.events_list)}")
    print(f"  Simulation time: {sim.current_time}")
    print()


if __name__ == "__main__":
    main()
