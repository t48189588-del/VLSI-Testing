# Initial Research Milestone: Dependability-Driven Adaptive VLSI Testing

> **Research Status:** Initial Concept Definition
> **Objective:** Establish a theoretical framework that unifies VLSI testing, dependability, and adaptive/ML-driven optimization.

---

# 1. Research Motivation

Traditional VLSI testing aims to maximize defect detection while minimizing manufacturing escapes. However, modern testing faces increasing challenges:

* Increasing transistor counts
* Longer test times
* Higher ATE costs
* Growing test vector storage
* Application-specific quality requirements (consumer, automotive, aerospace, medical)

Current optimization methods generally focus on:

* Test compression
* Test compaction
* Test scheduling
* ATPG optimization

The proposed research shifts the optimization target from **maximizing fault coverage** toward **maximizing confidence in dependability** while minimizing testing cost.

---

# 2. Core Research Question

Instead of asking:

> *How can we reduce the number of test vectors while maintaining fault coverage?*

The proposed research asks:

> **How can we achieve the required level of dependability assurance using the minimum amount of testing evidence?**

This reframes testing as an evidence-generation process rather than simply a fault-detection process.

---

# 3. Hierarchy of Concepts

```text
Dependability
        ↑
Assurance
        ↑
Evidence
        ↑
Verification + Validation + Testing
```

Testing is **not** the objective.

Testing produces evidence.

Evidence supports assurance.

Assurance provides confidence in dependability.

---

# 4. Dependability as the Umbrella Concept

Dependability is considered the highest-level engineering objective because it encompasses:

* Reliability
* Availability
* Safety
* Integrity
* Maintainability

Unlike **Functional Safety**, which only concerns safe behavior after faults occur, **Dependability** includes both:

* Preventing faults from escaping manufacturing.
* Ensuring acceptable behavior when faults occur during operation.

Therefore, dependability provides a broader optimization target than fault coverage alone.

---

# 5. Fault Terminology

The following hierarchy should remain consistent throughout the research.

```text
Manufacturing Defect
        ↓
Electrical Fault
        ↓
System Error
        ↓
Observable Failure
```

Definitions:

**Defect**

Physical manufacturing imperfection.

Examples:

* Missing via
* Metal bridge
* Oxide defect

---

**Fault**

Electrical abstraction of a defect.

Examples:

* Stuck-at
* Stuck-open
* Bridging
* Delay fault

---

**Error**

Incorrect internal system state.

---

**Failure**

Externally observable incorrect system behavior.

---

# 6. Dependability Evidence Throughout the VLSI Lifecycle

## Stage 1 — Pre-Silicon

Goal:

Verify that the design is correct.

Methods:

* RTL Simulation
* Formal Verification
* Gate-Level Simulation
* Static Timing Analysis
* Power Analysis
* Fault Simulation
* Fault Injection

Evidence Produced:

* Functional correctness
* Timing correctness
* Fault tolerance
* Testability

---

## Stage 2 — Manufacturing Test

Goal:

Verify that each fabricated chip is free from manufacturing defects.

Methods:

* Scan Testing
* ATPG
* Transition Fault Testing
* Bridging Fault Testing
* IDDQ
* Delay Testing

Evidence Produced:

* Fault coverage
* Defect screening
* Manufacturing quality

---

## Stage 3 — Characterization

Goal:

Measure robustness under operating conditions.

Methods:

* Voltage corners
* Temperature corners
* Frequency sweeps

Evidence Produced:

* Operating margins
* Robustness

---

## Stage 4 — Reliability Qualification

Goal:

Estimate lifetime behavior.

Methods:

* Burn-In
* HTOL
* Electromigration
* Aging characterization

Evidence Produced:

* Lifetime reliability

---

## Stage 5 — Functional Safety Validation

Goal:

Verify safe behavior after faults occur.

Methods:

* Fault Injection
* Diagnostic Testing
* Redundancy Verification

Evidence Produced:

* Diagnostic coverage
* Fault tolerance
* Safe-state transition capability

---

# 7. Important Observation

Fault coverage is **not** a dependability metric.

It is evidence supporting dependability.

This distinction is central to the proposed framework.

---

# 8. Proposed Optimization Framework

Current testing is approximately formulated as:

```text
Maximize Fault Coverage

Subject to

Test Cost
```

The proposed formulation becomes:

