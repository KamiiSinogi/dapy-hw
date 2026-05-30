"""
Simulation runner for your algorithm.

Run with: uv run run-my-algo
Or: uv run python -m my_algo.run_my_algo
"""

from dapy.core import Asynchronous, Ring, System
from dapy.sim import Settings

# from .algorithm import MyAlgorithm, MySignal


def main() -> None:
    system = System(
        topology=Ring.of_size(5),
        synchrony=Asynchronous(),
    )

    print("=" * 60)
    print("Distributed Algorithm Simulation")
    print("=" * 60)
    print(f"Topology: {type(system.topology).__name__} with {len(list(system.processes()))} processes")
    print(f"Synchrony: {type(system.synchrony).__name__}")
    print()

    print("ERROR: Algorithm not implemented yet!")
    print("Please implement your algorithm in my_algo/algorithm.py")
    print("Then uncomment the algorithm instantiation in run_my_algo.py")
    return

    # Sample code to run your algorithm once implemented
    algorithm = MyAlgorithm(system)
    settings = Settings(enable_trace=True)
    sim = Simulator.from_system(system, algorithm, settings=settings)
    sim.start()
    sim.schedule(event=MySignal(target=Pid(1)))
    sim.run_to_completion()


if __name__ == "__main__":
    main()
