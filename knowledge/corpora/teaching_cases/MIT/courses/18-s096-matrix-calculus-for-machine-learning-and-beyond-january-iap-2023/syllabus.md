> 检索摘要：18.S096 Matrix Calculus for Machine Learning and Beyond（January IAP 2023，Undergraduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Prerequisites；Course Description；Lecture Notes；Topics；Grading。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 3 sessions / week, 2 hours / session

### Prerequisites

Courses in linear algebra (such as [*18.06 Linear Algebra*](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/)) and multivariate calculus (such as [*18.02 Multivariable Calculus*](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/))

### Course Description

We all know that calculus courses such as [*18.01 Single Variable Calculus*](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/) and [*18.02 Multivariable Calculus*](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) cover univariate and vector calculus, respectively. Modern applications such as machine learning and large-scale optimization require the next big step, “matrix calculus” and calculus on arbitrary vector spaces.

This class covers a coherent approach to matrix calculus showing techniques that allow you to think of a matrix holistically (not just as an array of scalars), generalize and compute derivatives of important matrix factorizations and many other complicated-looking operations, and understand how differentiation formulas must be reimagined in large-scale computing. We will discuss reverse/adjoint/backpropagation differentiation, custom vector-Jacobian products, and how modern automatic differentiation is more computer science than calculus (it is neither symbolic formulas nor finite differences).

### Lecture Notes

There is no required textbook for this course, but a [complete set of lecture notes](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec_full_pdf/) is provided. The lecture notes were prepared by Paige Bright under the guidance of Professors Edelman and Johnson. The notes are also available on [arXiv.org](https://arxiv.org/abs/2501.14787), along with any updates and citing information.

### Topics

Here are some of the topics covered:

- Derivatives as linear operators and linear approximation on arbitrary vector spaces: beyond gradients and Jacobians.
- Derivatives of functions with matrix inputs and/or outputs (e.g. matrix inverses and determinants). Kronecker products and matrix “vectorization.”
- Derivatives of matrix factorizations (e.g. eigenvalues/SVD) and derivatives with constraints (e.g. orthogonal matrices).
- Multidimensional chain rules, and the significance of right-to-left (“forward”) vs. left-to-right (“reverse”) composition. Chain rules on computational graphs (e.g. neural networks).
- Forward- and reverse-mode manual and automatic multivariate differentiation.
- Adjoint methods (vJp/pullback rules) for derivatives of solutions of linear, nonlinear, and differential equations.
- Application to nonlinear root-finding and optimization. Multidimensional Newton and steepest–descent methods.
- Applications in engineering/scientific optimization and machine learning.
- Second derivatives, Hessian matrices, quadratic approximations, and quasi-Newton methods.

### Grading

The course grade is based on performance on the two homework assignments.
