"""Local-search improvement for the minimum vertex-cover problem.

The solver starts from the greedy degree cover, removes redundant vertices,
then repeatedly applies a strictly improving 2-for-1 swap.
"""
from .graphs import is_cover
from .vertex_cover import greedy_degree


def local_search(edges):
    """Return a valid cover no larger than the greedy-degree starting cover.

    A redundant selected vertex can be removed when all of its incident edges
    remain covered. A 2-for-1 swap removes two selected vertices and adds one
    unselected vertex, accepting the move only when it remains a valid cover.
    """
    edges = set(edges)
    cover = set(greedy_degree(edges))
    starting_size = len(cover)
    nodes = sorted({v for edge in edges for v in edge})

    # First remove every vertex whose removal preserves the cover property.
    changed = True
    while changed:
        changed = False
        for v in sorted(cover):
            candidate = cover - {v}
            if is_cover(edges, candidate):
                cover = candidate
                changed = True
                break

    # Then make strictly improving 2-for-1 swaps until none is available.
    while True:
        outside = [v for v in nodes if v not in cover]
        improved = False
        ordered_cover = sorted(cover)
        for i in range(len(ordered_cover)):
            if improved:
                break
            for j in range(i + 1, len(ordered_cover)):
                reduced = cover - {ordered_cover[i], ordered_cover[j]}
                for v in outside:
                    candidate = reduced | {v}
                    if is_cover(edges, candidate):
                        cover = candidate
                        improved = True
                        break
                if improved:
                    break
        if not improved:
            break

    # Defensive invariant: every accepted move is improving and valid.
    assert len(cover) <= starting_size
    assert is_cover(edges, cover)
    return cover
