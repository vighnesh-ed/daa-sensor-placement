# Project Plan: Optimal Security Sensor Placement in Computer Networks

**Course:** Design and Analysis of Algorithms (DAA)  **Team size:** 4  **Duration:** 4 weeks

Fill in names: **Person 1:** ________  **Person 2:** ________  **Person 3:** ________  **Person 4:** ________

---

## 0. How to use this document

1. Read sections 1 to 4 together as a team (20 minutes). Everyone needs the same picture.
2. Then go straight to **your own person section** (section 6) and follow it top to bottom.
3. Every task has a **Done when** line. If you can't tick it, the task isn't finished.
4. Time estimates are rough. If a task takes more than double the estimate, tell the team that day rather than struggling silently.

---

## 1. The project in five minutes

### The real-world problem

A company network has machines (servers, laptops, routers) connected by links. Attackers move along links. A **sensor** (an intrusion-detection tool) installed on a machine sees all traffic on every link attached to that machine. Sensors cost money, so we want **as few sensors as possible while still watching every link**.

Second question: if one machine is compromised, what is the **cheapest set of links to cut** so the attacker can no longer reach the crown-jewel server (e.g. the database)?

### The same problems in algorithm language

| Real world | Algorithm problem | Hardness |
|---|---|---|
| Fewest sensors that watch every link | **Minimum Vertex Cover** on a graph | NP-hard (no known fast exact algorithm) |
| Cheapest links to cut to isolate an attacker | **Minimum Cut** = **Maximum Flow** | Polynomial (fast and exact) |

**The story of our project:** the first problem is hard, so we try four different strategies (a fast approximation with a guarantee, a greedy heuristic, an exact search, and an ILP solver), compare them with real experiments, and contrast them with the second problem, which is easy. That contrast is the whole point.

### Glossary (read once, refer back)

- **Graph G = (V, E):** V = vertices (machines), E = edges (links).
- **Vertex cover:** a set of vertices such that every edge has at least one endpoint in the set. Our "sensor set".
- **Optimal (OPT):** the smallest possible vertex cover size.
- **Approximation ratio:** (size of our answer) / OPT. A ratio of 1.0 is perfect; 2.0 means we used twice as many sensors as necessary.
- **Matching:** a set of edges that share no vertices. **Maximal matching:** one you can't add another edge to.
- **Independent set:** vertices with no edge between any two of them. **Clique:** vertices where every pair is connected.
- **NP-hard / NP-complete:** "at least as hard as every problem in NP"; no polynomial-time algorithm is known, and finding one would prove P = NP.
- **ILP (Integer Linear Program):** minimise a linear function of variables that must be whole numbers, subject to linear constraints. Off-the-shelf solvers handle these.
- **Flow network, max-flow, min-cut:** a graph with capacities; max-flow is the most "stuff" you can push from a source s to a target t; min-cut is the cheapest set of edges whose removal separates s from t. The two numbers are always equal (Max-Flow Min-Cut theorem).

### What already exists (starter code)

A working starter codebase is already in this repository, with all solvers and 57 passing tests:

```
sensorplace/graphs.py        graph generators (hub-heavy, random, grid) + is_cover() checker
sensorplace/vertex_cover.py  approx_matching, greedy_degree, exact_branch_and_bound, ilp
sensorplace/mincut.py        Edmonds-Karp min_cut
tests/test_correctness.py    checks solvers against brute force / NetworkX
experiments/benchmark.py     runs all solvers on all graph families -> results.csv
```

**You are not starting from zero.** Your job is to understand it, prove things about it, extend it, measure it, and explain it. A graph in this codebase is just a Python `set` of edges `(u, v)` with `u < v`.

Why the work is mostly **understanding + experiments + proofs + report**: that is what the course marks. Do not spend the 4 weeks on a fancy interface.

---

## 2. Roles at a glance

