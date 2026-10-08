> 检索摘要：18.086 Mathematical Methods for Engineers II（Spring 2006，Graduate）的「Projects」。页内标题：Projects；Project Overview；Project 1；Computational Project Topics Students Chose this Term；Sample Project from 2006；Sample Project from 2005。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### Project Overview

18.086 has two main parts, Initial Value Problems and Solving Large Linear Systems. The lectures will present the underlying theory and many of the key algorithms for these important problems.

A project on Part 1 is due the day after spring break. A project on Part 2 is due before the end of the semester, with a brief oral report to the class. The scope of the projects will be discussed in class.

### Project 1

Many projects will move to 2 or 3 space dimensions or nonlinear problems like conservative laws, starting in 1 space dimension.

(Area 1) Numerical methods for initial-value problems
(Area 2) Direct and iterative methods for large systems Ax=b

In area 1, the first questions will be similar to the recent homework, but in more dimensions. Implicit methods may need an idea from area 2. Shocks and fans in 2D would be extremely interesting. (Even in 1D, how well does a difference method show the fan+shock solution when u(x,0)= δ(x)?)

In area 2, experiments are badly needed on reordering the linear system to reduce fill-in, which is counted by nnz(L) and nnz(U). Compare minimum degree software, estimate or prove on estimate for fill-in and flop count as N increases (dimensions 2 and 3). Last year’s final project on multi-grid by Joseph Kovac can be seen below. That would have ideas for this year’s first project (not as extensive of a final project). How is multi-grid affected by a first-difference matrix which might be one-sided, or centered and anti-symmetric, coming from implicit convection-diffusion? Does multi-grid break down when convection dominates diffusion? Also experiments on Incomplete LU using luinc and cholinc with different tolerances. Good preconditioner for iterative methods? Dependence on the choice of tolerance?

### Computational Project Topics Students Chose this Term

- Solving the 2D Diffusion Equation with the Alternating Direction ADI Method
- Experimental Analysis of the Two Dimensional Laplacian Matrix (K2D): Application and Reordering Algorithms
- Finite Difference Methods for the Hyperbolic Wave Partial Differential Equations
- Minimum Degree and Nested Dissection
- Convection-Diffusion Equation
- Conservation Laws
- Multigrid Method
- Investigations into Direct Methods for Solving Large Sparse Systems of Linear Equations
- Thermal Analysis of the Heating of a Fiber Optic via Concentrated Solar Energy
- The Korteweg-deVries Equation: A Brief Look at Numerical Solutions to the KdV Equation for Waves in Shallow Water
- Numerical Methods for Initial-value Problems
- Comparison of Multigrid Methods for the One-Dimensional Convection-Diffusion Equation
- Finite Difference Acoustics Modeling for Waveguide Loudspeaker Design
- Poisson-Boltzmann Equation
- Efficiently Solving the Two-way Wave Equation
- 2D Wave Equation and Navier-Stokes Equations
- The 2D Wave Equation Using Centered Second Differences
- Solving the 2D Convection-Diffusion Equation with Multigrid Methods
- A Look into Solving Ax=b for K and K2D Matrix Structures
- Extrapolation of Two Numerical Methods into Two Dimensions with Application to the Conservation Law
- Numerical Methods for Partial Differential Equations in 2 Spatial Dimensions

### Sample Project from 2006

This sample project is courtesy of Jose A. Dominguez-Caballero, a student in the class, and is used with permission.

Experimental Analysis of the Two Dimensional Laplacian Matrix (K2D): Applications and Reordering Algorithms ([PDF - 1.3 MB](https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/resources/project1domnguez/))

### Sample Project from 2005

This sample project is courtesy of Joseph Kovac, a student in the class, and is used with permission. The project implements a 2D multigrid solver for Laplace’s and Poisson’s equation.

Overview of Multi-grid Project ([PDF](https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/resources/overview/))

Project File: The Fundamentals and Advantages of Multigrid Techniques ([PDF](https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/resources/josephkovacpro/))

Matlab_Files_for_Project.zip ([ZIP](https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/resources/matlab_files_for_project/)) (The ZIP file contains: 10 .m files.)