```text
Minimize Testing Cost

Subject to

Required Dependability Assurance
```

or mathematically,

[
\min C_{\text{test}}
]

subject to

[
\begin{aligned}
FC &\ge FC_{min}\
DPPM &\le DPPM_{max}\
P(\text{Unsafe Product}) &\le \epsilon
\end{aligned}
]

where:

* FC = Fault Coverage
* DPPM = Defective Parts Per Million
* ε = acceptable residual risk

---

# 9. Proposed Dependability Confidence Concept

A new conceptual metric is proposed:

## Dependability Confidence

Rather than measuring only fault coverage,

estimate the confidence that the manufactured chip satisfies its required dependability objectives.

Conceptually,

[
DC = P(\text{Dependability Requirements Satisfied}\mid\text{Evidence})
]

where evidence may include:

* Simulation results
* Formal verification
* ATPG
* Scan testing
* Delay testing
* Characterization
* Burn-in
* Reliability tests
* Fault injection
* Safety diagnostics

Testing therefore becomes an information-gathering process.

Each additional test should ideally reduce uncertainty.

---

# 10. Machine Learning Perspective

Machine Learning is **not intended to replace testing**.

Instead, ML becomes a decision engine.

Possible roles include:

* Test selection
* Test prioritization
* Adaptive testing
* Early stopping
* Test scheduling
* Fault localization
* Yield prediction
* Risk estimation

Rather than asking

> "Which faults remain?"

the ML model asks

> "Which test provides the largest increase in dependability confidence?"

---

# 11. Future Adaptive Testing Vision

Traditional ATPG philosophy:

```text
Generate vectors
↓

Detect faults

↓

Increase Fault Coverage
```

Proposed philosophy:

```text
Generate candidate tests

↓

Estimate information gain

↓

Execute highest-value test

↓

Update Dependability Confidence

↓

Repeat until required confidence is achieved
```

This creates an adaptive testing loop.

---

# 12. Potential Research Hypothesis

A possible central hypothesis is:

> **Adaptive testing guided by estimated dependability confidence can achieve equivalent or better manufacturing quality than conventional fixed test flows while significantly reducing test time, test data volume, and overall manufacturing cost.**

---

# 13. Open Research Questions

The following questions remain to be explored:

1. **How should Dependability Confidence be mathematically modeled?**

   * Bayesian inference?
   * Information theory?
   * Belief functions?
   * Probabilistic graphical models?

2. **How can each test's information gain be quantified?**

   * Mutual information?
   * Entropy reduction?
   * Confidence interval reduction?
   * Expected Value of Information (EVI)?

3. **What features should drive ML-based adaptive testing?**

   * ATPG outcomes
   * Physical layout
   * Process monitor data
   * Wafer coordinates
   * Previous test outcomes
   * PVT measurements
   * Aging indicators

4. **How should application-specific dependability targets be incorporated?**

   * Consumer electronics
   * Automotive (ISO 26262)
   * Aerospace
   * Medical devices

5. **How can confidence thresholds be mapped to industrial metrics?**

   * Fault Coverage
   * DPPM
   * Diagnostic Coverage
   * Safety Integrity Levels (SIL/ASIL)

---

# 14. Key Insight

The fundamental shift proposed by this research is:

> **Testing should be viewed not as a process for maximizing fault detection, but as a process for collecting sufficient evidence to justify confidence that a device satisfies its required dependability objectives.**

Under this paradigm, adaptive and ML-driven testing become principled methods for optimizing *evidence acquisition*, balancing manufacturing cost against the level of assurance required for the target application. This reframing provides a unified foundation that can encompass traditional ATPG, production testing, reliability qualification, and functional safety within a single dependability-driven framework.


## Possible week 10 report
I think there are **two separate research questions** here, and distinguishing them is what may make your work novel.

1. **How should dependability be modeled mathematically?** (A modeling problem.)
2. **Given that model, how should testing be optimized?** (A decision/optimization problem.)

Most of the literature focuses on (2). Very little work starts by redefining (1), especially for manufacturing test.

---

# 1. How should dependability be represented?

This is probably the most important decision in your dissertation.

I don't think dependability should be represented as a single scalar.

For example,

Is

* 99% reliable
* 100% safe

better than

* 100% reliable
* 99% safe?

There is no universal answer.

That immediately tells us

> **Dependability is inherently multi-objective.**