Work is split so each person owns **one syllabus area, one set of code files, one experiment, and one report chapter**. Estimated effort is about 20 to 25 hours each over 4 weeks.

| | Area | You own (files) | Main experiment | Syllabus |
|---|---|---|---|---|
| **Person 1** | Approximation and greedy | `docs/approximation_proof.md`, `docs/complexity.md`, `experiments/greedy_counterexample.py`, `experiments/approx_ratio.py` | Approximation ratio vs graph size | Unit I, IV, VI |
| **Person 2** | NP-completeness and ILP | `docs/np_completeness.md`, `sensorplace/ilp_models.py`, `tests/test_ilp_models.py`, `experiments/weighted.py` | Weighted sensor costs | Unit VI, practical 9 |
| **Person 3** | Exact search and local search | `sensorplace/vertex_cover.py` (the only editor), `sensorplace/local_search.py`, `experiments/pruning_ablation.py`, `experiments/wall.py`, `docs/exact_search.md` | Where exact search breaks | Unit IV |
| **Person 4** | Network flow, scenario, visualisation | `sensorplace/mincut.py`, `sensorplace/scenario.py`, `sensorplace/viz.py`, `experiments/scenario_demo.py`, `docs/flow.md`, report assembly, demo | Attacker isolation on a realistic network | Unit V |

**Shared:** the benchmark run (Person 1 runs it, everyone uses the result), the report (each person writes a chapter), and the viva (everyone must answer questions about everything).

---

## 3. Team rules

1. **File ownership.** Only the owner edits a file. This avoids merge conflicts. If you need a change in someone else's file, message them.
2. **One shared repo on GitHub.** Everyone clones it. Commit small and often. Pull before you start working each day.
3. **No code without a test.** If you add a function, add a test that proves it works (valid output, or equal to brute force on small graphs). Run `pytest -q` before every commit; it must pass.
4. **Results come from code.** Every number in the report must come from a script you can re-run. Never type numbers by hand.
5. **Explain everything.** At the end of week 1, and again in week 3, each person teaches their area to the other three for 15 to 20 minutes. The viva will ask any of you about any part.
6. **Ask early.** Stuck for more than 45 minutes on one thing means ask the team or ask Claude.

---

## 4. Timeline

| Week | Everyone | Person 1 | Person 2 | Person 3 | Person 4 |
|---|---|---|---|---|---|
| **1: Learn** | Setup (section 5), study your area, 20-min teach-in at end of week | Study CLRS 35.1; draft proof | Study CLRS 34.5; draft reduction | Study KT 10.1; hand-trace the search | Study CLRS 26; hand-run Edmonds-Karp |
| **2: Build** | Benchmark Day (Person 1 runs on day 1, commits `results.csv`) | Greedy counterexample; ratio plot | ILP models for VC / IS / clique + tests | Instrument solver; pruning ablation; wall experiment | Scenario network; scenario demo |
| **3: Extend and write** | Write your own report chapter; second teach-in | Complexity table; findings paragraph | Weighted experiment | Local-search solver | Visualisation; disjoint-paths experiment |
| **4: Finish** | Report assembly, demo rehearsal, mock viva, buffer | Review all proofs | Review report | Review code | Assemble report; demo script |

**Rule for week 4:** no new features. Only fixes, polish, and rehearsal.

---

## 5. Everyone: week 1 setup checklist (about 1.5 hours)

- [ ] One person creates a GitHub repo and pushes this project; everyone else clones it.
- [ ] Everyone installs: `pip install -r requirements.txt`.
- [ ] Everyone runs `pytest -q` and sees all tests pass.
- [ ] Everyone reads `sensorplace/graphs.py` and `sensorplace/vertex_cover.py` (about 150 lines) and writes down **three lines they don't understand**; bring those to the first team meeting.
- [ ] Everyone runs this in a Python shell and looks at the output:

