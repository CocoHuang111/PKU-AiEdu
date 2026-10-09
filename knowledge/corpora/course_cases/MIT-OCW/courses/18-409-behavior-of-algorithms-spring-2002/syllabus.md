- Source: https://ocw.mit.edu/courses/18-409-behavior-of-algorithms-spring-2002/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Course Description

In this course, we will discuss rigorous approaches to explaining the typical performance of algorithms. In particular, we examine alternatives to the traditional worst-case and average-case analyses. Such analyses must necessarily make assumptions about the inputs to algorithms.

We will develop this theory together, and I expect we will debate the merits of various approaches, as well as the names I have tentatively assigned to them.

My lectures will center around the following three approaches.

#### Smoothed Analysis

Analyzing algorithms assuming their inputs are subject to noise. That is, we measure the maximum over inputs of the expected performance of an algorithm under slight random perturbations of those inputs. This is the intersection of [Shannon Theory (PDF)](http://worrydream.com/refs/Shannon%20-%20A%20Mathematical%20Theory%20of%20Communication.pdf) with Analysis of Algorithms by assuming inputs come through a noisy channel.

#### Condition Numbers/Parametric Analysis

In this approach, we find a simple parameter of the input that is predictive of the running time of the algorithm. This parameter should be significantly simpler than “the running time of the algorithm”.

Examples could include

- Feature size of point sets
- Condition numbers of matrices or polynomial
- Bit length of inputs

#### Subclassing Inputs

In many practical problem domains, the inputs to algorithms have special structure, and may form a proper subclass of the possible inputs. If it is known an algorithm in a particular application only sees inputs from this subclass, then it is natural to analyze the performance of this algorithm on the subclass.

### Homework and Projects

Students will perform class projects examining the applicability of these analyses to some problem area, and will present their findings to the class as well as writing up their findings. Some students may wish to choose their project from a list of tractable open problems that will be circulated within the class.

Students will also be responsible for scribing lectures.

### Prerequisites

At least one graduate course in algorithms or numerical analysis.
