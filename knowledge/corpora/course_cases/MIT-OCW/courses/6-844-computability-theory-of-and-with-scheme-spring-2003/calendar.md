- Source: https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/pages/calendar/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Calendar

[Scheme software](http://www.gnu.org/software/mit-scheme/) is required to run the .scm files in this section.

This calendar shows the weekly schedule for the course, which usually includes three lecture and group problem solving sessions per week. This calendar provides links to course notes, problem sets, and other relevant resources. These materials are also provided separately in the [readings](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/pages/readings/), [assignments](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/pages/assignments/), and [tools](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/pages/tools/) sections of this course.

### Week 1

*Wednesday* (*First day of class*)

- Course overview; no notes

### Week 2

#### Readings

- Notes 1: Proving Arithmetic Equations, pp. 1–6 ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/aeqn/))

#### Assignments

- Due at the end of Week 2:
  - Download [Scheme](http://www.gnu.org/software/mit-scheme/)
  - Download Scheme Continuation Interpreter project (Project 3 from 6.001 Fall ‘02) and submit solutions to Problems 11, 12 and 13
    - A description of continuations ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/continuations/))
    - Project 3 description ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/project3/))
    - Project 3 code
      - c-eval.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/ceval/))
      - desugar.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/desugar/))
      - meval.scm (Optional) ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/meval/))

#### Monday

- Diagnostic Questionnaire ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/diagnostic/)) and Solutions ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/diagnosticsol/))

#### Wednesday

- Problems on arithmetic equations

#### Friday

- Problems on implementing catch/throw with call-cc

### Week 3

#### Readings

- Notes 1: Proving Arithmetic Equations, final sections ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/aeqn/))

#### Wednesday

- Procedure to check a linear proof and convert between linear and tree proofs

#### Friday

- Exercise: Convert a tree proof to a substitution proof ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/subst_proof/))
- Scheme code ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/mccamanttreeproof/)) for the conversion
- Arithmetic inequalities
- Pattern matcher match.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/match/))

### Week 4

#### Readings

- Pattern matcher match.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/match/))
- Pattern-match based procedure proof-match.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/proofmatch/)) for converting a sequence-of-equations proof into a tree proof
- Notes 2: Substitution into Arithmetic Expressions ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/subst/))
- Also, from last week, see Scheme code for converting a tree proof to a substitution proof ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/mccamanttreeproof/))

#### Monday

- Structural induction proof of the Substitution Lemma and Soundness of Substitution Proofs (see Notes 2: Substitution into Arithmetic Expressions ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/subst/)))
- Intro to pattern matching, with pattern-match based procedure proof-match.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/proofmatch/)) for converting a sequence-of-equations proof into a tree proof

#### Wednesday

- Review of Notes 2: Substitution into Arithmetic Expressions ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/subst/))
- Problem for Friday: We extend Arithmetic Expressions with another case called an application
- “Doctor” program using unnested matching eliza.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/eliza/))

#### Friday

- Discussion of using match/rewrite rules to put arithmetic expressions (possibly extended with applications and a derivative operator) into canonical form. An example is in deriv-simplify-rules.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/derivsimplifyrules/)); this version uses the alphabetized sum-of-monomials canonical form rather than the one-variable-polynomial-with-polynomial-coefficients canonical form of the Notes
- Intro to Scheme Substitution Model

### Week 5

#### Readings

- Notes 3: A Scheme Substitution Model, Sections 1–6 (pp. 1–14) ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/submodel/))
- Skim the scheme programs implementing the [Scheme Substitution Model](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/pages/tools/)

#### Monday

- Bring your laptop loaded with the [files](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/pages/tools/) for running the Substitution Model
- Observe the submodel running on expressions in test-submodel.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/testsubmodel/))

#### Wednesday

- Discussion of control contexts in the Substitution Model

#### Friday

- Further example file for Substitution Model evaluation politician.scm ([SCM](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/politician/))

### Week 6

#### Readings

- Notes 4: Term Models ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/term_models/))

#### Assignments

- Due on Monday of Week 7: Problems 1–3 in Notes 4: Term Models ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/term_models/))

