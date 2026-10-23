- Source: https://ocw.mit.edu/courses/6-7220j-nonlinear-optimization-spring-2025/pages/calendar/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Calendar

The course is roughly divided into three interconnected parts:

- Part I will focus on the characterization of optimal points from an analytic point of view. In particular, we will develop analytic techniques to find and certify optimal points in convex and nonconvex problems.
- Part II will focus on gradient-based optimization methods in convex and nonconvex problems.
- Part III will focus on preconditioned algorithms, second-order algorithms, or more generally algorithms that exploit the geometry of the objective function beyond its mere gradient.

#### Lecture 1: Introduction

*Topics:* Overview of the course material; goals and applications; general form of an optimization problem; Weierstrass’s theorem; computational considerations.

### Part I: Nonlinear Optimization Theory

#### Lecture 2: First-order optimality conditions

*Topics:* First-order necessary optimality conditions; the unconstrained case; halfspace constraints.

*Key Dates:* Homework 1 out

#### Lecture 3: More on normal cones, and a first taste of duality

*Topics:* The connection between normal cones and Lagrange multipliers; linear programming duality as a straightforward consequence of normal cones.

#### Lecture 4: Convex functions and sufficiency of normal cones

*Topics:* Definition of convexity for functions; local optimality implies global optimality; sufficiency of first-order optimality conditions; how to recognize a convex function.

#### Lecture 5: The driver of duality: separation

*Topics:* Feasibility as minimization of distance from the feasible set; how separation implies the normal cone to the intersection of halfspaces.

#### Lecture 6: Separation as a proof system

*Topics:* Primer on computational complexity; the class NP coNP and its significance; certificate of infeasibility and Farkas’s lemma.

*Key Dates*: Homework 2 out

#### Lecture 7: Functional constraints, Lagrange multipliers, and KKT conditions

*Topics:* Optimization problems with functional constraints; Lagrangian function and Lagrange multipliers; constraint qualifications (linear independence of constraint gradients, Slaters condition).

#### Lecture 8: Lagrangian duality

*Topics:* Lagrangian function; connections with KKT conditions; dual problem; examples.

#### Lecture 9: Conic constraints

*Topics:* Conic programs and notable cases: linear programs, second-order cone programs, semidefinite programs; selected applications.

#### Lecture 10: Polynomial optimization

*Topics:* Polynomial optimization problems; connection between polynomial optimization and semidefinite programming; the sum of squares decomposition.

*Key Dates:* Homework 3 out

#### Lecture 11: Polarity and oracle equivalence

*Topics:* Duality between optimization and separation; polar and bipolar.

#### Session: Midterm review

#### Session: In-class midterm

*Key Dates:* Midterm exam

### Part II: Algorithms based on first-order information

#### Lecture 12: Gradient descent and descent lemmas

*Topics:* Gradient descent algorithm; smoothness and the gradient descent lemma; computation of a point with small gradient in general (non-convex) functions; descent in function value for convex functions: the Euclidean mirror descent lemma.

#### Lecture 13: Acceleration and momentum

*Topics:* The idea of momentum; Nesterov’s accelerated gradient descent; Allen-Zhu and Orecchia’s accelerated gradient descent; practical considerations.

*Key Dates:* Homework 4 out

#### Lecture 14: Projected gradient descent and mirror descent (Part I)

*Topics:* The projected gradient descent (PGD) algorithm; distance-generating functions and Bregman divergences; proximal steps and their properties; the mirror descent algorithm; descent lemmas for mirror descent.

#### Lecture 15: Projected gradient descent and mirror descent (Part II)

*Topics:* The projected gradient descent (PGD) algorithm; distance-generating functions and Bregman divergences; proximal steps and their properties; the mirror descent algorithm; descent lemmas for mirror descent.

#### Lecture 16: Stochastic gradient descent and empirical risk minimization

*Topics:* Practical importance of stochastic gradient descent with momentum in training deep learning models; empirical risk minimization problems; minibatches; stochastic gradient descent lemmas; the effect of variance.

*Key Dates:* Homework 5 out

#### Lecture 17: Distributed optimization and ADMM [Optional]

*Topics:* The setting of distributed optimization; the alternating direction method of multipliers (ADMM) algorithm; convergence analysis of ADMM in the case of convex functions.

### Part III: Preconditioning and higher-order information

#### Lecture 18: Hessians, preconditioning, and Newton’s method

*Topics:* Local quadratic approximation of objectives; Newton’s method; local quadratic convergence rate; global convergence for certain classes of functions; practical considerations.

#### Lecture 19: Adaptive preconditioning: AdaGrad and ADAM

*Topics:* Adaptive construction of diagonal preconditioning matrices; the AdaGrad algorithm; the convergence rate of AdaGrad; proof sketch; AdaGrad with momentum: the popular ADAM algorithm.

#### Lecture 20: Self-concordant functions (Part I)

*Topics:* Limitations of the classic analysis of Newton’s method; desiderata and self-concordant functions; properties and examples.

*Key Dates:* Homework 6 out

#### Lecture 21: Self-concordant functions (Part II)

*Topics:* Limitations of the classic analysis of Newton’s method; desiderata and self-concordant functions; properties and examples.

#### Lecture 22: Central path and interior-point methods (Part I)

*Topics:* Central path; barriers and their complexity parameter; the short-step barrier method; proof sketch.

#### Lecture 23: Central path and interior-point methods (Part II)

*Topics:* Central path; barriers and their complexity parameter; the short-step barrier method; proof sketch.

#### Session: Final exam review

#### Session: In-class final

*Key Dates:* Final exam