---

## Option A — Weighted Vector (my recommended starting point)

Represent dependability as a vector

[
D =
(R,\ S,\ A,\ M,\ I,\ \ldots)
]

where

* (R) = Reliability
* (S) = Safety
* (A) = Availability
* (M) = Maintainability
* (I) = Integrity

Each application defines its own importance vector

[
W =
(w_R,w_S,w_A,w_M,w_I)
]

Overall utility becomes

[
U=W\cdot D
]

Advantages

* Very intuitive
* Easy to explain
* Compatible with multi-objective optimization
* Compatible with ML

Disadvantage

Choosing weights is difficult.

---

## Option B — Utility Function

Instead of

weighted sum

define

[
U(D)
]

For example,

space systems

may have

```text
Reliability

must exceed

99.9999%

otherwise

utility ≈ 0
```

Consumer electronics

may instead have

```text
Cost dominates
```

This resembles decision theory.

---

## Option C — Bayesian Confidence (my favorite)

This aligns with our previous discussion.

Instead of

measuring dependability,

estimate

confidence

that the dependability requirements are satisfied.

[
P(D \ge D_{required}|Evidence)
]

Now every test updates

belief.

This is almost textbook Bayesian experimental design.

Very elegant.

---

# 2. Where does the literature currently stand?

This is actually encouraging.

I searched across recent work, and there is a clear pattern.

The field is moving toward **adaptive testing**, but not yet toward **dependability-driven adaptive testing**.

---

## Current Research Theme 1

Adaptive test reduction

Questions include

> Which test patterns are redundant?

> Which vectors can be removed?

ML

↓

Reduce test time

↓

Maintain fault coverage

Examples include adaptive VLSI test pattern selection using LDA/MRMR, Bayesian classifiers, and ensemble learning to reduce test cost while maintaining defect levels. ([ScienceDirect][1])

---

## Current Theme 2

Bayesian test selection

Question

> Which test should I execute next?

Bayesian Networks

↓

Estimate

probability of failure

↓

Reduce cost

Representative work formulates black-box test reduction as a constrained optimization problem using Bayesian networks to exploit dependencies among tests. ([Scholars@Duke][2])

---

## Current Theme 3

Data-driven adaptive testing

Question

> Can production history reduce testing?

Answer

Yes.

Historical yield

↓

ML

↓

Skip unnecessary tests

↓

Maintain quality

Recent work combines offline subset selection with online multi-armed bandits to switch between reduced and full test plans based on process stability while explicitly considering escape risk. ([Frontiers][3])

---

## Current Theme 4

Learning-based pattern ranking

Question

Which vectors matter most?

CNN

↓

Rank vectors

↓

Keep important ones

↓

Discard redundant ones

This direction aims to reduce pattern volume while preserving defect screening performance. ([ScienceDirect][4])

---

# Notice the common denominator

Every paper asks something like

```text
How can we reduce

Test Cost

while

maintaining

Fault Coverage?
```

or

```text
How can we

predict

Pass/Fail?
```

Very few ask

```text
What level of

application-specific confidence

is required?
```

That is a very different question.

---

# I think your work introduces a missing layer

Current literature

```text
Tests
↓

Fault Coverage
↓

Ship
```

Your proposal

```text
Tests

↓

Evidence

↓

Dependability Confidence

↓

Application Requirement

↓

Decision
```

The extra layer is

**Dependability Confidence**

This is not merely

fault coverage.

---

# Existing arguments supporting your hypothesis

Several independent research trends actually point toward your direction.

### Trend 1

Adaptive testing

already exists.

Researchers agree

fixed testing

is becoming inefficient. ([ScienceDirect][5])

---

### Trend 2

ML works

Many papers show

ML

can identify

redundant tests

or

important tests. ([ScienceDirect][1])

---

### Trend 3

Bayesian decision making

already appears.

Researchers

are replacing

fixed rules

with

probabilistic inference. ([Scholars@Duke][2])

---

### Trend 4

Production data

is valuable.

Everyone agrees

historical yield

contains information.

Yet

most methods

use it only

to predict pass/fail.

---

# Arguments against your hypothesis

These are the objections I would expect from reviewers.

---

## Objection 1

Manufacturing does not know the final application.

This is true.

Chip manufacturers often sell

the same die

to multiple customers.

Therefore

how can the test flow depend on the application?

This is probably