```python
from sensorplace import *
E = preferential_attachment(30, seed=1)
print(len(E), "links")
for f in (approx_matching, greedy_degree, ilp):
    print(f.__name__, len(f(E)))
print(min_cut(E, 0, 29))
```

- [ ] Agree on a meeting time: two 30-minute check-ins per week.

---

## 6. Person sections

---

### PERSON 1: Approximation and Greedy

**Your question to answer:** *Why does an algorithm with a proven guarantee (2-approximation) perform worse in practice than a simple greedy heuristic with no guarantee?*

#### Study first (about 5 hours, in this order)

1. Vertex cover from scratch: re-read section 1 above, then draw 3 small graphs on paper and find their minimum vertex cover by hand.
2. **CLRS 35.1** "The vertex-cover problem". Read the whole section; it is the proof you will write.
3. Understand the words: *approximation ratio*, *maximal matching*, *lower bound on OPT*.
4. Read `approx_matching` and `greedy_degree` in `vertex_cover.py` line by line.

#### Tasks

**1.1 Write the 2-approximation proof** in `docs/approximation_proof.md` (about 2 hours)

Structure it exactly like this:
- The algorithm in 3 lines.
- **Lemma 1:** the output is a valid vertex cover. *(Hint: suppose some edge is uncovered; then it could be added to the matching, contradicting maximality.)*
- **Lemma 2:** OPT is at least |M|, where M is the matching. *(Hint: matched edges share no vertices, so any cover needs a different vertex for each.)*
- **Theorem:** the output has size 2|M| ≤ 2·OPT.
- A **tight example** showing the ratio of 2 really happens: the path `a-b-c-d` with edges processed in the order (a,b), (b,c), (c,d) gives 4 vertices, but OPT is 2 ({b, c}). Note this depends on edge order; explain why.

*Done when:* a teammate who has not read CLRS can follow every step without asking you.

**1.2 Greedy: find where it fails** (about 3 hours)

Create `experiments/greedy_counterexample.py`:
- Generate many small random graphs (6 to 11 vertices, `erdos_renyi`).
- For each, compute the true optimum by **brute force** (try all subsets) and compare with `greedy_degree`.
- Print and draw the **smallest graph** where greedy is worse than optimal.
- **Careful:** greedy has ties (several vertices with the same degree). A counterexample that only fails because of an unlucky tie-break is weak. Make sure yours fails **even with the best tie-breaking**. (We checked: examples with about 8 vertices and 6 edges exist where greedy uses 4 sensors but OPT is 3. Your search should find one in seconds.)
- *Stretch goal:* look up the known bipartite construction where greedy's ratio grows like log n (search "greedy vertex cover logarithmic lower bound", Papadimitriou and Steiglitz). Implement it and show the ratio growing with n.

*Done when:* the script prints one concrete counterexample with sizes, and you can explain on paper why greedy picks wrong.

**1.3 Complexity table** `docs/complexity.md` (about 1.5 hours)

Create a table with one row per solver: time complexity, space complexity, best / worst case. **You write the rows for `approx_matching` and `greedy_degree`**; the other three people add their own rows later (ILP: Person 2, exact search: Person 3, Edmonds-Karp: Person 4). Derive yours from the code by counting loops, don't copy.

Hints: `approx_matching` is one pass over the edges. For `greedy_degree`, look at what happens inside the `while` loop (the `any(...)` check and the `max(...)`); how many times can it run, and what does each run cost? Verify your answer with a quick timing experiment on growing n.

*Done when:* both rows have a derivation of a few lines each, not just a final Big-O.

**1.4 Run the benchmark, make the ratio plot** (about 4 hours)

- On **Benchmark Day** (first day of week 2), run `python -m experiments.benchmark` and commit `results.csv`. It takes several minutes. If it's too slow, reduce `SIZES` in `benchmark.py` (you may edit that file) and say so in the report.
- Write `experiments/approx_ratio.py`: read `results.csv` and produce `figures/approx_ratio.png`: x-axis n, y-axis ratio (algorithm size ÷ optimal size), one line per algorithm, one panel per graph family, with a horizontal line at ratio = 2.

