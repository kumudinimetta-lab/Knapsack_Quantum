# Novelty possibilities after the corrections

These are research directions, not established priority claims. The revised
paper does not describe the combination as the first quantum knapsack hybrid.

The closest verified work already covers feasible-state generation with
amplitude amplification and maximum finding ([Wilkening et al., 2025](https://doi.org/10.1038/s41534-025-01097-8)),
quantum binary search and hybrid branch-and-bound ([Creemers and Perez Armas,
2025](https://doi.org/10.1016/j.ejor.2024.12.016)), and annealer-assisted knapsack
branch-and-bound ([Bozejko et al.](https://doi.org/10.1007/s10479-024-06025-1)).
Thus hybridization, thresholding, or being knapsack-specific is insufficient
by itself to support a novelty claim.

The most useful next theoretical target is a **nontrivial certified tree-size
bound for a clearly defined instance family**, obtained without enumerating the
whole tree. The present conservative B can be exponential, and merely knowing
that the core ratio is small does not solve that problem. A correct family-
specific certificate could connect the LP structure to the quantum query bound
more substantively. It would need explicit assumptions and adversarial examples;
it must not be presumed true because random data look favorable.

The most concrete engineering target is **coherent composition of the clean
finite-precision predicate (including the newly tested depth wrapper) with walk reflections**, followed
by an end-to-end gate/resource comparison against QTG and strong classical
baselines. The new Boolean circuits establish a transparent starting point but
use substantial workspace. Optimizing and benchmarking them could be a useful
component contribution; simply using known reversible arithmetic is not itself
evidence of novelty.

The exact integer fixed-gap counterexample and node-level rounding analysis
already strengthen the paper's mathematical clarity. They should be presented
as proved statements with bounded scope, not as priority claims until a fuller
literature search establishes what is already known. No practical speedup or
novel asymptotic advantage has been established by the current experiments.
