# Complexity Table

- Owner: Person 1 (owns the table; each row is filled in by the person named in the Row owner column)
- Status: not started
- Plan reference: PROJECT_PLAN.md, section 6: task 1.3 (Person 1 rows), 3.5 and 3.6 (Person 3 rows), 4.6 (Person 4 row), and the Person 2 deliverables (ILP row)

## Complexity table

| Solver | Row owner | Time (best/worst) | Space | Derivation |
|---|---|---|---|---|
| approx_matching | P1 | Θ(E) best and worst | O(V) extra | One pass over the edges, constant work per edge; see below |
| greedy_degree | P1 | best Θ(V+E), worst Θ(V²) | O(V+E) | Up to min(V,E) rounds, each rescanning all vertices; see below |
| exact_branch_and_bound | P3 | TODO | TODO | TODO |
| ilp | P2 | polynomial when the LP relaxation is integral (e.g. bipartite graphs); exponential in V in the worst case | O(V+E) for the model | NP-hard problem solved by LP-based branch-and-bound; see below |
| min_cut (Edmonds-Karp) | P4 | TODO | TODO | TODO |
| local_search | P3 | TODO | TODO | TODO |

## Derivations

### approx_matching

The code is one `for` loop over the edges. For each edge it tests `u not in cover and v not in cover` (two set lookups, constant time on average) and at most adds two vertices (constant time). There is no early exit and no work that depends on what happened before, so the loop costs Θ(E) in the best case and in the worst case alike.

Space: besides the input, only the set `cover` is stored. It holds two vertices per matched edge, and matched edges share no vertices, so it has at most V vertices: O(V).

(A set iterates in some fixed internal order; the bound does not depend on that order. Only the *quality* of the answer does, see `docs/approximation_proof.md`.)

### greedy_degree

1. `adjacency(edges)` visits every edge once and builds one neighbour set per vertex: Θ(V+E) time and space.
2. The `while` loop. Each round picks a vertex with at least one remaining neighbour, adds it to the cover and empties its neighbour set. So every round removes at least one edge, and the chosen vertex never has links again: the loop runs at most min(V, E) times.
3. Cost of one round. `any(adj[v] for v in adj)` may scan all V vertices (it stops at the first non-empty set, but many sets can be empty already), and `max(adj, key=...)` always scans all V vertices. The inner `for u in adj[v]` costs the degree of v, and over the whole run each edge is removed once, so all inner loops together cost O(E). So a round costs Θ(V) for the scans.
4. Total: Θ(V+E) for step 1, plus up to min(V,E) rounds of Θ(V) for step 3, plus O(E) for the inner loops.

Best case: a star (one hub): a single round, so Θ(V+E). Worst case: V/2 separate links (a perfect matching). Every round removes just one link, so V/2 rounds each rescan about V vertices: Θ(V²). In general O(V·min(V,E) + E), which is O(V²).

Space: the adjacency structure is Θ(V+E); the cover adds at most V.

### exact_branch_and_bound

### ilp

The model (`ilp` in `sensorplace/vertex_cover.py`, written out for all three problems in `sensorplace/ilp_models.py`) has V binary variables and one constraint per edge (E constraints), so building it costs Θ(V+E) time and space. Solving it is the expensive part: the solver (PuLP with CBC) works by branch-and-bound on the LP relaxation, where each x_v is allowed to be any number between 0 and 1.

- **Best case, polynomial:** if the LP optimum already has every x_v equal to 0 or 1, no branching is needed and the cost is that of solving one linear program, which is polynomial. This is guaranteed for bipartite graphs, where the constraint matrix is totally unimodular. For any graph, the LP optimum can be taken with every x_v in {0, 1/2, 1}; the fractional vertices are what force branching.
- **Worst case, exponential:** vertex cover is NP-hard (`docs/np_completeness.md`), so no polynomial worst-case bound is known for any exact method, and for the ILP the search tree can have up to 2^V leaves, one per 0/1 assignment. In practice the LP bounds prune most of the tree, which is why the running time on real instances is an experimental question (`figures/ilp_runtime.png`).
- **Weights do not change this.** `cost=` only changes the objective, so the weighted problem has the same constraints and the same complexity class. That is why the ILP adapts to prices with no extra work, while the backtracking solver's pruning rules assume every machine costs the same.

Space: the model is Θ(V+E); the memory used by the branch-and-bound tree is not bounded by this and depends on the solver.

### min_cut (Edmonds-Karp)

### local_search

## Timing check on growing n

For `approx_matching` and `greedy_degree`, produced by `python -m experiments.complexity_timing` (graphs made of n/2 separate links, the worst case for `greedy_degree`; best of 3 runs; the absolute times are specific to the machine, the ratios are what matters). If a function is linear, doubling n should roughly double the time; if quadratic, roughly quadruple it.

| n | approx_matching | greedy_degree |
|---|---|---|
| 2000 | 0.08 ms | 129 ms |
| 4000 | 0.16 ms (x2.1) | 533 ms (x4.1) |
| 8000 | 0.46 ms (x2.9) | 2229 ms (x4.2) |
| 16000 | 0.78 ms (x1.7) | 9151 ms (x4.1) |

`greedy_degree` quadruples at every doubling, as the derivation Θ(V²) predicts. `approx_matching` stays near doubling (the individual ratios are noisy because the times are below a millisecond), as expected for Θ(E).