*Done when:* the plot has both algorithms in all three families, and the guarantee line at 2 is visible.

**1.5 Findings paragraph** (about 1 hour)

Write a paragraph in your own words, backed by the plot, that answers your question at the top. Do not guess; use the numbers. (Our early experiments suggest greedy is within a few percent of optimal on hub-heavy graphs while the 2-approximation is roughly 60% worse on average. Check whether your full results agree on all three families, and say honestly where they don't.)

#### Your deliverables

`docs/approximation_proof.md`, `experiments/greedy_counterexample.py`, `experiments/approx_ratio.py`, `figures/approx_ratio.png`, `docs/complexity.md` (table owner), report chapter 3.1 and 5.1.

#### Be ready to answer in the viva

1. Prove the 2-approximation guarantee. Why does the algorithm take both endpoints?
2. Is the ratio of 2 tight? Show an example.
3. Why can greedy be bad even though it looks smart?
4. If greedy beats the 2-approximation in our experiments, why would anyone use the 2-approximation?

---

### PERSON 2: NP-completeness and ILP

**Your question to answer:** *Why is this problem hard, and what is the most flexible tool for solving it exactly (including with different costs per machine)?*

#### Study first (about 6 hours, in this order)

1. **What NP, NP-hard, NP-complete mean:** CLRS 34.1 to 34.3 (skim; read the definitions carefully). Understand what a **polynomial-time reduction** is: converting an instance of problem A into an instance of problem B, in polynomial time, so that the answers match.
2. **CLRS 34.5.1 (Clique) and 34.5.2 (Vertex cover).** This is the proof you will write up.
3. **ILP basics:** read the PuLP documentation's introductory example (search "PuLP blending problem"), then read `ilp()` in `vertex_cover.py`; it is only about 10 lines.
4. Know the three relationships (draw them on paper):
   - S is a vertex cover **if and only if** V \ S is an independent set.
   - A clique in G is an independent set in the **complement** graph (the graph with edges where G has none, and none where it has).
   - So at the optimum: **|min vertex cover| + |max independent set| = |V|**.

#### Tasks

**2.1 Write the NP-completeness argument** in `docs/np_completeness.md` (about 3.5 hours)

Cover, in this order:
- **(a) Vertex Cover is in NP.** Say what the certificate is (a proposed cover) and how fast it can be checked (one pass over the edges).
- **(b) The reduction Clique ≤p Vertex Cover.** Given G and k, build the complement graph Ḡ. Claim: G has a clique of size k **iff** Ḡ has a vertex cover of size |V| − k. Prove **both directions** (CLRS does this; rewrite it in your own words, with a small worked example such as a 5-vertex graph).
- **(c) The chain:** Clique, Independent Set, Vertex Cover are all NP-complete and reduce to each other; draw the picture.
- **(d) One paragraph on Cook-Levin and 3-SAT:** where this chain starts (CLRS shows 3-SAT ≤p Clique). You do not need to prove Cook-Levin, only state it and say what it implies.
- **(e) What it means for us:** why we can't hope for a fast exact algorithm for all networks.

*Done when:* you can draw the reduction for a small graph on a whiteboard without notes.

**2.2 Write ILP models for the three NP-complete problems** `sensorplace/ilp_models.py` (about 3 hours). This is **practical 9** in the syllabus.

Implement three functions (reuse `ilp()` from `vertex_cover.py` for the first). Pass the vertex list explicitly as `nodes` so isolated vertices are counted:

| Problem | Variables | Objective | Constraints |
|---|---|---|---|
| Vertex cover | x_v ∈ {0,1} | minimise Σ cost_v · x_v | x_u + x_v ≥ 1 for every **edge** |
| Independent set | x_v ∈ {0,1} | maximise Σ x_v | x_u + x_v ≤ 1 for every **edge** |
| Clique | x_v ∈ {0,1} | maximise Σ x_v | x_u + x_v ≤ 1 for every **non-edge** (pair of vertices *not* connected) |

*Done when:* all three functions return a vertex set, and you can explain in one sentence why each constraint is written the way it is.

**2.3 Test them** `tests/test_ilp_models.py` (about 2 hours)

Check:
- For many random small graphs: `|vertex_cover| + |independent_set| == |V|`.
- Clique size of G equals independent set size of the complement graph.
- All three agree with **brute force** on graphs of at most 11 vertices.
- Clique matches `networkx.algorithms.clique.max_weight_clique(G, weight=None)`.

*Done when:* the tests pass on at least 15 random graphs, and one test per relationship exists.

**2.4 Weighted sensor-cost experiment** `experiments/weighted.py` (about 3 hours)

In real networks some machines are costlier to instrument (e.g. core servers cost 5, workstations cost 1). Compare, on hub-heavy and random graphs:
- (a) the **unweighted** optimum, then compute its **total cost** under the costs;
- (b) the **weighted ILP** optimum (`cost=` argument);
- (c) a **weighted greedy**: repeatedly pick the vertex with the highest (uncovered links) ÷ cost.

Report how much cheaper (b) is than (a). *Done when:* a table of the three total costs over several graphs exists and a one-sentence conclusion is written.

**2.5 ILP running-time plot** (about 1.5 hours)

From `results.csv` (column `ilp_s`), plot ILP time vs n for each family. Answer: does ILP scale better or worse than the exact search (Person 3's experiment)? *Done when:* the plot exists.

**2.6 Stretch (only if everything else is done):** LP relaxation. Solve the same ILP but with continuous variables 0 ≤ x_v ≤ 1. For vertex cover, optimal basic solutions use only 0, ½, and 1; rounding every x_v ≥ ½ up to 1 gives another 2-approximation (Kleinberg-Tardos 11.6). Compare it with `approx_matching`.

#### Your deliverables

`docs/np_completeness.md`, `sensorplace/ilp_models.py`, `tests/test_ilp_models.py`, `experiments/weighted.py`, ILP runtime plot, your row(s) in `docs/complexity.md`, report chapter 2 and 5.2.

#### Be ready to answer in the viva

1. What does it mean that Vertex Cover is NP-complete? What's the reduction you showed?
2. What is the relationship between vertex cover, independent set, and clique?
3. Write the ILP for vertex cover. Why is "≥ 1" correct? Why do we change it to "≤ 1" for independent set?
4. What does the weighted version change, and why is ILP easier to adapt than the backtracking solver?

---

### PERSON 3: Exact Search and Local Search

**Your question to answer:** *How far can exact search go before it breaks, and what makes it fast?*

#### Study first (about 5 hours, in this order)

1. **Backtracking and branch-and-bound** in general: the idea of a search tree, where each node is a decision, and *pruning* means cutting off branches that can't lead to a better answer.
2. **Kleinberg-Tardos section 10.1 "Finding small vertex covers"**: it explains exactly the branching used in our solver ("either v is in the cover, or all its neighbours are").
3. Read `exact_branch_and_bound` in `vertex_cover.py` slowly. It has three ideas:
   - **Branching:** pick the highest-degree vertex v. Branch 1: v is in the cover. Branch 2: v is not, so **all** its neighbours must be.
   - **Degree-1 rule:** if a vertex has exactly one neighbour, putting that neighbour in the cover is never worse. Apply repeatedly.
   - **Lower bound:** at least ⌈(edges left) ÷ (max degree)⌉ more vertices are needed; if that already can't beat the best known solution, stop.

#### Tasks

**3.1 Hand-trace the search tree** `docs/exact_search.md` (about 2 hours)

On paper, take a 6-vertex graph of your choice (a triangle with a few attached edges is fine) and draw the search tree the solver explores: label each branch ("v in cover" / "v out, neighbours in"), mark where the degree-1 rule fires and where the lower bound prunes. Photograph or redraw the diagram into the doc and explain it in a short paragraph.

*Done when:* you can explain each branch and each pruned node to a teammate.

**3.2 Instrument the solver** (about 2 hours)

You are the **only person who edits `vertex_cover.py`**. Add to `exact_branch_and_bound`:
- an optional `stats=None` dictionary parameter that counts the number of search nodes visited;
- two flags `use_degree1=True` and `use_bound=True` to switch the two pruning rules off.

Default behaviour must not change. *Done when:* `pytest -q` still passes and calling with `stats={}` fills in a node count.

**3.3 Pruning ablation experiment** `experiments/pruning_ablation.py` (about 3 hours)

On random graphs (e.g. n = 20, 30, 40, 50; average degree about 4), run the solver four ways: no pruning, degree-1 only, bound only, both. Record the **search nodes visited** (not just time). Produce a table and a bar chart. Use a time limit so "no pruning" doesn't run forever.

*Done when:* the chart shows how many times fewer nodes each rule saves and you can explain why.

**3.4 "Where does it break?" experiment** `experiments/wall.py` (about 3 hours)

For random graphs with average degree 8, run the exact solver for n = 20, 40, 60, 80, 100, 120, 160 and record the time (use `time_limit=10` and note any timeouts). Do the same for hub-heavy graphs. Produce a **log-scale** plot of time vs n for both families. Answer: at what n does it exceed 5 seconds? How does time grow per +10 vertices?

*Done when:* the plot shows two lines and a sentence states the "wall" for each family. (Early results show hub-heavy graphs stay fast even at 300+ vertices while random graphs hit the wall around 160. Verify it yourself.)

**3.5 Local-search solver** `sensorplace/local_search.py` (about 4 hours)

A fifth solver that improves a good solution:
1. Start from the greedy cover.
2. **Remove redundant vertices:** a cover vertex whose neighbours are all in the cover can be removed.
3. **Swap move:** try removing two cover vertices and adding one outside vertex; keep it if the result is still a cover.
4. Repeat until no move helps.

Add tests: output is always a valid cover and never larger than the starting cover. Compare its size with greedy and with the optimal on the benchmark graphs.

*Done when:* a small table (greedy vs local search vs optimal) exists and tests pass.

**3.6 Complexity row** in `docs/complexity.md` for the exact solver: worst case exponential; explain why in a few lines (the search tree can have up to about 2^V leaves) and why pruning doesn't change the worst case but helps in practice.

#### Your deliverables

`vertex_cover.py` changes, `sensorplace/local_search.py` + tests, `experiments/pruning_ablation.py`, `experiments/wall.py` and plots, `docs/exact_search.md`, report chapter 3.2 and 5.3.

#### Be ready to answer in the viva

1. Explain the branching: why is "v out of the cover" the same as "all neighbours of v in"?
2. What does the degree-1 rule do and why is it safe?
3. Why does exact search work great on some graphs and not others?
4. Is local search guaranteed to be optimal? Why or why not?

---

### PERSON 4: Network Flow, Scenario, Visualisation, Integration

**Your question to answer:** *When a machine is compromised, what is the cheapest way to cut it off, and how does this "easy" problem compare to the "hard" sensor-placement one?*

#### Study first (about 6 hours, in this order)

1. **Flow networks, residual graphs, augmenting paths:** CLRS 26.1 to 26.2. Draw a small example on paper before reading any code.
2. **Ford-Fulkerson and Edmonds-Karp (CLRS 26.2 to 26.3):** Edmonds-Karp is Ford-Fulkerson using **BFS** to find the shortest augmenting path, which gives a guaranteed time bound of O(V·E²).
3. **Max-Flow Min-Cut theorem** (CLRS 26.2): the value of the max flow equals the capacity of the min cut.
4. **Menger's theorem idea (Kleinberg-Tardos 7.6):** with every link given capacity 1, the max flow from s to t equals the **number of edge-disjoint paths** from s to t. This tells us "how many independent routes does the attacker have".
5. Search YouTube for "William Fiset max flow Edmonds-Karp" for a visual walk-through.
6. Read `mincut.py` line by line.

#### Tasks

**4.1 Hand-run Edmonds-Karp** `docs/flow.md` (about 2.5 hours)

Pick a flow network with 6 nodes and about 8 edges with capacities. On paper, run Edmonds-Karp step by step: draw the residual graph after each augmentation, write the bottleneck, and at the end identify the min cut (the vertices still reachable from s in the final residual graph). Put the diagrams and explanation in `docs/flow.md` and show that the cut capacity equals the flow value.

*Done when:* you can explain what a residual edge is, and why the flow can "undo" earlier decisions.

**4.2 Build a realistic labelled network** `sensorplace/scenario.py` (about 3 hours)

Write a function `build_campus_network()` returning named nodes and links that look like a real network, e.g.: `internet` → 2 `firewall`s → 3 `switch`es → about 15 `workstation`s and 3 `server`s (one named `database`). Give each link a **cut cost** (e.g. firewall links expensive to cut, workstation links cheap). Convert names to integers inside (the algorithms use integer vertices) and keep a dict to convert back.

*Done when:* the function returns edges, a name map, and capacities, and prints a readable summary.

**4.3 Scenario demo** `experiments/scenario_demo.py` (about 3 hours)

On your campus network, run and print:
1. All four vertex-cover solvers, with **named** machines that receive sensors (e.g. "sensors go on: switch-1, firewall-2, ...").
2. `min_cut(edges, compromised_workstation, database, capacities)` and the **named links to cut** and their total cost.
3. The **number of edge-disjoint attack paths** from the workstation to the database (run `min_cut` with all capacities equal to 1 and read the flow value).

*Done when:* running the script prints a clear story a non-technical person could follow.

**4.4 Visualisation** `sensorplace/viz.py` (about 3 hours)

Write `draw(edges, sensors=None, cut=None, labels=None, path="figure.png")` using NetworkX and Matplotlib. Sensors in red, other machines in blue, cut links as dashed red lines; use a fixed `spring_layout(seed=...)` so the picture is reproducible. Produce two figures for the report: (i) sensor placement on the campus network, (ii) the min cut.

*Done when:* both PNG files exist and are readable at report size.

**4.5 Extra tests** (about 1 hour)

Add a test that the disjoint-paths count from `min_cut` with unit capacities matches `networkx.edge_disjoint_paths` on several random graphs.

**4.6 Report assembly and demo** (about 3 hours, mostly in weeks 3 and 4)

You are the integrator: keep the README status checklist up to date, collect each person's chapter, make the report consistent (same notation, same figure style), write the introduction (chapter 1) and conclusion (chapter 6), and write the 10-minute demo script (see section 9). Edmonds-Karp's complexity row (O(V·E²) time, O(V+E) space; derive the reasoning) goes into `docs/complexity.md`.

#### Your deliverables

`docs/flow.md`, `sensorplace/scenario.py`, `experiments/scenario_demo.py`, `sensorplace/viz.py` and two figures, extra tests, assembled report, demo script, report chapter 4 and 1 and 6.

#### Be ready to answer in the viva

1. Explain the Max-Flow Min-Cut theorem in your own words with an example.
2. Why does Edmonds-Karp use BFS? What would go wrong with an arbitrary path choice?
3. Minimum cut is solvable in polynomial time but vertex cover isn't. What does that tell us about the two problems?
4. What does the number of edge-disjoint paths mean for the security team?

---

## 7. Shared milestones

| Milestone | When | Who | Done when |
|---|---|---|---|
| Setup complete | Week 1, day 2 | Everyone | All 4 laptops pass `pytest -q` |
| Teach-in 1 | End of week 1 | Everyone | Each person explains their study topic for 15 min |
| **Benchmark Day** | Week 2, day 1 | Person 1 runs; all use it | `results.csv` committed; everyone has looked at it |
| Experiments done | End of week 2 | Everyone | Each person's main experiment has a plot |
| Teach-in 2 | Middle of week 3 | Everyone | Each person presents their findings |
| Chapters drafted | End of week 3 | Everyone | All chapters in the shared document |
| Report assembled | Week 4, day 3 | Person 4 | One consistent document |
| Mock viva | Week 4, day 5 | Everyone | Every person has answered questions on every area |

---

## 8. Report outline and who writes what

| Chapter | Content | Writer |
|---|---|---|
| 1 | Introduction: real-world problem, objectives | Person 4 |
| 2 | Theory: problem formulation, NP-completeness, relations among VC / IS / clique | Person 2 |
| 3.1 | 2-approximation and greedy: algorithms and proofs | Person 1 |
| 3.2 | Exact search and local search | Person 3 |
| 3.3 | ILP formulation | Person 2 |
| 4 | Network flow and attacker isolation | Person 4 |
| 5.1 | Experiment: approximation ratio | Person 1 |
| 5.2 | Experiments: weighted costs, ILP running time | Person 2 |
| 5.3 | Experiments: pruning and the exact-search wall | Person 3 |
| 5.4 | Experiment: campus scenario | Person 4 |
| 6 | Conclusion and comparison of all methods | Person 4 (all review) |

Each chapter should be about 1 to 3 pages. Every figure needs a caption saying what it shows and one sentence of interpretation.

---

## 9. Demo plan (10 minutes)

1. **(1 min)** The problem: show the campus network picture. *(Person 4)*
2. **(2 min)** Four strategies, one sentence each. Show the sensor placement they produce. *(Persons 1, 3)*
3. **(2 min)** The key results: ratio plot (greedy beats the guaranteed algorithm) and the wall plot. *(Persons 1, 3)*
4. **(1 min)** Weighted costs: cheaper with ILP. *(Person 2)*
5. **(2 min)** Why it's hard (NP-completeness in one picture) vs the min-cut that's easy. *(Persons 2, 4)*
6. **(2 min)** Questions. Anyone may be asked about anything.

---

## 10. Things NOT to do

- No GUI, web app, or login system.
- No real network scanning or live traffic capture.
- No new algorithms or new problems after the end of week 3.
- No unexplained code: if you can't explain a line, don't submit it.
- Don't write the report text before you have the plots. Numbers first, then words.
- Don't change someone else's file without telling them.

---

## 11. Questions everyone must be able to answer

1. What is the problem, in one sentence, and why is it a vertex cover problem?
2. Why can't we just use the exact algorithm for every network?
3. What does a 2-approximation guarantee, and what doesn't it guarantee?
4. Which method would you actually deploy on a real network and why? (Use our results.)
5. How is min-cut different from vertex cover in difficulty, and why?
6. What was the most surprising result in our experiments?

---

## 12. Resources

- **CLRS** (Introduction to Algorithms): ch. 26 (max flow), ch. 34 (NP-completeness), ch. 35 (approximation algorithms).
- **Kleinberg and Tardos, Algorithm Design:** ch. 7 (network flow), ch. 8 (NP), ch. 10.1 (finding small vertex covers), ch. 11 (approximation, including weighted vertex cover).
- **PuLP documentation:** https://coin-or.github.io/pulp/
- **NetworkX documentation:** https://networkx.org/
- **YouTube:** search "William Fiset max flow / Edmonds-Karp" for visual flow explanations.
- **Ask Claude:** paste a specific paragraph or proof step you don't follow and ask for it to be explained with a small example; also use it to review your proof or test before you commit.