the biggest criticism.

---

Possible response

Use

application profiles.

For example

Standard

Industrial

Automotive

Space

Medical

The customer chooses

the profile

before manufacturing.

Exactly like

speed binning

or

temperature grades.

---

## Objection 2

Certification

Automotive

Medical

Space

already prescribe

minimum testing.

You

cannot simply

skip tests.

True.

Therefore

your optimization becomes

```text
Mandatory Tests

+

Adaptive Tests
```

rather than

removing

mandatory ones.

---

## Objection 3

Dependability

cannot be measured directly.

Correct.

This is actually

an opportunity.

Because

confidence

can be measured.

Exactly like

Bayesian statistics.

---

# Where I think the novelty actually is

I would be careful **not** to claim:

> "I propose adaptive testing."

That already exists.

I also would not claim:

> "I use ML for test reduction."

That is an active research area.

Instead, I think your contribution is at a higher level of abstraction:

> **I propose a decision-theoretic framework in which manufacturing tests are viewed as evidence-generating actions whose value depends on the dependability objectives of the target application. Adaptive testing is then formulated as a sequential decision problem that maximizes application-specific dependability assurance (or confidence) per unit of test cost.**

That framing shifts the optimization target from *fault coverage* to *assurance*. The adaptive policy is no longer justified because it preserves fault coverage alone, but because it maximizes the expected reduction in residual application-specific risk. In my view, that is the conceptual gap between the current state of the art and the research direction you've been developing. It also gives you a rich set of mathematical tools to draw from—Bayesian decision theory, active learning, sequential experimental design, and partially observable decision processes—without abandoning the established metrics (fault coverage, DPPM, diagnostic coverage) that industry already understands.

[1]: https://www.sciencedirect.com/science/article/abs/pii/S0167926021000948?utm_source=chatgpt.com "Valid test pattern identification for VLSI adaptive test - ScienceDirect"
[2]: https://scholars.duke.edu/publication/1473659?utm_source=chatgpt.com "Scholars@Duke publication: Black-Box Test-Cost Reduction Based on Bayesian Network Models"
[3]: https://www.frontiersin.org/journals/mechanical-engineering/articles/10.3389/fmech.2026.1861443/full?utm_source=chatgpt.com "Frontiers | A quality-preserving model for test reduction in electronics production"
[4]: https://www.sciencedirect.com/science/article/pii/S1879239126000470?utm_source=chatgpt.com "Learning-driven identification of fault-relevant test patterns for cost-efficient VLSI testing - ScienceDirect"
[5]: https://www.sciencedirect.com/science/article/pii/S2665917422001313?utm_source=chatgpt.com "Current issues and emerging techniques for VLSI testing - A review☆ - ScienceDirect"

Below is a "research context package" that can be copied into a new chat to continue the work without losing context. It summarizes the technical discussion, the current hypothesis, the research direction, and the open problems.

---

# Research Context: Dependability-Driven Adaptive VLSI Testing Framework

## Research Status

Early-stage PhD/MSc research conceptualization.

The objective is **not** to improve ATPG algorithms directly.

Instead, the objective is to propose a **new testing paradigm** where manufacturing and qualification testing are synthesized according to application-specific dependability requirements.

This is intended as a theoretical framework first, followed later by mathematical formalization and ML implementation.

---

# High-Level Research Vision

Traditional VLSI testing optimizes:

> Maximize Fault Coverage while minimizing Test Cost.

This research proposes replacing that objective with:

> Maximize Application-Specific Dependability Assurance while minimizing the cost of acquiring testing evidence.

Testing is viewed as an **evidence-generation process**, not merely a fault-detection process.

---

# Core Research Hypothesis

> **There is no universally optimal production test flow. The optimal testing strategy depends on the dependability requirements of the intended application. Therefore, production testing should be synthesized from application-specific dependability objectives rather than applying a fixed sequence of tests to every manufactured device.**

This shifts optimization from

* test vectors

to

* testing policies.

---

# Fundamental Conceptual Shift

Current manufacturing philosophy

```text
Specification
        ↓
ATPG
        ↓
Run Fixed Test Flow
        ↓
Fault Coverage
        ↓
Ship
```

Proposed philosophy

```text
Application Requirements
          ↓
Dependability Objectives
          ↓
Risk Assessment
          ↓
Evidence Planning
          ↓
Test Policy Synthesis
          ↓
Adaptive Testing
          ↓
Dependability Confidence
          ↓
Qualification Decision
```

