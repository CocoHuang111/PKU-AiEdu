- Source: https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-analysis-and-numerics-fall-2014/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 3 sessions / week, 1 hour / session

### Prerequisites

[*18.06 Linear Algebra*](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010), [*18.700 Linear Algebra*](https://ocw.mit.edu/courses/18-700-linear-algebra-fall-2013) or equivalent.

### Description

This course provides students with the basic analytical and computational tools of linear partial differential equations (PDEs) for practical applications in science engineering, including heat/diffusion, wave, and Poisson equations.

Analytics emphasize the viewpoint of linear algebra and the analogy with finite matrix problems including operator adjoints and eigenproblems, series solutions, Green’s functions, and separation of variables.

Numerics focus on finite-difference and finite-element techniques to reduce PDEs to matrix problems, including stability and convergence analysis and implicit/explicit time-stepping.

[Julia programming language](https://github.com/JuliaLang/julia) (a MATLAB®-like environment) is introduced and used in homework for simple examples. Julia is a high-level, high-performance dynamic language for technical computing, with syntax that is familiar to users of other technical computing environments. It provides a sophisticated compiler, distributed parallel execution, numerical accuracy, and an extensive mathematical function library.

### Textbook

There is no required text for this course, though the following books are recommended:

Strang, Gilbert. *Computational Science and Engineering*. Wellesley-Cambridge Press, 2007. ISBN: 9780961408817.
(emphasizing more the numerical part of the course). More information, including online chapters, can be found on [Prof. Strang’s CSE website](http://math.mit.edu/~gs/cse/).

Olver, Peter. [*Introduction to Partial Differential Equations*](https://www.amazon.com/Introduction-Differential-Equations-Undergraduate-Mathematics/dp/3319020986). Springer, 2013. ISBN: 9783319020983. [Preview with [Google Books](http://books.google.com/books?id=aQ8JAgAAQBAJ&pg=PAfrontcover)] (free online book)

### Requirements

There will be five problem sets and a mid-term exam. There is a final project instead of a final exam. Late problem sets are not accepted, however the lowest problem set score will be dropped at the end of the term.

### Grading

| ACTIVITIES | PERCENTAGES |
| --- | --- |
| Assignments | 45% |
| Midterm exam | 25% |
| Final project | 30% |

### Calendar

<table><tr><th>SES #</th><th>TOPICS</th><th>KEY DATES</th></tr><tr><td>L1</td><td>Overview of linear PDEs and analogies with matrix algebra</td><td></td></tr><tr><td>L2</td><td>Poisson’s equation and eigenfunctions in 1d: Fourier sine series</td><td></td></tr><tr><td>L3</td><td>Finite-difference methods and accuracy</td><td></td></tr><tr><td>L4</td><td>Discrete vs. continuous Laplacians: Symmetry and dot products</td><td></td></tr><tr><td>Optional</td><td colspan="2">Julia Tutorial</td></tr><tr><td>L5</td><td>Diagonalizability of infinite-dimensional Hermitian operators</td><td>Problem set 1 due</td></tr><tr><td>L6</td><td>Start with a truly discrete (finite-dimensional) system, and then derive the continuum PDE model as a limit or approximation</td><td></td></tr><tr><td>L7</td><td>Start in 1d with the “Sturm-Liouville operator”, generalize Sturm-Liouville operators to multiple dimensions</td><td></td></tr><tr><td>L8</td><td>Music and wave equations, Separation of variables, in time and space</td><td>Problem set 2 due</td></tr><tr><td>L9</td><td>Separation of variables in cylindrical geometries: Bessel functions</td><td></td></tr><tr><td>L10</td><td>General Dirichlet and Neumann boundary conditions</td><td></td></tr><tr><td>L11</td><td>Multidimensional finite differences</td><td></td></tr><tr><td>L12</td><td>Kronecker products</td><td>Problem set 3 due</td></tr><tr><td>L13</td><td>The min-max theorem</td><td></td></tr><tr><td>L14</td><td>Green’s functions with Dirichlet boundaries</td><td></td></tr><tr><td>L15</td><td>Reciprocity and positivity of Green’s functions</td><td></td></tr><tr><td>L16</td><td>Delta functions and distributions</td><td></td></tr><tr><td>L17</td><td>Green’s function of ∇ <br> 2 <br> in 3d for infinite space, the method of images</td><td>Problem set 4 due</td></tr><tr><td>L18</td><td>The method of images, interfaces, and surface integral equations</td><td></td></tr><tr><td>L19</td><td>Green’s functions in inhomogeneous media: Integral equations and Born approximations</td><td></td></tr><tr><td>L20</td><td>Dipole sources and approximations, Overview of time-dependent problems</td><td></td></tr><tr><td>L21</td><td>Time-stepping and stability: Definitions, Lax equivalence</td><td></td></tr><tr><td>L22</td><td>Von Neumann analysis and the heat equation</td><td>Problem set 5 due</td></tr><tr><td>L23</td><td>Algebraic properties of wave equations and unitary time evolution, Conservation of energy in a stretched string</td><td></td></tr><tr><td>L24</td><td>Staggered discretizations of wave equations</td><td></td></tr><tr><td>L25</td><td>Traveling waves: D’Alembert’s solution</td><td></td></tr><tr><td>L26</td><td>Group-velocity derivation, Dispersion</td><td></td></tr><tr><td colspan="3">Midterm Exam</td></tr><tr><td>L27</td><td>Material dispersion and convolutions</td><td></td></tr><tr><td>L28</td><td>General topic of waveguides, Superposition of modes, Evanescent modes</td><td></td></tr><tr><td>L29</td><td>Waveguide modes, Reduced eigenproblem</td><td></td></tr><tr><td>L30</td><td>Guidance, reflection, and refraction at interfaces between regions with different wave speeds</td><td></td></tr><tr><td>L31</td><td>Numerical examples of total internal reflection</td><td></td></tr><tr><td>L32</td><td>Perfectly matched layers (PML)</td><td></td></tr><tr><td>L33</td><td>Perturbation theory and Hellman-Feynman theorem</td><td></td></tr><tr><td>L34</td><td>Finite element methods: Introduction</td><td></td></tr><tr><td>L35</td><td>Galerkin discretization</td><td></td></tr><tr><td>L36</td><td>Convergence proof for the finite-element method, Boundary conditions and the finite-element method</td><td></td></tr><tr><td>L37</td><td>Finite-element software</td><td></td></tr><tr><td>L38</td><td>Symmetry and linear PDEs</td><td>Final project due</td></tr></table>
