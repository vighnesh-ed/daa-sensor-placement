"""A labelled campus network used by the security-sensor case study.

The algorithms use integer vertex IDs and undirected (u, v) edges with u < v.
The returned name_to_id map lets reports and plots display human-readable names.
"""
def build_campus_network():
    """Return (edges, name_to_id, capacities) for a small campus network.

    The campus contains an internet gateway, two firewalls, three switches,
    fifteen workstations, and three servers. Workstation-01 is dual-homed to
    two switches so it has two independent access links to the campus core.
    Link capacities represent the cost of cutting that link.
    """
    names = (
        ["internet", "firewall-1", "firewall-2",
         "switch-1", "switch-2", "switch-3"]
        + [f"workstation-{i:02d}" for i in range(1, 16)]
        + ["app-server", "file-server", "database"]
    )
    name_to_id = {name: i for i, name in enumerate(names)}
    links = []

    def add(a, b, cost):
        links.append((a, b, cost))

    # Internet edge and firewall uplinks are expensive to sever.
    add("internet", "firewall-1", 20)
    add("internet", "firewall-2", 20)
    add("firewall-1", "switch-1", 8)
    add("firewall-1", "switch-2", 8)
    add("firewall-2", "switch-2", 8)
    add("firewall-2", "switch-3", 8)

    # Redundant core links connect the three campus switches.
    add("switch-1", "switch-2", 6)
    add("switch-2", "switch-3", 6)
    add("switch-1", "switch-3", 6)

    # Five workstations per access switch. Workstation-01 is dual-homed.
    for i in range(1, 16):
        workstation = f"workstation-{i:02d}"
        if i == 1:
            add(workstation, "switch-1", 2)
            add(workstation, "switch-2", 2)
        elif i <= 5:
            add(workstation, "switch-1", 2)
        elif i <= 10:
            add(workstation, "switch-2", 2)
        else:
            add(workstation, "switch-3", 2)

    # Server links have a higher cut cost than workstation access links.
    add("app-server", "switch-1", 10)
    add("file-server", "switch-2", 10)
    add("database", "switch-2", 10)
    add("database", "switch-3", 10)

    edges = set()
    capacities = {}
    for a, b, cost in links:
        u, v = sorted((name_to_id[a], name_to_id[b]))
        edges.add((u, v))
        capacities[(u, v)] = cost

    return edges, name_to_id, capacities


def campus_summary(edges, name_to_id, capacities):
    """Return a concise, readable summary string for the campus network."""
    id_to_name = {v: k for k, v in name_to_id.items()}
    lines = [
        "Campus network summary",
        f"Machines: {len(name_to_id)}",
        f"Links: {len(edges)}",
        f"Total cut cost across all links: {sum(capacities.values())}",
        "Links (endpoint A -- endpoint B, cut cost):",
    ]
    for u, v in sorted(edges):
        lines.append(
            f"  {id_to_name[u]} -- {id_to_name[v]} "
            f"(cost {capacities[(u, v)]})"
        )
    return "\\n".join(lines)
