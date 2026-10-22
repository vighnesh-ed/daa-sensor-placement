# Optimal Security Sensor Placement in Computer Networks

**Exact, Approximation and Flow-Based Algorithms**

Group project for **Design and Analysis of Algorithms (DAA)**.

## Overview

A company network is a set of machines connected by links. A security **sensor** installed on a machine sees all traffic on every link attached to it. Sensors cost money, so the question is: **what is the fewest number of sensors that still watches every link?** A second question follows: if one machine is compromised, **which links should be cut, at minimum cost, to stop the attacker reaching a critical server?**

Both questions are modelled on a graph, where machines are vertices and links are edges:

| Real-world problem | Algorithm problem | Difficulty |
|---|---|---|
| Fewest sensors that watch every link | Minimum Vertex Cover | NP-hard |
| Cheapest links to cut to isolate an attacker | Minimum Cut / Maximum Flow | Polynomial |

The project implements several strategies for the hard problem, compares them experimentally, and contrasts them with the easy one.

## Approach

**Sensor placement (Minimum Vertex Cover):**

1. **2-approximation:** take both endpoints of each edge in a maximal matching. Provably never worse than twice the optimum.
2. **Greedy:** repeatedly instrument the machine with the most unmonitored links. No guarantee, but often strong in practice.
3. **Exact branch-and-bound:** backtracking search with pruning (degree-1 rule and a lower bound).
4. **Integer Linear Programming:** solved with PuLP and the CBC solver; also handles per-machine sensor costs.
5. *(Planned)* **Local search** that improves a greedy solution.

**Attacker isolation:** Edmonds-Karp max-flow, with the min-cut giving the cheapest set of links to remove. With unit capacities, the flow value counts independent attack routes.

**Theory:** proof of the 2-approximation guarantee, NP-completeness of Vertex Cover (via Clique), and the equivalence of Vertex Cover, Independent Set and Clique, shown as ILP models.

**Experiments:** all solvers are benchmarked on three graph families (hub-heavy, random, grid) across increasing sizes, measuring solution quality (ratio to optimal) and running time.

## Syllabus mapping

| Unit | Where it appears |
|---|---|
| I: Asymptotic analysis, correctness | Complexity analysis of every solver; correctness proofs |
| IV: Greedy and backtracking | Greedy heuristic, branch-and-bound, 2-approximation |
| V: Network flow | Edmonds-Karp, Max-Flow Min-Cut, attacker isolation |
| VI: NP-completeness | Vertex Cover NP-completeness, ILP modeling of Vertex Cover / Independent Set / Clique |

## Repository structure

```
sensorplace/     library code: graph generators, solvers, min-cut, ILP models, visualisation
tests/           correctness tests (brute force and NetworkX cross-checks)
experiments/     benchmark and experiment scripts; run as: python -m experiments.<name>
docs/            proofs and write-ups (approximation, NP-completeness, exact search, flow, complexity)
figures/         generated plots and network drawings
PROJECT_PLAN.md  team plan: roles, tasks, timeline, report outline
CLAUDE.md        instructions for Claude Code (shared by the team)
```

A graph is a Python `set` of edges `(u, v)` with `u < v`. Every solver takes the edges and returns a set of vertices.

## Getting started

Requires Python 3.10 or newer.

```bash
git clone <repo-url>
cd <repo-folder>
pip install -r requirements.txt
pytest -q                          # all tests should pass
python -m experiments.benchmark    # takes a few minutes; writes results.csv
```

Run all commands from the repository root.

## Team and roles

Work is split into four areas of roughly equal effort. Details, tasks, and deadlines for each are in [`PROJECT_PLAN.md`](PROJECT_PLAN.md).

| Person | Name | Area |
|---|---|---|
| 1 | | Approximation and greedy: 2-approximation proof, greedy counterexample, ratio experiments |
| 2 | | NP-completeness and ILP: reduction proof, ILP models, weighted-cost experiment |
| 3 | | Exact search and local search: pruning analysis, scaling limits, local-search solver |
| 4 | | Network flow, scenario, visualisation, report and demo assembly |

## Workflow

- Each person edits only the files they own (listed in `PROJECT_PLAN.md` and `CLAUDE.md`).
- Pull before you start working; commit small and often.
- Work on your own branch `person-N`; merge into `main` through a pull request once the tests pass.
- Every new function has a test. Run `pytest -q` before every commit.
- Every number in the report comes from a script, never typed by hand.
- Each member must be able to explain every part of the project at the viva.

**Using Claude Code:** `CLAUDE.md` is read automatically at the start of a session. Tell it which person you are. It is set up to teach first and build second, to stay within your files, and to never commit or push. All commits and pushes are made by the team members themselves.

## Status

- [x] Starter code: graph generators, four vertex cover solvers, min-cut, correctness tests
- [ ] Proof: 2-approximation guarantee
- [ ] Proof: NP-completeness of Vertex Cover
- [ ] ILP models for Vertex Cover, Independent Set, Clique
- [ ] Full benchmark across graph families (`results.csv`)
- [ ] Plots: approximation ratio, exact-search scaling, ILP runtime, pruning ablation
- [ ] Weighted sensor-cost experiment
- [ ] Local-search solver
- [ ] Campus network scenario and visualisation
- [ ] Report and demo

## Results

*To be filled in from `results.csv` and `figures/` once the benchmark has been run.*

## References

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms* (CLRS), ch. 26, 34, 35.
- J. Kleinberg, E. Tardos, *Algorithm Design*, ch. 7, 8, 10, 11.
- R. M. Karp, "Reducibility Among Combinatorial Problems", 1972.
- L. R. Ford Jr., D. R. Fulkerson, "Maximal Flow through a Network", 1956.
- [PuLP documentation](https://coin-or.github.io/pulp/) and [NetworkX documentation](https://networkx.org/).