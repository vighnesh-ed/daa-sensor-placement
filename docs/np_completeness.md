# NP-Completeness of Vertex Cover

- Owner: Person 2
- Status: draft
- Plan reference: PROJECT_PLAN.md, section 6 (Person 2), task 2.1 (write the NP-completeness argument)

Notation: G = (V, E) is a graph, n = |V|. A *vertex cover* is a set of vertices touching every edge, an *independent set* is a set of vertices with no edge between any two of them, and a *clique* is a set of vertices with an edge between every two of them. The complement graph Ḡ has the same vertices as G and an edge exactly where G has none (written `complement_edges` in `sensorplace/ilp_models.py`).

We work with the **decision versions**, which have yes/no answers:

- VERTEX COVER: given G and k, does G have a vertex cover of size at most k?
- CLIQUE: given G and k, does G have a clique of size at least k?
- INDEPENDENT SET: given G and k, does G have an independent set of size at least k?

(The sensor placement problem asks for the smallest k. If the yes/no question is hard, the optimisation question is at least as hard.)

## (a) Vertex Cover is in NP

A problem is in NP if a "yes" answer comes with a short proof that can be checked quickly.

- **Certificate:** a proposed cover S, that is, a list of at most k vertices.
- **Verifier:** check that |S| <= k, then go through the edges once and check that each edge (u, v) has u in S or v in S. With S stored as a set each membership test takes constant time, so the check takes O(|E|) time, which is polynomial.

If a cover of size k exists, the certificate is that cover. If none exists, no certificate passes. So VERTEX COVER is in NP. (This is the same check as `is_cover` in `sensorplace/graphs.py`.)

## (b) The reduction: Clique <=p Vertex Cover

**What a reduction is.** To show that VERTEX COVER is at least as hard as CLIQUE, we give a procedure that turns any CLIQUE question into a VERTEX COVER question with the same yes/no answer, in polynomial time. Then a fast VERTEX COVER algorithm would answer CLIQUE questions just as fast.

**The construction.** Given a CLIQUE instance (G, k), output the VERTEX COVER instance (Ḡ, n - k). Building Ḡ means looking at every pair of vertices once: O(n^2) time, polynomial.

**Claim.** G has a clique of size k if and only if Ḡ has a vertex cover of size n - k.

**(⇒) a clique gives a cover.** Let C be a clique in G with |C| = k. We show that S = V \ C, which has n - k vertices, is a vertex cover of Ḡ. Take any edge (u, v) of Ḡ. By definition of Ḡ, u and v are *not* adjacent in G. If both were in C, they would be adjacent in G, because C is a clique. So at least one of them is outside C, that is, in S. Every edge of Ḡ is covered.

**(⇐) a cover gives a clique.** Let S be a vertex cover of Ḡ with |S| = n - k. We show that C = V \ S, which has k vertices, is a clique in G. Take two different vertices u, v in C. Suppose they were not adjacent in G. Then (u, v) is an edge of Ḡ, so S must contain u or v. But u and v are both in C = V \ S, a contradiction. So u and v are adjacent in G, which means C is a clique.

(If the cover has fewer than n - k vertices, we can add arbitrary vertices to reach exactly n - k, and covers stay covers. This is why "size at most" in VERTEX COVER matches "size at least" in CLIQUE.)

**Worked example.** Let G have vertices 1 to 5 and edges 12, 13, 23, 34, 45. Vertices 1, 2, 3 form a triangle, and 3-4-5 is a path hanging off it. The largest clique is {1, 2, 3}, so k = 3 is a "yes".

    G:  1 --- 2           complement:  1 ... 4     (edges 14, 15, 24, 25, 35)
         \   /                         1 ... 5
          \ /                          2 ... 4
           3 --- 4 --- 5               2 ... 5
                                       3 ... 5

The complement has the 5 edges 14, 15, 24, 25, 35 (the pairs G does not have). We need a cover of size n - k = 5 - 3 = 2. Take S = V \ {1, 2, 3} = {4, 5}: vertex 4 touches 14 and 24, vertex 5 touches 15, 25 and 35, so every edge is covered. No single vertex covers all five edges (vertex 1 misses 24, 25 and 35, and so on), so the smallest cover of Ḡ has size 2 and the largest clique of G has size 5 - 2 = 3, as it should. (Computed and checked by the code in `sensorplace/ilp_models.py`.)

