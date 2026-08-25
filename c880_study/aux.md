C880 VLSI Fault-Testing Project — Session Handoff Summary

This document is intended to be pasted into a future LLM session so the project can continue without repeating the requirements, assumptions, architecture, or decisions already made.

1. Project objective

We are developing a Python/Jupyter Notebook-based fault-testing framework for the ISCAS'85 C880 combinational benchmark.

The project has three main goals:

Generate test vectors

Stage 1: completely uniform random pattern generation.
Stage 2: weighted random pattern generation using circuit/SCOAP/path information.
Stage 3: dynamically directed random pattern generation using fault observability/testability information.

Execute the generated test vectors against the circuit and injected faults

Measure testing/simulation time.
Identify inserted fault and fault type/location.
Count detecting vectors for each fault.
Count PO mismatches.
Calculate collapsed fault coverage.
Record all PO values for every test vector.

Compare the three test-generation approaches

Determine whether SCOAP/path-guided weighting provides a meaningful improvement over uniform random testing.
Compare coverage versus number of vectors.
Compare runtime.
Compare detecting-vector distribution.
Compare PO mismatch behavior.
Determine whether directed fault selection provides a significant benefit.

The benchmark for the current work is specifically:

c880.bench

2. C880 benchmark information

The provided .bench begins with:

# c880
# 60 inputs
# 26 outputs
# 63 inverters
# 320 gates
# (143 ANDs + 150 NANDs + 29 ORs + 61 NORs + 26 buffers)


There are:

60 primary inputs
26 primary outputs

Primary inputs:

1
8
13
17
26
29
36
42
51
55
59
68
72
73
74
75
80
85
86
87
88
89
90
91
96
101
106
111
116
121
126
130
135
138
143
146
149
152
153
156
159
165
171
177
183
189
195
201
207
210
219
228
237
246
255
259
260
261
267
268


Primary outputs:

388
389
390
391
418
419
420
421
422
423
446
447
448
449
450
767
768
850
863
864
865
866
874
878
879
880


Example circuit definitions:

269 = NAND(1, 8, 13, 17)
270 = NAND(1, 26, 13, 17)
273 = AND(29, 36, 42)
276 = AND(1, 26, 51)
279 = NAND(1, 8, 51, 17)
280 = NAND(1, 8, 13, 55)


The full .bench file exists locally and should be treated as the authoritative circuit definition.

3. Fault model

We are testing single stuck-at faults.

Both:

SA0
SA1

are used.

The fault file is a collapsed fault list.

Examples:

1->269/SA1
1->270/SA1
1->276/SA1
1->279/SA1
1->280/SA1
1->483/SA1

1/SA0
1/SA1

101->303/SA1
101->304/SA0

Fault semantics

There are two important categories.

Stem/node fault

Example:

1/SA0


This means signal/stem 1 is stuck at zero.

Similarly:

1/SA1


means signal 1 is stuck at one.

Branch fault

Example:

1->269/SA1


means the specific branch/connection

1 → 269


is stuck at 1.

It must not be implemented as signal 1 globally stuck at 1.

For example, if signal 1 fans out to:

269
270
276
279
280
483


then:

1->269/SA1


must affect only the input of gate 269.

This branch-vs-stem distinction is critical.

4. Fanout-stem information

An additional fanout-stem file is available.

Example:

Fanout stems:
  1: 6 branches -> 269, 270, 276, 279, 280, 483
  101: 4 branches -> 303, 304, 334, 506
  106: 4 branches -> 303, 304, 335, 508
  111: 4 branches -> 305, 306, 336, 511
  116: 4 branches -> 305, 306, 338, 513
  121: 4 branches -> 307, 308, 340, 515
  126: 3 branches -> 307, 308, 517
  13: 3 branches -> 269, 270, 280
  130: 4 branches -> 498, 499, 518, 519


This information should eventually be used to correctly interpret branch/stem faults and potentially optimize fault injection.

5. SCOAP information

A SCOAP file is available with fields:

signal, type, CC0, CC1, CO, CC_avg, Testability, is_PI, is_PO


Example:

