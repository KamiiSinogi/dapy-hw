from pathlib import Path

from dataclasses import dataclass, field
from dapy.core import Asynchronous, Pid, System, ProcessSet
from dapy.core import Ring, CompleteGraph, Star
from dapy.core.topology import NetworkTopology
from dapy.sim import Settings, Simulator

from .hw3_Raymond import CV_Algorithm, CV_START

@dataclass(frozen=True)
class CustomTopology(NetworkTopology):
    adjacency: dict[Pid, ProcessSet] = field(default_factory=dict)
    
    def neighbors_of(self, pid):
        return self.adjacency.get(pid, ProcessSet())
    
    def processes(self):
        return ProcessSet(self.adjacency.keys())
    
    @classmethod
    def from_edges(cls, n, edges):
        adj = {Pid(i): set() for i in range(1, n+1)}
        for i, j in edges:
            adj[Pid(i)].add(Pid(j))
            adj[Pid(j)].add(Pid(i))
        return cls(adjacency={node: ProcessSet(edge) for node, edge in adj.items()})
    

def main() -> None:
    # 1. Create the system with its topology and synchrony.
    system = System(
        topology = CustomTopology.from_edges(n=12,
             edges=[(1,2), (2,3), (2,4), (1,5), (5,6), (5,7), #(4,9), (4,12), (9,12),
                    (6,7), (6,8), (7,8), (8,9), (1,10), (10,11), (11,12)]),
        synchrony=Asynchronous())

    print("=" * 60)
    print("Distributed Algorithm Simulation")
    print("=" * 60)
    print("Topology: ")
    for pid in sorted(system.topology.processes()):
        neighbors = system.topology.neighbors_of(pid)
        print(f"    {pid} : {', '.join(str(n) for n in sorted(neighbors))}")
    print(f"Synchrony: {type(system.synchrony).__name__}")
    print()

    # 2. Instantiate the algorithm
    algorithm = CV_Algorithm(system)
    print(f"Algorithm: {algorithm.name}")
    print()

    # 3. Create the simulator (e.g., with trace enabled)
    settings = Settings(enable_trace=True)
    sim = Simulator.from_system(system, algorithm, settings=settings)

    # 4. Start the simulator (initializes processes' states)
    sim.start()

    # 5. Create and schedule the initial event that starts the broadcast from process p1
    initiator = Pid(1)
    initial_event = CV_START(target=initiator)

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
    trace_file = traces_dir / "cutVert_trace.pkl"

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