---

# Key Insight

Testing is **not the objective.**

Testing generates **evidence**.

Evidence supports **assurance**.

Assurance provides confidence in **dependability**.

Hierarchy

```text
Dependability
        ↑
Assurance
        ↑
Evidence
        ↑
Verification
Validation
Testing
```

---

# Why Dependability?

Dependability is chosen as the umbrella engineering concept because it naturally encompasses

* Reliability
* Safety
* Availability
* Integrity
* Maintainability

Unlike Functional Safety, which focuses only on safe behavior after faults occur, Dependability includes

* preventing manufacturing escapes
* surviving operational faults
* maintaining correct service

---

# Fault Terminology

Keep these definitions consistent throughout the research.

```text
Physical Defect
        ↓
Electrical Fault
        ↓
System Error
        ↓
Observable Failure
```

Definitions

Defect

Physical manufacturing imperfection.

Fault

Electrical abstraction of a defect.

Error

Incorrect internal state.

Failure

Externally observable incorrect behavior.

---

# Dependability Throughout the Chip Lifecycle

## Pre-Silicon

Purpose

Verify the design.

Evidence

* RTL simulation
* Formal verification
* Gate-level simulation
* STA
* Power analysis
* Fault simulation
* Fault injection

Produces evidence for

* correctness
* robustness
* fault tolerance

---

## Manufacturing Test

Purpose

Verify manufactured silicon.

Methods

* ATPG
* Scan
* Delay tests
* Transition tests
* IDDQ
* Bridging tests

Produces evidence for

* manufacturing quality
* defect screening

---

## Characterization

Purpose

Measure operating margins.

Examples

* Voltage corners
* Temperature corners
* Frequency sweeps

---

## Reliability Qualification

Purpose

Estimate long-term behavior.

Methods

* Burn-in
* HTOL
* Aging
* Electromigration

---

## Functional Safety Validation

Purpose

Measure behavior after faults.

Methods

* Fault injection
* Diagnostic coverage
* Safe-state transitions
* Redundancy verification

---

# Important Observation

Fault Coverage

≠

Dependability

Instead

Fault Coverage

↓

Evidence

↓

Dependability Confidence

---

# Dependability Confidence

A proposed new conceptual metric.

Instead of measuring only fault coverage,

estimate

```math
P(
Dependability Requirements Satisfied
|
Evidence
)
```

Every test updates confidence.

Confidence becomes the stopping criterion.

Not simply

"All vectors executed."

---

# Multi-Dimensional Dependability

Dependability should **not** be represented as a single scalar.

Instead,

```math
D =
(
Reliability,
Safety,
Availability,
Integrity,
Maintainability,
...
)
```

Different applications assign different priorities to each dimension.

Example

Space

Reliability

Very High

Safety

Very High

Maintainability

Low

---

Consumer

Reliability

Medium

Cost

High

---

Medical

Availability

High

Safety

High

Radiation

Low

---

Dependability therefore becomes application-dependent.

---

# Dependability Profile

Instead of categorizing by industry,

characterize applications through measurable properties.

Possible parameters

Mission duration

Maintenance accessibility

Radiation exposure

Temperature extremes

Power constraints

Safety criticality

Availability requirements

Repair cost

Failure consequence

Redundancy

Environmental stress

This profile drives the testing policy.

---

# Risk-Based Fault Prioritization

Instead of

testing every fault equally,

estimate

```text
Risk

=

Probability

×

Consequence
```

The application changes

Consequence

therefore

fault priorities change.

Example

Space

SEU

Very High

Consumer

SEU

Very Low

The circuit is identical.

Only the application changed.

---

# Evidence-Generating Actions

The unit of optimization should **not** be

* ATPG vectors

nor

* fault models

Instead,

optimize

Evidence-Generating Actions.

Examples

ATPG pattern set

Scan campaign

Burn-in

Radiation testing

Delay testing

Fault injection

PVT characterization

BIST

On-chip monitoring

Each action produces evidence with

* cost
* duration
* expected information gain

---

# Test Policy Synthesis

The workflow becomes

```text
Application Profile
          ↓
Dependability Objectives
          ↓
Risk Model
          ↓
Fault Prioritization
          ↓
Evidence Value Estimation
          ↓
Test Policy Synthesis
          ↓
Adaptive Execution
          ↓
Confidence Update
          ↓
Stopping Decision
```