1, PI, 1, 1, 6, 1.0, 7.0, True, False
8, PI, 1, 1, 6, 1.0, 7.0, True, False
13, PI, 1, 1, 6, 1.0, 7.0, True, False
17, PI, 1, 1, 6, 1.0, 7.0, True, False
26, PI, 1, 1, 6, 1.0, 7.0, True, False
29, PI, 1, 1, 4, 1.0, 5.0, True, False
36, PI, 1, 1, 4, 1.0, 5.0, True, False
42, PI, 1, 1, 4, 1.0, 5.0, True, False
51, PI, 1, 1, 6, 1.0, 7.0, True, False


SCOAP will be used later for weighted and directed test generation.

6. Path-tracing information

A path-tracing file is also available with:

rank
signal
gate
level
fanout
PO_count
PO_impact
PO_impact_%
reachable_POs


Example:

rank 1
signal 1
fanout 6
PO_count 15
PO_impact 0.5769230769230769
PO_impact_% 57.692307692307686
reachable_POs =
['418', '419', '446', '447', '448', '449',
 '850', '863', '864', '865', '866',
 '874', '878', '879', '880']


Other examples:

signal 29
PO_count 15
PO_impact_% 57.6923

signal 42
PO_count 14
PO_impact_% 53.8462

signal 59
PO_count 13
PO_impact_% 50.0

signal 13
PO_count 13
PO_impact_% 50.0


This information will later be combined with SCOAP.

7. Detection definition

A fault is considered detected when at least one primary output differs between:

good circuit response


and

faulty circuit response


Formally, for a test vector:

