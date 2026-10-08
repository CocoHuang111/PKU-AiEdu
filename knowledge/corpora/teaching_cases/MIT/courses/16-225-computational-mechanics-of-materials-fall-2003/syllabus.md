> 检索摘要：16.225 Computational Mechanics of Materials（Fall 2003，Graduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Learning Objectives；Measurable Outcomes；Prerequisites；Lectures；Recitations；Course Work；Homework Assignments；Assessment of Student Performance；Bibliography。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/16-225-computational-mechanics-of-materials-fall-2003/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

Recitations: 1 session / week, 1.5 hours / session

### Learning Objectives

16.225 is a graduate level course on Computational Mechanics of Materials. The primary focus of this course is on the teaching of state-of-the-art computational methods for the modeling and simulation of the mechanical response of engineering materials used in aerospace as well as in other branches of engineering including mechanical and civil engineering, material science and biomechanics. The range of material behavior considered includes: finite deformation elasticity and inelasticity, contact, friction and coupled problems. Numerical formulation and algorithms include: Variational formulation and variational constitutive updates, finite element discretization, mesh generation, error estimation, constrained problems, time discretization and convergence analysis. There will be a strong emphasis on the (parallel) computer implementation of algorithms in programming assignments. At the beginning of the course, the students will be given the source of a base code with all the elements of a finite element program which constitute overhead and do not contribute to the learning objectives of this course (assembly and equation-solving methods, etc.). Each assignment will consist of formulating and implementing on this basic platform, the increasingly complex algorithms resulting from the theory given in class, as well as in using the code to numerically solve specific problems. The application to real engineering applications and problems in engineering science will be stressed throughout. 16.225 has a specific set of learning objectives. Students graduating from 16.225 will be able to:

1. **Formulate** numerical (finite element) approximations to the equations of motion governing the large, possibly dynamic, deformations of continua.
2. **Formulate** variational update algorithms for the integration of the constitutive equations modeling a wide range of material behavior, including finite elasticity, plasticity and rate-dependency.
3. **Implement** the resulting algorithms in a computer program.
4. **Apply** the computer program to the solution of concrete engineering science and engineering design problems.

### Measurable Outcomes

The achievement of the learning objectives in 16.225 will be measured through the students’ ability to:

1. apply the mathematical tools of tensor calculus to the analysis of the nonlinear kinematics of deforming continua,
2. explain the large nonlinear deformations of continua through the local Lagrangian analysis of deformation,
3. formulate the Lagrangian equations of motion of deforming continua in integral and differential form,
4. formulate the Principle of Virtual Displacements for deforming continua,
5. explain stress and strain measures and work-conjugacy relationships,
6. explain constitutive theory and apply it to the formulation of appropriate models of finite elasticity, plasticity and viscosity, explain the basic elements of finite element theory, including its ability to provide approximate solutions to problems of deforming continua,
7. explain the formulation of and implement in a computer program isoparametric finite element models of three-dimensional deforming continua,
8. explain the locking phenomenon in the finite element formulation of constrained problems,
9. estimate a *priori* the convergence error of finite element solutions of linear problems,
10. implement a *priori* estimates of the convergence error of finite element solutions of linear problems and use them to
11. evaluate the error in finite element calculations of elasticity problems with known analytical solution and confirm the theoretical estimates,
12. explain the basic elements of a general purpose finite element program, implement on a computer program advanced algorithms of complex constitutive material models in finite element codes, explain Newton’s algorithm for the solution of nonlinear systems of algebraic equations,
13. read scientific articles in the field of Computational Mechanics of Materials understanding relevant in-depth details,
14. conduct research towards a Graduate Degree in various engineering Departments at MIT that either requires the educated application of currently available tools of Computational Mechanics of Materials or seeks to further expand this area of research.

### Prerequisites

Undergraduate mechanics background or permission of the instructor, some programming experience in any of the following languages: Python, C++, C or Fortran.

### Lectures

There will be two lectures of one and a half hours a week. Student attendance is necessary to maximize the learning experience.

### Recitations

Recitations will be used for answering questions related to the homework assignments, explanations of the computer software **sumMIT** developed for this course, software issues on the athena cluster.

### Course Work

The course work involved in 16.225 includes homework assignments.

### Homework Assignments

A total of approximately six (6) problem sets and computer assignments will be given on Wednesdays and on a bi-weekly basis. The due date for submission of assignments is at the beginning of class two Wednesdays after the assignment is given. Late submission of assignments is not accepted. The assignments will consist of specific exercises of algorithm formulation on paper, their computer implementation in programming exercises and their testing in specific applications. At the beginning of the course, the students will be given the source of a base code sumMIT with all the elements of a finite element program which constitute overhead and do not contribute to the learning objectives of this course (assembly and equation-solving methods, etc.). Electronic homework submissions are strongly recommended. Students are strongly encouraged to discuss homework problems in groups, since this is expected to help the learning process. However, homework assignments are also used for performance assessment and, therefore, the material that is turned in must represent the student’s own understanding of the material.

### Assessment of Student Performance

Students are strongly encouraged to discuss homework problems with each other, since this is expected to help the learning process. However, homework assignments are also used for performance assessment and, therefore,the material that is turned in must represent the student’s own understanding of the material. The final letter grades will be assigned according to the rules and regulations of the Faculty.

### Bibliography

Textbooks on Continuum Mechanics and Mathematical Theory of Elasticity:

1. Marsden, J. E., and T. J. R. Hughes. *Mathematical Foundations of Elasticity.* Prentice-Hall, 1983.
2. Malvern, L. E. *Introduction to the Mechanics of a Continuous Medium.* Prentice-Hall, 1969.
3. Gurtin, M. E. *An Introduction to Continuum Mechanics.* Academic Press, 1981.

Textbooks on the finite element method:

1. Bathe, K. J. *Finite Element Procedures.* Prentice Hall, 1996.
2. Hughes, T. J. R. *The Finite Element Method, Linear Static and Dynamic Finite Element Analysis.* Dover.
3. Zienkiewicz, O. C., and R. L. Taylor. *The Finite Element Method.* Mc-Graw Hill, 1989.