#### Monday

- Trivial decision procedure: Two terms are equal in all models iff they are identical
- Proving it: Introduction to term models

#### Wednesday

- Equational completeness theorem: If an equation follows logical from a set of equations, then the equation is provable using standard rules starting with the set of equations as axioms. Outline of proof using a term model

#### Friday

- Introduction to simple types

### Week 7

#### Monday

- Environment models for simple types

#### Wednesday

- Combinator formulation of environment models

#### Friday

- Term models for simple types

### Week 8

#### Assignments

- Due on Monday of Week 10: Problem Set 1 ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/pset1/))

#### Monday

- Compiling Scheme to register machines with a memory array

#### Wednesday

- Reducing RegM’s with a memory array to 2-Counter machines

#### Friday

- Semigroup word problems: Rewrite rules for 2-CM simulation

### Week 9

#### Monday

- Semigroup word problems: Confluence implies equations capture one-way rewrite rules for 2-CM simulation
- Diamond Lemma for confluence

### Week 10

#### Assignments

- Due at the end of Week 10: Problem 18 from Notes 5: Scheme Computability, Part I ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/computability/))

#### Monday

- Computability on S-expressions

#### Wednesday

- Notes 5: Scheme Computability, Part I ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/computability/))

#### Friday

- Proof that productivity inherits up many-one reducibility (≦<sub>m</sub>). Further properties of ≦<sub>m</sub>

### Week 11

#### Wednesday

- Notes 7: Counter Machines ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/counter_machines/))
- Notes 8: Semigroup Word Problems ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/semigroups/))
- Notes 9: 1st-order Theory of Concatenation ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/concatenation/))

#### Friday

- Notes 3: Scheme Substitution Model ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/submodel/))
- Notes 5: Scheme Computability, Part I ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/computability/))
- Notes 6: Scheme Computability, Part II ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/comput2/))

### Week 12

#### Assignments

- Due on Wednesday of Week 13: Final Problem Set, 6 of these 10 problem:
  - Notes 3: Scheme Substitution Model ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/submodel/)), Problems 2, 13 (which is more appropriately **a** term project ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/projects/))), 14
  - Notes 5: Scheme Computability, Part I ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/computability/)) , Problem 21 – not Problem 22; Problem 22 can be a term project ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/projects/))
  - Notes 6: Scheme Computability, Part II ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/comput2/)), Problems 1, 5, 6, 7, 8, 9

#### Monday

- Course projects ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/projects/))

#### Wednesday

- Halting Problem for 2-Counter Machines ≤<sub>m</sub> Th(∑*, ·) ≤<sub>m</sub> Th({1,2}*, ·) ≤<sub>m</sub> Th(N,+,×, ≦) ≡<sub>m</sub> Th(Z,+,-, ×, ≦),

where Th(*M*) denotes the 1st-order formulas valid in model *M*

#### Friday

- Complete proof that [2-CM Halting Problem ≤<sub>m</sub> Th(∑*, ·)]
- Observe that Halts reduces to the set of closed formulas of the form ∃z.G where all quantifiers in G range over subwords of *z*

### Week 13

#### Assignments

- Due at the beginning of this week: Course project ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/projects/)) proposals

#### Monday

- Topic: Diophantine sets over the integers and naturals; closure under intersection. Primes ≠ range(*g*) for any polynomial, *g*

#### Wednesday

- MIN<sub>Scheme</sub> ≡<sub>T</sub> Halts. Sketch of relative computability: The jump operation

#### Friday

- Diophantine Predicates closed under ∧, ∨, ∃, but not ¬ (negation)
- A Diophantine polynomial whose nonnegative range is the nonprimes

### Week 14

#### Assignments

- Due at the end of this week: Term project ([PDF](https://ocw.mit.edu/courses/6-844-computability-theory-of-and-with-scheme-spring-2003/resources/projects/))

#### Monday

- Excerpt: pp. 174–181 on Undecidability of Exponential Diophantine Polynomials, from Jones, Neil D. “Computability and Complexity: from a Programming Perspective,” MIT Press, c. 1997, 466pp.

#### Wednesday (Last class)

- Term project