𝐷
𝑒
𝑡
𝑒
𝑐
𝑡
𝑒
𝑑
(
𝑓
,
𝑣
)
=
{
1
	
if any PO differs


0
	
otherwise

For example:

Good PO:
101101...

Faulty PO:
101001...


means the fault is detected.

The exact number of different POs should also be recorded.

8. Testing limits

For the initial experiment:

Maximum number of test vectors = 1024
This is exactly:

2
10
=
1024

Two possible stopping conditions are being considered:

100% collapsed fault coverage, if achieved before 1024 vectors.
Otherwise stop at 1024 vectors.

For initial comparison it may be useful to support both:

early stop at 100% coverage


and

always run all 1024 vectors


because both approaches can provide useful experimental data.

9. Randomization

Randomization is acceptable.

For reproducibility, the current implementation uses:

RANDOM_SEED = 42


and:

N_VECTORS = 1024


Stage 1 uses uniform random binary values for all 60 PIs.

All inputs initially have equal probability:

𝑃
(
𝑥
𝑖
=
0
)
=
𝑃
(
𝑥
𝑖
=
1
)
=
0.5

10. Test-generation roadmap
Stage 1 — Uniform random

Generate up to 1024 random vectors.

Every PI has equal probability.

Goal:

establish baseline coverage
establish baseline runtime
establish baseline detecting-vector count
establish coverage-vs-vector curve
Stage 2 — Weighted random

Assign different weights/probabilities to signals.

The project will likely experiment with:

Stage 2A

Equal PO weights.

All 26 POs have equal importance.

Stage 2B

Different PO weights.

Weights are derived from path-tracing information.

The user suggested an idea based on the total weight of POs reachable from a signal/fault.

Example:

Signal 1 affects 15 of the 26 POs.

A possible weighting metric could be:

𝑊
(
𝑠
)
=
∑
𝑃
𝑂
∈
𝑅
𝑒
𝑎
𝑐
ℎ
𝑎
𝑏
𝑙
𝑒
(
𝑠
)
𝑤
𝑃
𝑂

with equal PO weights initially:

𝑤
𝑃
𝑂
=
1

giving:

𝑊
(
1
)
=
15

Later, different PO weights can be assigned.

This approach is not yet finalized.

11. Stage 3 — Dynamic fault-directed random testing

Still under consideration.

The proposed idea is:

Use existing SCOAP and path information.
Estimate how easy/difficult a fault is to activate and observe.
Dynamically select a subset of faults to target.
Generate random vectors preferentially aimed at those faults.
Remove/discard faults that are considered too expensive for the current generation phase, while retaining them in the final report as not included/untargeted.

Potential difficulty metric:

𝐶
𝑜
𝑠
𝑡
(
𝑓
)
=
𝐴
𝑐
𝑡
𝑖
𝑣
𝑎
𝑡
𝑖
𝑜
𝑛
𝐶
𝑜
𝑠
𝑡
(
𝑓
)
+
𝑂
𝑏
𝑠
𝑒
𝑟
𝑣
𝑎
𝑡
𝑖
𝑜
𝑛
𝐶
𝑜
𝑠
𝑡
(
𝑓
)

or some normalized combination of:

CC0
CC1
CO
path observability
reachable PO count
PO impact

This requires further design before implementation.

12. PO-weight idea

The user proposed an interesting PO weighting concept.

For a signal/fault affecting multiple POs, calculate a weight based on the reachable POs.

For example:

signal 1
15 reachable POs
26 total POs


A future metric might consider a weighted PO response.

The user gave an example conceptually involving:

expected value = 2^27 - 1
received value = 2^12 - 1


if POs are interpreted as a binary/integer response and some/all outputs become zero.

This idea needs refinement before being used because:

a binary PO signature depends on PO ordering;
integer magnitude is not necessarily equivalent to observability;
one high-order PO mismatch can dominate several low-order mismatches;
the metric should probably be defined independently of arbitrary PO numbering.

A better candidate may be:

𝑃
𝑂
𝑊
𝑒
𝑖
𝑔
ℎ
𝑡
(
𝑓
)
=
∑
𝑝
∈
𝑅
𝑒
𝑎
𝑐
ℎ
𝑎
𝑏
𝑙
𝑒
(
𝑓
)
𝑤
𝑝

and separately:

𝑀
𝑖
𝑠
𝑚
𝑎
𝑡
𝑐
ℎ
𝑊
𝑒
𝑖
𝑔
ℎ
𝑡
(
𝑓
,
𝑣
)
=
∑
𝑝
∈
𝑀
𝑖
𝑠
𝑚
𝑎
𝑡
𝑐
ℎ
(
𝑓
,
𝑣
)
𝑤
𝑝

This should be evaluated experimentally.

13. Initial implementation completed

The first part of the implementation has been designed in Python for Jupyter.

The code currently contains:

Circuit representation
class Gate
class Circuit

.bench parser
parse_bench_file()

Evaluation order
build_evaluation_order()


The circuit is topologically ordered before simulation.

Circuit validation
validate_circuit_signals()

Logic evaluation
evaluate_gate()


Supports at least:

AND
NAND
OR
NOR
NOT / INV / INVERTER
BUF / BUFFER

Good-circuit simulation
simulate_circuit()


and generalized:

simulate_circuit_with_fault()

PO extraction
get_po_vector()
po_vector_to_string()

14. Scenario 1 vector generation

The current vector generator:

generate_random_vectors()


generates:

1024 vectors
60 bits/vector
uniformly random
unique vectors
deterministic with seed 42

Vectors are stored as dictionaries mapping PI signal names to 0/1.

They are also represented as strings such as:

010101001...


in the exact PI order from the .bench file.

15. Good-circuit results

The current implementation simulates all 1024 good-circuit vectors.

Results contain:

vector_id
input_vector
po_vector
simulation_time_s


POs are also expanded into individual columns:

PO_388
PO_389
PO_390
...
PO_880


Results are saved as:

c880_scenario1_good_circuit_results.csv
c880_scenario1_po_values.csv

16. Fault representation implemented

A Fault dataclass was introduced:

@dataclass(frozen=True)
class Fault:
    fault_id: int
    source: str
    location: str
    fault_type: str
    is_branch: bool


It supports:

1/SA0
1/SA1
1->269/SA1
101->303/SA0


The .name property returns the original-style representation.

17. Fault parser implemented

Functions:

parse_fault_line()
load_fault_file()


These parse both:

signal/SA0
signal/SA1


and:

source->destination/SA0
source->destination/SA1


The fault list should be treated as the collapsed fault universe for coverage.

18. Fault validation

Function:

validate_faults()


checks:

source exists
location exists
branch destination is a gate
branch source is actually an input of the destination gate

This is especially important for branch faults.

19. Fault injection implementation

The current fault simulator handles:

Stem fault
1/SA0


All uses of signal 1 are forced to 0.

Branch fault
1->269/SA1


Only the connection:

1 → 269


is forced to 1.

The other fanout branches from signal 1 remain unchanged.

The fault is injected while evaluating gate inputs rather than by globally overwriting the source signal.

This is the correct conceptual model for branch faults.

20. Fault detection implementation

Function:

compare_po_vectors()


returns:

detected
mismatch_count
mismatching_pos


A fault is detected if:

len(mismatching_pos) > 0


For every vector/fault pair we want to retain:

vector_id
fault_id
fault
fault_type
is_branch
good_po
faulty_po
detected
mismatch_count
mismatching_pos

21. Current naive fault simulation

A straightforward loop was designed:

for vector in random_vectors:
    for fault in faults:
        simulate_fault(...)


This creates:

1024
×
𝑁
𝑓
𝑎
𝑢
𝑙
𝑡
𝑠

fault/vector simulations.

However, the current naive implementation unnecessarily recomputes the good circuit for every fault.

This should NOT be used as the final implementation.

22. Immediate next step

The next coding task should be to implement the optimized fault simulation architecture.

Instead of:

for vector:
    for fault:
        simulate good
        simulate faulty


use:

for vector:
    simulate good ONCE
    store 26-bit good PO response

    for fault:
        simulate faulty
        compare faulty PO against cached good PO


Therefore:

𝐺
𝑜
𝑜
𝑑
𝑆
𝑖
𝑚
𝑢
𝑙
𝑎
𝑡
𝑖
𝑜
𝑛
𝑠
=
1024

instead of:

𝐺
𝑜
𝑜
𝑑
𝑆
𝑖
𝑚
𝑢
𝑙
𝑎
𝑡
𝑖
𝑜
𝑛
𝑠
=
1024
×
𝑁
𝑓
𝑎
𝑢
𝑙
𝑡
𝑠

This is the correct baseline architecture.

23. Recommended optimized data flow

Use:

                    ┌─────────────────┐
                    │ Test Vector #1  │
                    └────────┬────────┘
                             │
                     Good circuit
                             │
                         Good PO
                             │
                  ┌──────────┴──────────┐
                  │                     │
                Fault 1              Fault 2 ... Fault N
                  │                     │
              Faulty PO             Faulty PO
                  │                     │
                  └──────────┬──────────┘
                             │
                      XOR comparison
                             │
                       PO mismatches


Then move to vector #2.

24. Fault simulation results to collect

For each fault:

Identification
fault_id
fault
fault_type
source
location
is_branch

Detection
detected
detecting_vector_count
first_detecting_vector

PO behavior
total_po_mismatches


and ideally:

per-PO mismatch count


For example:

PO_388 mismatch count
PO_389 mismatch count
...
PO_880 mismatch count

Coverage

Overall:

total collapsed faults
detected collapsed faults
undetected collapsed faults
fault coverage %

25. Coverage curve

A major experimental result should be:

Vector count → Fault coverage


Example:

1 vector      → 12.4%
10 vectors    → 34.7%
50 vectors    → 61.2%
100 vectors   → 72.1%
...
1024 vectors  → XX.X%


This curve will eventually be compared between:

Uniform Random
Weighted Random
Dynamic Fault-Directed Random

26. Runtime metrics

The final experiments should distinguish at least:

Test-vector generation time

Time required to generate the vectors.

Good-circuit simulation time

Time to simulate all good vectors.

Fault simulation time

Time to simulate faults.

Total experiment time

Preferably:

𝑇
𝑡
𝑜
𝑡
𝑎
𝑙
=
𝑇
𝑔
𝑒
𝑛
𝑒
𝑟
𝑎
𝑡
𝑖
𝑜
𝑛
+
𝑇
𝑔
𝑜
𝑜
𝑑
+
𝑇
𝑓
𝑎
𝑢
𝑙
𝑡

For later comparison, use the same hardware/environment and preferably multiple random seeds if statistical significance is desired.

27. Fault dropping consideration

Fault dropping is a future optimization.

Once a fault is detected by a vector, it no longer needs to be simulated for subsequent vectors if the only goal is to determine the minimum number of vectors needed to detect every fault.

However, there is an important conflict:

The project also wants:

total number of detecting vectors for each fault.

Therefore, full fault dropping cannot be used during the experiment if we need the exact detecting-vector count.

Possible modes:

Mode A — Full statistics

Do not drop detected faults.

This gives:

detecting_vector_count
PO mismatch statistics


for every fault.

Mode B — Coverage acceleration

Drop detected faults.

This gives:

minimum/early test set
coverage progression
runtime reduction


but does not give exact detecting-vector counts after first detection.

Both modes should eventually be supported.

28. Important distinction: collapsed faults

Fault coverage must use:

number of faults in the provided collapsed fault file


as the denominator.

Do not silently expand to the complete uncollapsed fault universe unless explicitly requested later.

Thus:

𝐹
𝐶
=
detected collapsed faults
total collapsed faults
×
100

29. Future open-source fault simulator

At the beginning, no fault simulator was available.

The current approach is to implement a Python fault simulator directly because:

C880 is small enough;
the .bench format is simple;
branch faults require exact control;
we need custom PO mismatch and per-fault statistics;
later weighted/directed generation will benefit from direct access to internal circuit information.

An external/open-source simulator can still be evaluated later for cross-validation.

Do not replace the custom simulator until its fault semantics are validated.

30. Stage 2 future implementation

After Scenario 1 is validated:

Weighted random generation

Build a signal weighting model from:

SCOAP
+
path tracing
+
fanout information


Potential initial formulation:

𝑆
𝑐
𝑜
𝑟
𝑒
(
𝑠
)
=
𝛼
⋅
𝑁
𝑜
𝑟
𝑚
𝑎
𝑙
𝑖
𝑧
𝑒
(
𝐶
𝑂
(
𝑠
)
)
+
𝛽
⋅
𝑁
𝑜
𝑟
𝑚
𝑎
𝑙
𝑖
𝑧
𝑒
(
𝑃
𝑂
𝐼
𝑚
𝑝
𝑎
𝑐
𝑡
(
𝑠
)
)
+
𝛾
⋅
𝑁
𝑜
𝑟
𝑚
𝑎
𝑙
𝑖
𝑧
𝑒
(
𝑃
𝑂
𝐶
𝑜
𝑢
𝑛
𝑡
(
𝑠
)
)

But the direction of the SCOAP term must be carefully chosen because:

lower CO generally means easier observability;
lower CC means easier controllability;
higher PO impact means potentially greater observability.

Do not simply sum raw values without normalization.

31. Potential weighting model

A more principled model may separate:

Controllability

𝐶
(
𝑠
)
=
𝑓
(
𝐶
𝐶
0
(
𝑠
)
,
𝐶
𝐶
1
(
𝑠
)
)

Observability

𝑂
(
𝑠
)
=
𝑔
(
𝐶
𝑂
(
𝑠
)
,
𝑃
𝑂
𝐼
𝑚
𝑝
𝑎
𝑐
𝑡
(
𝑠
)
,
𝑃
𝑂
𝐶
𝑜
𝑢
𝑛
𝑡
(
𝑠
)
)

Combined testability

𝑇
(
𝑠
)
=
ℎ
(
𝐶
(
𝑠
)
,
𝑂
(
𝑠
)
)

Then normalize:

𝑊
(
𝑠
)
=
𝑁
𝑜
𝑟
𝑚
𝑎
𝑙
𝑖
𝑧
𝑒
(
𝑇
(
𝑠
)
)

and convert to random generation probabilities.

The exact formula remains open for discussion.

32. PO weighting future experiment

We agreed that it is worthwhile to test two weighted-PO configurations:

Configuration A
All POs equal weight

Configuration B
PO weights derived from path-tracing information


This allows us to determine whether merely using path-derived PO importance improves generation.

33. Stage 3 future experiment

The third method will potentially work as:

Fault list
    ↓
Calculate fault difficulty
    ↓
Rank faults
    ↓
Select difficult/high-priority faults
    ↓
Generate targeted random vectors
    ↓
Simulate
    ↓
Update remaining fault set
    ↓
Recalculate priority
    ↓
Repeat


This is intentionally not finalized yet.

Potential priority factors:

fault controllability
fault observability
reachable PO count
PO impact
SCOAP CC0/CC1
SCOAP CO
historical detection difficulty
number of vectors already tried


A particularly interesting future strategy is to dynamically update fault priority based on observed detection performance.

34. Future experimental comparison

For each strategy we should record:

Metric	Uniform	Weighted	Directed
Vectors generated			
Generation time			
Good simulation time			
Fault simulation time			
Total runtime			
Final fault coverage			
Vectors to 100% coverage			
Undetected faults			
Avg detecting vectors/fault			
Total PO mismatches			

Also generate:

Coverage curve
x = number of vectors
y = fault coverage %

Detection distribution
fault → number of detecting vectors

Fault difficulty

Compare SCOAP/path estimates against actual detection difficulty.

This will be especially valuable for validating whether the proposed heuristic actually predicts difficult faults.

35. Potential statistical comparison

Because random pattern generation is stochastic, one seed is useful for debugging but not sufficient for a rigorous comparison.

Eventually consider:

Seeds:
42
43
44
45
...


For each method calculate:

mean coverage
standard deviation
mean vectors-to-target
runtime
confidence intervals if appropriate

For the initial development, however, seed 42 / 1024 vectors is sufficient.

36. Current status at end of session
Completed conceptually
Project requirements defined.
C880 identified.
Single stuck-at fault model established.
Stem and branch faults distinguished.
Collapsed fault file established as coverage universe.
SCOAP information identified.
Path-tracing information identified.
Fanout-stem information identified.
Uniform random generation established.
Maximum 1024 vectors established.
Detection definition established.
PO mismatch measurement established.
Weighted and directed generation concepts established.
Python/Jupyter architecture established.
.bench parser designed.
Topological circuit evaluation designed.
Good-circuit simulation designed.
Fault parser designed.
Fault injection designed.
Branch fault semantics designed.
PO comparison designed.
Coverage calculation designed.
Not yet fully completed/validated

The actual full fault experiment should still be validated and optimized.

In particular:

Load the actual fault file.
Run fault validation.
Test stem fault manually.
Test branch fault manually.
Confirm branch injection changes only the intended gate input.
Implement optimized good-response caching.
Run all faults × 1024 vectors.
Calculate final coverage.
Generate coverage curve.
Save fault-level results.
37. Immediate next coding session

Start from the existing notebook, do not rebuild the circuit parser from scratch.

The next cell should implement something like:

good_results = {}

for vector_id, input_vector in enumerate(random_vectors, start=1):

    good_values = simulate_circuit_with_fault(
        circuit,
        input_vector,
        fault=None
    )

    good_results[vector_id] = get_po_vector(
        circuit,
        good_values
    )


Then:

for vector_id, input_vector in enumerate(random_vectors, start=1):

    good_po = good_results[vector_id]

    for fault in faults:

        faulty_values = simulate_circuit_with_fault(
            circuit,
            input_vector,
            fault=fault
        )

        faulty_po = get_po_vector(
            circuit,
            faulty_values
        )

        # compare good_po vs faulty_po


This should be the baseline optimized fault simulator.

After that, we should consider a second optimization: avoid repeatedly reconstructing data structures and potentially exploit the fact that the circuit is static and only one branch/node is modified per fault.

38. Important implementation philosophy

Throughout this project:

Keep everything executable in Jupyter Notebook.
Prefer clear, testable functions over one giant script.
Preserve raw experimental data.
Never overwrite raw results with processed summaries.
Use deterministic seeds when debugging.
Keep circuit PO ordering fixed according to .bench.
Keep PI ordering fixed according to .bench.
Explicitly distinguish branch and stem faults.
Never claim a fault is detected unless at least one PO differs.
Use the supplied collapsed fault file as the coverage denominator.
Record enough information to reproduce every result.
Separate correctness implementation from performance optimization.
Validate each optimization against the simple reference implementation before trusting it.
39. Files expected in the project

The eventual notebook/project should have approximately:

c880.bench
c880_collapsed_faults.txt
c880_scoap.txt
c880_path_tracing.txt
c880_fanout_stems.txt


Generated outputs:

c880_scenario1_good_circuit_results.csv
c880_scenario1_po_values.csv
c880_scenario1_fault_simulation.csv
c880_scenario1_fault_summary.csv
c880_scenario1_coverage_curve.csv


Future:

c880_scenario2_weighted_results.csv
c880_scenario3_directed_results.csv
comparison_results.csv

40. Key conclusion from today's session

The most important architectural decision is:

Treat the .bench circuit as a combinational directed graph and inject branch faults at the specific gate-input connection rather than globally modifying the source signal.

The second important decision is:

Cache the good-circuit PO response once per vector and reuse it for every fault.

This gives us a clean baseline:

                 C880
                  │
          ┌───────┴────────┐
          │                │
      Test Vector       Fault List
          │                │
          ▼                ▼
    Good simulation    Fault injection
          │                │
          ▼                ▼
       Good POs         Faulty POs
          │                │
          └───────┬────────┘
                  ▼
             PO comparison
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
     detected   mismatch   fault coverage


This is the foundation for all three future test-generation strategies.

Next session should begin with the optimized fault simulation implementation and validation, not with test-generation strategy design yet. Once Scenario 1 produces trustworthy fault-level results, those results become the baseline against which the weighted and dynamically directed approaches will be evaluated.