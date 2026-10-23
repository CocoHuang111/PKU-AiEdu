- Source: https://ocw.mit.edu/courses/16-s498-risk-aware-and-robust-nonlinear-planning-fall-2019/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Sessions: 1 session / week, 2 hours / session

### Course Description

Concern for safety is one of the dominant issues that arises in planning in the presence of uncertainties and disturbances. This course addresses advanced probabilistic and robust optimization-based techniques to safely control and analyze nonlinear dynamical systems in the presence of uncertainties. Specifically, we will learn how to leverage rigorous mathematical tools, such as the theory of measures and moments, the theory of nonnegative polynomials, and semidefinite programming to develop convex optimization formulations to control and analyze uncertain nonlinear dynamical systems with applications in autonomous systems and robotics. Students will acquire a comprehensive overview of state-of-the-art techniques for polynomial optimization and will be able to implement the algorithms using related open-source packages. Evaluation will be based on problem sets and a final individual or team research project.

This course introduces optimization methods of semidefinite programs for:

1. Nonlinear Chance Optimization,
2. Nonlinear Chance-Constrained Optimization,
3. Nonlinear Robust Optimization, and
4. Nonlinear Distributionally Robust Chance Constrained Optimization.

The applications of the programs include:

1. Probabilistic and Robust Nonlinear Safety Verification,
2. Risk Aware Control of Probabilistic Nonlinear Dynamical Systems, and
3. Robust Control of Uncertain Nonlinear Dynamical Systems.

### Prerequisites

*Linear Algebra* (e.g., [*18.06*](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010)), *Convex Optimization* (e.g., *6.215*, *[6.251](https://ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009)*, *[6.255](https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009)*), *Probability Theory* (e.g., *[6.431](https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010)*), *Dynamical Systems* (e.g., *[6.241](https://ocw.mit.edu/courses/6-241j-dynamic-systems-and-control-spring-2011)*) or permission of the instructor for MIT students.

### Grading Policy

| ACTIVITIES | PERCENTAGES |
| --- | --- |
| Problem Sets | 50% |
| Research Project | 50% |

### Code Repository

The codes of the lectures are available on the [fall 2019 course website on GitHub](https://github.com/jasour/rarnop19). To run the codes you need the following packages:

1. [GloptiPoly 3](https://homepages.laas.fr/henrion/software/gloptipoly/)
2. [Yalmip](https://yalmip.github.io/download/)
3. SDP solvers like “[Mosek](https://www.mosek.com/downloads/)” or “[SeDuMi](https://sedumi.ie.lehigh.edu/?page_id=58)”