**Conclusion.** CLIQUE <=p VERTEX COVER. Since CLIQUE is NP-complete (part (d)) and VERTEX COVER is in NP (part (a)), VERTEX COVER is NP-complete.

## (c) The chain: Clique, Independent Set, Vertex Cover

The three problems are three views of one problem, and each reduces to the others.

    3-SAT  ->  CLIQUE  <->  INDEPENDENT SET  <->  VERTEX COVER

    (each arrow is a polynomial-time reduction; the double arrows
     can be followed in both directions, as shown below)

- **Vertex cover <-> independent set (same graph).** S is a vertex cover of G if and only if V \ S is an independent set of G. Proof: S covers every edge, exactly when no edge has both endpoints outside S, exactly when V \ S contains no edge. So G has an independent set of size k if and only if it has a vertex cover of size n - k, and at the optimum

      |minimum vertex cover| + |maximum independent set| = n.

- **Clique <-> independent set (complement graph).** A set is a clique in G if and only if it is an independent set in Ḡ, because "every pair is adjacent in G" is the same as "no pair is adjacent in Ḡ".
- Putting the two together gives the reduction in (b): clique in G, independent set in Ḡ, vertex cover in Ḡ (the complement of that independent set).

Because every arrow can be reversed, all three problems are equally hard: if one has a fast algorithm, so do the other two.

**The same fact as three ILP models** (`sensorplace/ilp_models.py`). Each machine gets a 0/1 variable x_v ("chosen"):

| Problem | Objective | Constraint |
|---|---|---|
| Vertex cover | minimise sum of cost_v * x_v | x_u + x_v >= 1 for every **edge** (one end must be chosen) |
| Independent set | maximise sum of x_v | x_u + x_v <= 1 for every **edge** (not both ends) |
| Clique | maximise sum of x_v | x_u + x_v <= 1 for every **non-edge** (a pair that is not linked cannot both be chosen) |

The tests in `tests/test_ilp_models.py` check on random graphs that |cover| + |independent set| = n, that clique size in G equals independent set size in Ḡ, and that all three agree with brute force.

## (d) Cook-Levin and 3-SAT

The chain has to start somewhere. The **Cook-Levin theorem** says that SAT (given a Boolean formula, can its variables be set to true/false to make it true?) is NP-complete: every problem in NP can be turned, in polynomial time, into a SAT question with the same answer. The idea is that "this verifier accepts this certificate" can itself be written as a Boolean formula. We do not prove it here.

From SAT one reduces to **3-SAT** (formulas whose clauses have exactly three literals), and 3-SAT <=p CLIQUE: build one vertex per literal occurrence in each clause, join two vertices when they are in different clauses and do not contradict each other, and the formula with m clauses is satisfiable if and only if the graph has a clique of size m (this is the reduction in CLRS section 34.5.1, which we cite but do not repeat). Then CLIQUE <=p VERTEX COVER from (b) finishes the chain:

    SAT -> 3-SAT -> CLIQUE -> INDEPENDENT SET -> VERTEX COVER

What it implies: if anyone finds a polynomial-time algorithm for VERTEX COVER (or for any problem in the chain), then every problem in NP has one, and P = NP. Nobody has managed this, and most researchers believe P is different from NP.

## (e) What it means for us

- There is **no known algorithm** that finds the smallest sensor set quickly on every network, and finding one would settle P versus NP. So we cannot expect an exact method that is fast on all networks.
- That is why the project compares four strategies instead of one: a 2-approximation (fast, guaranteed within a factor of 2), greedy (fast, no guarantee), exact branch-and-bound (optimal, but exponential in the worst case) and an ILP solver (optimal, flexible, also exponential in the worst case).
- NP-completeness is a statement about the **worst case** over all graphs. It does not say that every network is hard, and which real networks are easy is an experimental question. Our benchmark measures this, and we do not quote results here before it has run.
- The contrast with attacker isolation is the point of the project: minimum cut is solvable in polynomial time (Edmonds-Karp), while minimum vertex cover is NP-complete, even though both are questions about small sets of vertices or links in the same graph.