ATPG becomes one component of a larger decision framework.

---

# Stopping Criterion

Traditional

Run every planned test.

Proposed

Run until

Dependability Confidence

reaches

Application Threshold.

Therefore

test duration becomes

a decision variable.

---

# Three Thought Experiments

## Scenario 1

Unknown application

Objective

Maximize expected dependability over unknown deployment scenarios.

Prioritize

Common manufacturing defects

General-purpose robustness

Low-cost testing

---

## Scenario 2

Space

Objective

Minimize mission failure probability.

Additional testing

Radiation

SEU

TID

Long burn-in

Aging

Recovery testing

TMR verification

Testing cost is secondary.

Mission success dominates.

---

## Scenario 3

Medical

Objective

Maximize clinical dependability.

Prioritize

Signal integrity

Delay faults

Availability

Calibration

EMC

Radiation testing becomes lower priority (depending on the specific device), but not necessarily eliminated.

The framework should **de-prioritize** evidence with low expected value rather than completely ignore a fault class.

---

# Machine Learning Role

ML should **not replace ATPG**.

Instead,

ML synthesizes testing policy.

Inputs

Application profile

Manufacturing history

Yield

Layout

Wafer data

PVT

Previous tests

↓

ML predicts

Optimal Next Evidence Action

↓

Testing

↓

Confidence Update

↓

Repeat

---

# Current State of the Art

Existing literature focuses on

* Test compression
* Test compaction
* Adaptive ATPG
* Bayesian test selection
* Test ranking
* Yield prediction
* ML pass/fail prediction

Optimization objective

Fault Coverage

or

Yield

This research instead proposes optimizing

Dependability Assurance.

---

# Potential Novelty

Not

Adaptive ATPG.

Not

ML for test reduction.

Instead

A **decision-theoretic framework** where

testing actions are selected according to

their expected contribution toward

application-specific dependability assurance.

---

# Expected Mathematical Direction

Possible mathematical tools

Bayesian Inference

Bayesian Experimental Design

Expected Value of Information

Mutual Information

Sequential Decision Theory

Partially Observable Markov Decision Processes

Reinforcement Learning

Multi-objective Optimization

Information Theory

---

# Open Research Questions

## RQ1

How should Dependability be mathematically represented?

Vector?

Utility function?

Bayesian confidence?

Belief function?

---

## RQ2

How should application profiles be defined?

Which measurable properties best characterize deployment requirements?

---

## RQ3

How should evidence value be quantified?

Possible candidates

Expected Information Gain

Entropy Reduction

Expected Value of Information

Risk Reduction

---

## RQ4

How should confidence be updated after each testing action?

Bayesian updating?

Belief propagation?

Sequential hypothesis testing?

---

## RQ5

How should stopping criteria be defined?

Confidence threshold?

Risk threshold?

Economic threshold?

Certification threshold?

---

## RQ6

How can mandatory certification tests coexist with adaptive testing?

Possible solution

Mandatory Tests

*

Adaptive Tests

---

## RQ7

How should the synthesized testing policy be validated?

Simulation

Industrial benchmarks

Fault simulation

Digital twins

Historical manufacturing data

---

# Long-Term Research Goal

Develop a **Dependability-Driven Test Synthesis (DDTS)** framework capable of automatically generating application-aware testing workflows.

Instead of asking

> "Which test vector should I generate?"

the framework asks

> "Which evidence-generating action should I execute next to maximize application-specific dependability confidence while minimizing testing cost?"

The final system would accept:

* Application requirements
* Dependability objectives
* Cost constraints
* Manufacturing constraints
* Certification constraints

and automatically synthesize:

* Fault models to prioritize
* Test categories
* Test ordering
* Adaptive stopping rules
* Evidence updates
* Qualification decision

---

# Proposed Dissertation Vision

**Tentative Title**

> **Dependability-Driven Adaptive Test Synthesis for Application-Specific VLSI Manufacturing and Qualification**

**One-Sentence Thesis**

> Manufacturing and qualification testing should be treated as a sequential evidence-acquisition problem, where the optimal testing policy is synthesized from application-specific dependability objectives using probabilistic decision theory and machine learning, rather than executing a fixed set of tests designed solely to maximize fault coverage.
