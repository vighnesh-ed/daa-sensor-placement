"""End-to-end campus security demo for sensor placement and isolation.

Run from the repository root:
    python -m experiments.scenario_demo
"""
from pathlib import Path

from sensorplace import (
    approx_matching, exact_branch_and_bound, greedy_degree, ilp, min_cut
)
from sensorplace.scenario import build_campus_network, campus_summary
from sensorplace.viz import draw


def _names(vertices, id_to_name):
    return ", ".join(id_to_name[v] for v in sorted(vertices))


def run():
    edges, name_to_id, capacities = build_campus_network()
    id_to_name = {v: name for name, v in name_to_id.items()}
    labels = id_to_name

    print(campus_summary(edges, name_to_id, capacities))
    print("\\nSENSOR PLACEMENT")
    solvers = [
        ("2-approximation", approx_matching(edges)),
        ("Greedy degree", greedy_degree(edges)),
    ]
    exact_cover, exact_finished = exact_branch_and_bound(edges, time_limit=30.0)
    solvers.append(("Exact Branch-and-Bound", exact_cover))
    solvers.append(("ILP", ilp(edges)))

    for name, cover in solvers:
        print(f"{name}: {len(cover)} sensors")
        print(f"  Sensors go on: {_names(cover, id_to_name)}")
    if not exact_finished:
        print("WARNING: exact search reached its time limit; its result is not "
              "proven optimal.")

    compromised = name_to_id["workstation-01"]
    database = name_to_id["database"]
    flow_value, cut = min_cut(edges, compromised, database, capacities)
    cut_cost = sum(capacities[edge] for edge in cut)
    print("\\nATTACKER ISOLATION")
    print(f"Compromised machine: workstation-01")
    print(f"Protected server: database")
    print(f"Cheapest cut cost / max-flow value: {flow_value}")
    print("Links to cut:")
    for u, v in cut:
        print(f"  {id_to_name[u]} -- {id_to_name[v]} "
              f"(cost {capacities[(u, v)]})")
    print(f"Verified total cut cost: {cut_cost}")

    unit_capacities = {edge: 1 for edge in edges}
    disjoint_count, _ = min_cut(
        edges, compromised, database, unit_capacities
    )
    print(f"Edge-disjoint attack paths: {disjoint_count}")

    figures = Path("figures")
    draw(
        edges, sensors=solvers[1][1], labels=labels,
        path=figures / "campus_sensor_placement.png"
    )
    draw(
        edges, cut=cut, labels=labels,
        path=figures / "campus_min_cut.png"
    )
    print("\\nSaved campus_sensor_placement.png and campus_min_cut.png")
    return {
        "solvers": solvers, "flow_value": flow_value, "cut": cut,
        "cut_cost": cut_cost, "edge_disjoint_paths": disjoint_count,
    }


if __name__ == "__main__":
    run()
