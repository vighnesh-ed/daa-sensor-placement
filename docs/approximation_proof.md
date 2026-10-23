# Approximation Proof and Greedy Counterexample

- Owner: Person 1
- Status: draft
- Plan reference: PROJECT_PLAN.md, section 6 (Person 1), tasks 1.1 (2-approximation proof) and 1.2 (greedy: find where it fails)

Notation: a graph has vertices V (machines) and edges E (links). A vertex cover C is a set of vertices such that every edge has at least one endpoint in C. OPT is the size of a smallest vertex cover. The code is `approx_matching` in `sensorplace/vertex_cover.py`.

## The algorithm in 3 lines

1. Start with an empty cover C and an empty matching M.
2. Go through the edges one by one. If neither endpoint of the edge (u, v) is in C yet, put the edge in M and put **both** u and v in C.
3. Return C.

M is a *matching* (no two edges in it share a vertex) because as soon as an edge enters M, both its endpoints enter C, and an edge touching either of them is skipped afterwards. M is *maximal* (no further edge can be added) because every edge that was skipped already had an endpoint in C, that is, it touches an edge of M.

## Lemma 1: the output is a valid vertex cover

Take any edge e = (u, v). When the algorithm reaches e, one of two things holds.

- u or v is already in C. Then e is covered, and C only ever grows, so e stays covered.
- Neither is in C. Then the algorithm adds both, so e is covered.

Either way e ends up covered, so C is a vertex cover. (Another way to say it: if some edge were uncovered at the end, it could have been added to M, which contradicts M being maximal.)

## Lemma 2: OPT is at least |M|

Let C* be any vertex cover, for example a smallest one. C* must contain at least one endpoint of every edge of M. The edges of M share no vertices, so these endpoints are all different vertices. Hence C* contains at least |M| vertices, and in particular OPT >= |M|.

This is the key trick: we cannot compute OPT (that is the hard part), but we can compute a number that OPT is never below.

## Theorem: the output has size 2|M| <= 2*OPT

Every edge added to M puts two vertices into C, and both are new (neither endpoint was in C when the edge was accepted). So |C| = 2|M|. By Lemma 2, |M| <= OPT, therefore

    |C| = 2|M| <= 2 * OPT.

So the algorithm is a 2-approximation: it never uses more than twice the optimal number of sensors, on every graph, whatever the edge order. Together with Lemma 1 the answer is always a valid cover.

## Tight example: the path a-b-c-d

Take the path a-b-c-d with edges processed in the order (a,b), (b,c), (c,d).

- (a,b): neither in C, so take both. C = {a, b}, M = {ab}.
- (b,c): b is in C, skip.
- (c,d): neither in C, so take both. C = {a, b, c, d}, M = {ab, cd}.

The output has 4 vertices, but {b, c} covers all three edges, so OPT = 2. The ratio is exactly 2, so the bound in the theorem cannot be improved for this algorithm. (Checked by the test `test_tight_example_path` in `tests/test_approximation.py`.)

## Why the tight example depends on edge order

The algorithm goes through the edges in the order it is given, so the matching it builds depends on that order. If the same path is processed in the order (b,c), (a,b), (c,d):

- (b,c): take both. C = {b, c}.
- (a,b) and (c,d): each has an endpoint in C, skip.

Now the output is {b, c}, which is optimal. So the ratio of 2 on the path is a worst case over orders, not what happens every time.

Some graphs are bad for **every** order. In the complete bipartite graph K(3,3), every maximal matching has 3 edges (each accepted edge removes one vertex from each side), so the output always has 6 vertices, while one side alone, 3 vertices, covers everything. The ratio is 2 whatever the order (checked in `test_complete_bipartite_is_tight_for_every_order`).

## Greedy counterexample: smallest graph where greedy is worse than optimal

Found by `python -m experiments.greedy_counterexample`. The search covers every graph with up to 7 vertices (NetworkX's graph atlas, so it is exhaustive), and it reports the first graph where greedy-by-degree is worse than optimal. It is a tree on 7 vertices and 6 edges:

    edges: (0,1) (0,3) (0,4) (1,2) (3,6) (4,5)

Vertex 0 is a hub with three neighbours 1, 3, 4, and each neighbour has one extra leaf (2, 6, 5).

- Optimal cover: {1, 3, 4}, 3 sensors.
- Greedy: 4 sensors, for example {0, 1, 3, 4}.

No graph with 6 or fewer vertices is a counterexample, and no 7-vertex graph with fewer than 6 edges is one. The picture is `figures/greedy_counterexample.png`.

## Why the counterexample is not a tie-break artifact

Greedy picks a vertex of maximum degree, and when several vertices tie the choice is arbitrary, so a graph where greedy only fails after an unlucky tie-break would prove nothing. The script therefore tries **every** tie-break (`best_greedy_run`) and only accepts a graph if even the best run is worse than optimal.

Here there is nothing to tie-break in the first step: vertex 0 has degree 3 and every other vertex has degree at most 2, so greedy must pick 0. After that, the three remaining edges (1,2), (3,6), (4,5) share no vertices, so they need three more sensors whatever is chosen. Greedy always ends with 4.

## Why greedy picks wrong

Degree counts how many links a vertex covers *right now*, and the hub looks like the best deal with 3 links. But those 3 links are covered anyway by the three neighbours 1, 3, 4, which we need regardless, because each of them also has a leaf edge. The hub buys nothing that is not already paid for. Greedy cannot see this because it only looks one step ahead: it measures the immediate gain of a vertex, not what the rest of the graph forces later.

## Stretch: greedy ratio grows like log n

Not done. It is a stretch goal in the plan. The project notes state the known result that greedy's worst-case ratio grows like log n, and the construction behind it (a bipartite graph where the greedy hub choices keep beating the optimal side) is not implemented here. Do not quote this as a result of our experiments.
