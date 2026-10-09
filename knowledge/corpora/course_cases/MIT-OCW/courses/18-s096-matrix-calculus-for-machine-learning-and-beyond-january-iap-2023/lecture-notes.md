- Source: https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/pages/lecture-notes-and-readings/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Lecture Notes and Readings

Lecture notes were prepared by Paige Bright under the guidance of Professors Edelman and Johnson. [Full Course Notes (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec_full_pdf/)
The notes are also available on [arXiv.org](https://arxiv.org/abs/2501.14787), along with any updates and citing information.

### Lecture 1

#### Outline

**Part 1:** Overview, applications, and motivation.

**Part 2:** Rethinking derivatives as linear operators: f(x + dx) - f(x) = df = f′(x)[dx] — f′ is the [linear operator](https://en.wikipedia.org/wiki/Linear_map) that gives the change df in the output from a “tiny” change dx in the inputs, to first order in dx (i.e. dropping higher-order terms). When we have a scalar function f(x) ∈ ℝ of vector inputs x ∈ ℝⁿ, then this gives us a “row vector” f′(x) since f′(x)dx is a scalar, which we interpret as the transpose of the gradient ∇f (which we call a “column” vector), i.e. df = (∇f) ⋅ dx = (∇f)ᵀdx. When we have a vector function f(x) ∈ ℝᵐ of vector inputs x ∈ ℝⁿ, then f’(x) is a linear operator that takes n inputs to m outputs, which we can think of as an m × n matrix called the [Jacobian matrix](https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant) (typically covered only superficially in [*18.02 Multivariable Calculus*](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/).)

#### Lecture Notes and Slides

- *Course notes: Chapter 1, and Chapter 2, Sections 2.1–2.3*
- Chapter 1: [Lecture 1, Part 1 Notes: Overview and Motivation (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec01_pdf/)
- Part 1 Slides: [Introduction (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec1_pdf/)
- Chapter 2: [Lecture 1, Part 2 Notes: Derivatives as Linear Operators (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec02_pdf/)

#### Further Readings

- [matrixcalculus.org](http://www.matrixcalculus.org/) is a fun site to play with derivatives of matrix and vector functions.
- [*The Matrix Cookbook* (PDF)](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf) has a lot of formulas for these derivatives, but no derivations.
- Notes on [Vector and Matrix Differentiation (PDF)](https://cdn-uploads.piazza.com/paste/j779e63owl53k6/04b2cb8c2f300212d723bea822a6b856085b28e28ca9debc75a05761a436499c/6.S087_Lecture_2.pdf) from *6.S087 Special Subject in Electrical Engineering and Computer Science* (IAP 2021) are helpful.
- **Fancier math:** The perspective of derivatives as linear operators is sometimes called a [Fréchet derivative](https://en.wikipedia.org/wiki/Fr%C3%A9chet_derivative) and you can find lots of very abstract (what I’m calling “fancy”) presentations of this online, chock full of weird terminology whose purpose is basically to generalize the concept to weird types of vector spaces. The “little-o notation” o(δx) we’re using here for “infinitesimal asymptotics” is closely related to the [Big *O* notation](https://en.wikipedia.org/wiki/Big_O_notation) used in computer science, but in computer science people are typically taking the limit as the argument (often called “n”) becomes very large instead of very small. A fancy name for a row vector is a “covector” or [linear form](https://en.wikipedia.org/wiki/Linear_form), and the fancy version of the relationship between row and column vectors is the [Riesz representation theorem](https://en.wikipedia.org/wiki/Riesz_representation_theorem), but until you get to non-Euclidean geometry you may be happier thinking of a row vector as the transpose of a column vector.

### Lecture 2

#### Outline

**Part 1:** Continued discussing derivatives as linear operators, starting with Jacobian matrices. Reviewed the sum rule d(f + g) = df + dg, the product rule d(fg) = (df)g + f(dg), and the chain rule for f(g(x)) (f’(x) = g’(h(x))h’(x), where this is a composition of two linear operations, performing h’ then g’ — g’h’ ≠ h’g’!). For functions from vectors to vectors, the chain rule is simply the product of Jacobians. Moreover, as soon as you compose 3 or more functions, it can make a huge difference whether you multiply the Jacobians from left to right (“reverse-mode”, or “backpropagation”, or “adjoint differentiation”) or right to left (“forward-mode”). Showed, for example, that if you have many inputs but a single output (as is common in machine learning and other types of optimization problems), that it is vastly more efficient to multiply left-to-right than right-to-left, and such “backpropagation algorithms” are a key factor in the practicality of large-scale optimization. Finally, began talking about functions in more general vector spaces, such as functions with **matrix inputs and/or outputs**. For example, considered f(A) = A³, giving d(A³) = f′(A)[dA] = A²(dA) + A(dA)A + (dA)A² (≠3A²dA!), and f(A) = A⁻¹, giving d(A⁻¹) = -A⁻¹(dA)A⁻¹.

**Part 2:** Began going into more detail on matrix-valued functions, and their relationship to the “Jacobian matrix” picture. Converting f′(A) to a conventional “Jacobian matrix” in such cases requires converting matrices A into column vectors vec(A), a process called “vectorization” of the matrix (by a common convention: simply stacking the matrix by columns). Linear operators like f′(A)[dA] = AdA + dAA can then be expressed as “ordinary” matrices via [Kronecker products](https://en.wikipedia.org/wiki/Kronecker_product).

#### Lecture Notes and Other Resources

- *Course notes: Chapter 2, Sections 2.4–2.6, and Chapter 3*
- Part 0: [Examples of Linear and Nonlinear Transformations of ℝ² via Images (try it online)](https://github.com/mitmath/JuliaComputation/blob/Fall23/notebooks/1_hyperbolic_corgi.jl)
- Part 1: Derivatives as Linear Operators (continued)
  - Chapter 2: [Lecture 1, Part 2 Notes: Derivatives as Linear Operators (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec02_pdf/)
- Chapter 3: [Lecture 2, Part 2 Notes: Jacobians of Matrix Functions (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec03_pdf/)
- Part 2 (Matrix Jacobians via [Vectorization](https://en.wikipedia.org/wiki/Vectorization_%28mathematics%29)): [Two by Two Matrix Jacobians (HTML)](https://rawcdn.githack.com/mitmath/matrixcalc/3f6758996e40c5c1070279f89f7f65e76e08003d/notes/2x2Jacobians.jl.html) [(Pluto notebook source code)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/2x2jacobians_jl/)

#### Further Readings

- The terms “forward-mode” and “reverse-mode” differentiation are most prevalent in [automatic differentiation](https://en.wikipedia.org/wiki/Automatic_differentiation) (AD), which we will cover later in this course.
- You can find many, many articles online about [backpropagation](https://en.wikipedia.org/wiki/Backpropagation) in neural networks.
- There are many other versions of this, e.g. in differential geometry the derivative linear operator (multiplying Jacobians and perturbations dx right-to-left) is called a [pushforward](https://en.wikipedia.org/wiki/Pushforward_%28differential%29), whereas multiplying a gradient row vector (covector) by a Jacobian left-to-right is called a [pullback](https://en.wikipedia.org/wiki/Pullback_%28differential_geometry%29).
- The video on [Understanding Automatic Differentiation (in Julia) (YouTube)](https://www.youtube.com/watch?v=UqymrMG-Qi4) by Dr. Mohamed Tarek also starts with a similar left-to-right (reverse) vs right-to-left (forward) viewpoint and goes into how it translates to Julia code, and how you define custom chain-rule steps for Julia AD.

### Lecture 3

#### Outline

**Part 1:** Continued from Lecture 2: matrix functions, Jacobians, vectorizations, and Kronecker products. More examples of matrix functions, including LU factorization and 2 × 2 eigenproblems.

**Part 2:** Finite-difference methods: viewing f(x + δx) – f(x) as an approximation for f’(x)δx on a computer. This is extremely useful as a quick check of a hand-derived derivative (which is very error-prone for complicated functions), and can also be used as a replacement for analytical derivatives in a pinch. Analyzed two sources of error: truncation error (from the non-infinitesimal δx) and roundoff error (from the finite precision of computer arithmetic).

#### Lecture Notes and Other Resources

- *Course notes: Chapter 3 and Chapter 4*
- Part 1 (Lecture 2 Part 2 continued)
  - Chapter 3: [Lecture 2, Part 2 Notes: Jacobians of Matrix Functions (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec03_pdf/)
- [Two by Two Matrix Jacobians (HTML)](https://rawcdn.githack.com/mitmath/matrixcalc/3f6758996e40c5c1070279f89f7f65e76e08003d/notes/2x2Jacobians.jl.html) [(Pluto notebook source code)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/2x2jacobians_jl/)
- Chapter 4: [Lecture 3, Part 2 Notes: Finite-Difference Approximations (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec04_pdf/)
- Part 2: [Finite Difference (Jupyter notebook)](https://nbviewer.org/urls/draft.ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/fd_checks.ipynb)

#### Further Readings

- Wikipedia has a useful list of [properties of the matrix trace](https://en.wikipedia.org/wiki/Trace_%28linear_algebra%29).
- The “matrix dot product” introduced today is also called the [Frobenius inner product](https://en.wikipedia.org/wiki/Frobenius_inner_product), and the corresponding norm (“length” of the matrix viewed as a vector) is the [Frobenius norm](https://mathworld.wolfram.com/FrobeniusNorm.html).
- When you “flatten” a matrix A by stacking its columns into a single vector, the result is called [vec(A)](https://en.wikipedia.org/wiki/Vectorization_%28mathematics%29), and many important linear operations on matrices can be expressed as [Kronecker products](https://en.wikipedia.org/wiki/Kronecker_product).
- [*The Matrix Cookbook* (PDF)](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf) has lots of formulas for derivatives of matrix functions.
- There is a lot of information online on [finite difference](https://en.wikipedia.org/wiki/Finite_difference), [18.303 Notes on Finite Differences (PDF)](https://github.com/mitmath/18303/blob/fall16/difference-approx.pdf), or [Section 5.7 of Numerical Derivatives (PDF)](http://www.it.uom.gr/teaching/linearalgebra/NumericalRecipiesInC/c5-7.pdf).
- The Julia [FiniteDifferences.jl](https://github.com/JuliaDiff/FiniteDifferences.jl) package provides lots of algorithms to compute finite-difference approximations; a particularly robust and powerful way to obtain high accuracy is to employ [Richardson extrapolation](https://github.com/JuliaDiff/FiniteDifferences.jl) to smaller and smaller δx. If you make δx too small, the finite precision (#digits) of [floating-point arithmetic](https://en.wikipedia.org/wiki/Floating-point_arithmetic) leads to [catastrophic cancellation](https://en.wikipedia.org/wiki/Catastrophic_cancellation) errors.

### Lecture 4

#### Outline

**Part 0:** To begin with, spent a few minutes talking about the last few sections of the [Finite Difference (Jupyter notebook)](https://nbviewer.org/urls/draft.ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/fd_checks.ipynb) from last lecture: higher-order finite-difference rules and finite differences in higher dimensions (e.g. for gradients).

**Part 1:** Generalizing **gradients** to scalar functions f(x) for x in arbitrary vector spaces x ∈ V. The key thing is that we need not just a vector space, but an **inner product** x ⋅ y (a “dot product”, also denoted ⟨x,y⟩ or ⟨x|y⟩); V is then formally called a [Hilbert space](https://en.wikipedia.org/wiki/Hilbert_space). Then, for any scalar function, since df = f’(x)[dx] is a linear operator mapping dx ∈ V to scalars df ∈ ℝ (a “[linear form](https://en.wikipedia.org/wiki/Linear_form)”), it turns out that it [*must* be a dot product](https://en.wikipedia.org/wiki/Riesz_representation_theorem) of dx with “something”, and we call that “something” the gradient! That is, once we define a dot product, then for any scalar function f(x) we can define ∇f by f’(x)[dx] = ∇f ⋅ dx. So ∇f is always something with the same “shape” as x (the [steepest-ascent](https://math.stackexchange.com/questions/223252/why-is-gradient-the-direction-of-steepest-ascent) direction).

Defined the most obvious inner product of m × n matrices: the [Frobenius inner product](https://en.wikipedia.org/wiki/Frobenius_inner_product) A\(\cdot\)B = sum(A\(\cdot\ast\)B) = trace(AᵀB) = vec(A)ᵀvec(B), the sum of the products of the matrix entries. This also gives us the “Frobenius norm” ‖A‖² = A ⋅ A = trace(AᵀA) = ‖vec(A)‖², the square root of the sum of the squares of the entries. Using this, we can now take the derivatives of various scalar functions of matrices, e.g. we considered

- f(A) = ‖A‖ ⥰ ∇f = A/‖A‖
- f(A) = xᵀAy ⥰ ∇f = xyᵀ (for constant x, y)
- f(A) = det(A) ⥰ ∇f = det(A)(A⁻¹)ᵀ = [adjugate](https://en.wikipedia.org/wiki/Adjugate_matrix)(A)ᵀ: we will prove this later

**Part 2:** Applications of derivatives to multivariate root-finding and optimization. A key fact enabling large-scale optimization, i.e. min f(x) where f is a scalar function of *many* parameters x, is that computing ∇f has about the same cost as f, using what is variously called “reverse-mode” or “adjoint” or “backpropagation” differentiation algorithms, which essentially boil down to evaluating the chain rule **left to right**. Went through a few examples of this, oriented more at engineering/physics optimization (and “topology optimization”).

#### Lecture Notes and Slides

- *Course notes: Section 5.1, and Chapter 6*
- Chapter 5: [Lecture 4, Part 1 Notes: Derivatives in General Vector Spaces (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec05_pdf/)
- Chapter 6: [Lecture 4, Part 2 Notes: Nonlinear Root-Finding, Optimization, and Adjoint Differentiation (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec06_pdf/)
- Part 2 Slides: [Nonlinear Root-Finding, Optimization, and Adjoint-Method Differentiation (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec4_pdf/)

#### Further Readings (Part 2)

- Prof. Steven Johnson gave another [overview of optimization problems (PDF)](https://github.com/mitmath/18335/blob/spring21/notes/optimization.pdf) in *18.335 Introduction to Numerical Methods*.
- There are many textbooks on nonlinear programming, including [*Nonlinear Programming*](http://www.athenasc.com/nonlinbook.html) (by Bertsekas) and specialized books on [*Convex Optimization*](http://web.stanford.edu/~boyd/cvxbook/) (by Boyd and Vandenberghe), [*Introduction to Derivative-Free Optimization*](http://bookstore.siam.org/mp08/) (by Conn, Scheinberg, and Vicente), etc.
- A useful review of topology-optimization methods can be found in [Topology Optimization Approaches](https://link.springer.com/article/10.1007/s00158-013-0978-6) (by Sigmund and Maute).
- See the [Notes on Adjoint Methods (PDF)](https://github.com/mitmath/18335/blob/spring21/notes/adjoint/adjoint.pdf) and [The Adjoint Method for Differentiating Complex Computations (PDF)](https://github.com/mitmath/18335/blob/spring21/notes/adjoint/adjoint-intro.pdf) from *18.335 Introduction to Numerical Methods*.

### Lecture 5

#### Lecture Notes and Other Resources

- *Course notes: Section 5.2, Chapter 7, and Sections 8.1–8.2*
- Part 0: Norms and Derivatives: Why a Norm of the Input and Output Are Needed to Define a Derivative
- Chapter 7:[Lecture 5, Part 1 Notes: Derivative of Matrix Determinant and Inverse (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec07_pdf/)
- Part 1: [Derivative of Matrix Determinant and Inverse (HTML)](https://rawcdn.githack.com/mitmath/matrixcalc/b08435612045b17745707f03900e4e4187a6f489/notes/determinant_and_inverse.html) [(Julia source code)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/determinant_and_inverse_jl/)
- Part 2: [Forward-Mode Automatic Differentiation via Dual Numbers (Jupyter notebook)](https://nbviewer.org/urls/draft.ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/autodiff.ipynb)
- Chapter 8: [Lecture 5, Part 3 Notes: Forward and Reverse-Mode Automatic Differentiation (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec08_pdf/)

#### Further Readings (Part 1)

- There are lots of discussions of the [derivative of a determinant](https://en.wikipedia.org/wiki/Jacobi%27s_formula) online, involving the [“adjugate” matrix](https://en.wikipedia.org/wiki/Adjugate_matrix) det(A)A⁻¹. Not as well documented is that the gradient of the determinant is the cofactor matrix widely used for the [Laplace expansion](https://en.wikipedia.org/wiki/Laplace_expansion) of a determinant. The formula for the [derivative of log(det A)](https://statisticaloddsandends.wordpress.com/2018/05/24/derivative-of-log-det-x/) is also nice, and logs of determinants appear in surprisingly many applications (from statistics to quantum field theory).
- [*The Matrix Cookbook* (PDF)](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf) contains many of these formulas, but no derivations.
- A nice application of d(det(A)) is solving for eigenvalues λ by applying Newton’s method to det(A - λI) = 0, and more generally one can solve det(M(λ)) = 0 for any function Μ(λ) — the resulting roots λ are called [nonlinear eigenvalues](https://en.wikipedia.org/wiki/Nonlinear_eigenproblem) (if M is nonlinear in λ), and one can apply Newton’s method using the determinant-derivative formula here.

#### Further Readings (Part 2)

- Googling “automatic differentiation” will turn up many, many resources—this is a huge practical field these days. [ForwardDiff.jl](https://github.com/JuliaDiff/ForwardDiff.jl) (described in detail by “[Forward-Mode Automatic Differentiation in Julia](https://arxiv.org/abs/1607.07892)”) uses [dual number](https://en.wikipedia.org/wiki/Dual_number) arithmetic similar to lecture to compute derivatives.
- See also the article “[How to Differentiate with a Computer](http://www.ams.org/publicoutreach/feature-column/fc-2017-12),” or google “dual number automatic differentiation” for many other reviews.

#### Further Readings (Part 3)

- See [Backpropagation through Back Substitution with a Backslash (PDF)](https://github.com/mitmath/matrixcalc/blob/main/notes/backprop_poster.pdf) about backpropagation on graphs, this blog post on [calculus on computational graphs](https://colah.github.io/posts/2015-08-Backprop/) for a gentle review, and Columbia University’s [Course Notes on Computational Graphs, and Backpropagation (PDF)](http://www.cs.columbia.edu/~mcollins/ff2.pdf) for a more formal approach.
- Implementing automatic reverse-mode AD is much more complicated than defining a new number type, unfortunately, and involves a lot more intricacies of compiler technology. See also Chris Rackauckas’s blog post on [Engineering Trade-Offs in Automatic Differentiation: from TensorFlow and PyTorch to Jax and Julia](https://www.stochasticlifestyle.com/engineering-trade-offs-in-automatic-differentiation-from-tensorflow-and-pytorch-to-jax-and-julia/), and Chris’s discussion post on [AD limitations](https://discourse.julialang.org/t/open-discussion-on-the-state-of-differentiable-physics-in-julia/72900/2).

### Lecture 6

#### Lecture Notes and Slides

- *Course notes: Chapter 9 and Chapter 10*
- Chapter 9: [Lecture 6, Part 1a Notes: Differentiating ODE Solutions (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec09_pdf/)
- Part 1 Slides: [An Introduction to (Local) Sensitivity Analysis for (Ordinary) Differential Equations (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec6_pdf/) (Courtesy of Frank Schäfer. Used with permission.)
- Chapter 10: [Lecture 6, Part 1b Notes: Calculus of Variations (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec10_pdf/)

#### Further Readings (Part 1)

- A classic reference on adjoint-method (reverse-mode/backpropagation) differentiation of ODEs (and generalizations thereof), using notation similar to that used today, is [Adjoint Sensitivity Analysis for Differential-Algebraic Equations: The Adjoint DAE System and Its Numerical Solution](https://epubs.siam.org/doi/10.1137/S1064827501380630) ([PDF](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.65.455&rep=rep1&type=pdf)).
- See also the [SciMLSensitivity.jl package](https://docs.sciml.ai/SciMLSensitivity/stable/) for sensitivity analysis with Chris Rackauckas’s amazing [DifferentialEquations.jl software suite](https://diffeq.sciml.ai/stable/) for numerical solution of ODEs in Julia, along with his notes [Differentiable Programming and Neural Differential Equations](https://rawcdn.githack.com/mitmath/18337/7b0e890e1211bfa253782f7862389aeaa321e8d7/lecture11/adjoints.html).
- There is a nice YouTube lecture on [Adjoint State Method for an ODE](https://www.youtube.com/watch?v=k6s2G5MZv-I), again using a similar notation.
- A *discrete* version of this process is [adjoint methods and sensitivity analysis for recurrence relations (PDF)](https://math.mit.edu/~stevenj/18.336/recurrence2.pdf) (MIT course notes), in which case one obtains a reverse-order “adjoint” recurrence relation.

#### Further Readings (Part 2)

- There are many resources on the [“calculus of variations”](https://en.wikipedia.org/wiki/Calculus_of_variations), which refers to derivatives of f(u) = ∫F(u,u′,…)dx for functions u(x), but we saw that it is essentially just a special case of our general rule df = f(u + du) - f(u) = f′(u)[du] = ∇f ⋅ du when du lies in a vector space of functions. Setting ∇f to find an extremum of f(u) yields an [Euler–Lagrange equation](https://en.wikipedia.org/wiki/Euler%E2%80%93Lagrange_equation), the most famous examples of which are probably [Lagrangian mechanics](https://en.wikipedia.org/wiki/Lagrangian_mechanics) and also the [Brachistochrone problem](https://en.wikipedia.org/wiki/Brachistochrone_curve), but it also shows up in many other contexts such as [optimal control](https://en.wikipedia.org/wiki/Optimal_control).
- A very readable textbook on the subject is [*Calculus of Variations* by Gelfand and Fomin](https://store.doverpublications.com/0486414485.html).

### Lecture 7

#### Lecture Notes

- *Course notes: Chapter 11 and Chapter 12*
- Chapter 11: [Lecture 7, Part 1 Notes: Derivative of Random Functions (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec11_pdf/)
- Lecture 7, Part 1 Guest Lecture Notes: [Derivatives of Random Functions (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec7_pdf/) (Courtesy of Gaurav Arya. Used with permission.)
- Chapter 12: [Lecture 7, Part 2 Notes: Second Derivatives, Bilinear Forms, and Hessian Matrices (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec12_pdf/)

#### Further Readings (Part 1)

- The idea of computing gradients of programs with a sampleable random output is called [Monte-Carlo Gradient Estimation](https://arxiv.org/abs/1906.10652); the link leads to a nice survey.
- This [Stack Exchange answer](https://stats.stackexchange.com/a/226136) gives a concise, worked-out example of the reparameterization trick applied to a toy program.
- [The frontier of simulation-based inference](https://www.pnas.org/doi/10.1073/pnas.1912789117) gives an overview of stochastic simulations across many domains of science, and discusses attempts to deal with the fact that it is much easier to sample them than to exactly compute a “likelihood.”
- [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) introduces the variational autoencoder, and introduces the reparameterization trick for use in training it.
- [Automatic differentiation of programs with discrete randomness](https://arxiv.org/abs/2210.08572) describes an approach for generalizing derivatives of continuous random functions based on the “reparameterization trick” to discrete random functions. [StochasticAD.jl](https://gaurav-arya.github.io/StochasticAD.jl/dev/) is an associated code package that implements the stochastic triples we played with at the end of class.

#### Further Readings (Part 2)

- [Bilinear forms](https://en.wikipedia.org/wiki/Bilinear_form) are an important generalization of quadratic operations to arbitrary vector spaces, and we saw that the second derivative can be viewed as a [symmetric bilinear forms](https://en.wikipedia.org/wiki/Symmetric_bilinear_form). This is closely related to a [quadratic form](https://en.wikipedia.org/wiki/Quadratic_form), which is just what we get by plugging in the same vector twice, e.g. the f’’(x)[δx,δx]/2 that appears in quadratic approximations for f(x + δx) is a quadratic form. The most familiar multivariate version of f’’(x) is the [Hessian matrix](https://en.wikipedia.org/wiki/Hessian_matrix); Khan Academy has an elementary [quadratic approximation](https://www.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/quadratic-approximations/a/quadratic-approximation).
- [Positive-definite](https://en.wikipedia.org/wiki/Definite_matrix) Hessian matrices, or more generally [definite quadratic forms](https://en.wikipedia.org/wiki/Definite_quadratic_form) f″, appear at extrema (f′ = 0) of scalar-valued functions f(x) that are local minima; there a lot [more formal treatments (PDF)](http://www.columbia.edu/~md3405/Unconstrained_Optimization.pdf) of the same idea, and conversely Khan Academy has the [simple 2-variable version](https://www.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/optimizing-multivariable-functions/a/second-partial-derivative-test) where you can check the sign of the 2 × 2 eigenvalues just by looking at the determinant and a single entry (or the trace). There’s a nice [Stack Exchange discussion](https://math.stackexchange.com/questions/2285282/relating-condition-number-of-hessian-to-the-rate-of-convergence) on why an [ill-conditioned](https://nhigham.com/2020/03/19/what-is-a-condition-number/) Hessian tends to make steepest descent converge slowly; some Toronto [Optimization (PDF)](https://www.cs.toronto.edu/~rgrosse/courses/csc421_2019/slides/lec07.pdf) may also be helpful.
- See e.g. these Stanford notes on [Sequential Convex Programming (PDF)](https://web.stanford.edu/class/ee364b/lectures/seq_notes.pdf) using trust regions (sec. 2.2). See 18.335 notes on [Quasi-Newton Optimization: Origin of the BFGS Update (PDF)](https://github.com/mitmath/18335/blob/spring21/notes/BFGS.pdf). The fact that a quadratic optimization problem in a sphere has [strong duality](https://en.wikipedia.org/wiki/Strong_duality) and hence is efficiently solvable is discussed in section 5.2.4 of the [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/). There has been a lot of work on [automatic Hessian computation](https://en.wikipedia.org/wiki/Hessian_automatic_differentiation), but for large-scale problems you can ultimately only compute Hessian–vector products efficiently in general, which are equivalent to a directional derivative of the gradient, and can be used e.g. for [Newton–Krylov methods](https://en.wikipedia.org/wiki/Newton%E2%80%93Krylov_method).

### Lecture 8

#### Lecture Notes and Other Resources

- *Course notes: Chapter 13, and Chapter 8, Sections 8.3-8.4, and Chapter 14*
- Chapter 13: [Lecture 8, Part 1 Notes: Derivatives of Eigenproblems (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec13_pdf/)
- Part 1: [Derivatives of Eigenproblems (HTML)](https://rawcdn.githack.com/mitmath/matrixcalc/d11b747d70a5d9e1a3da8cdb68a7f8a220d3afae/notes/symeig.jl.html) [(Julia source code)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/symeig_jl/)
- Part 2: Forward and Reverse-Mode Automatic Differentiation on Computational Graphs (continued from Lecture 5) and [interactive notebook (HTML)](https://simeonschaub.github.io/ReverseModePluto/notebook.html)
- Chapter 14: [Lecture 8, Part 3 Notes: Where We Go From Here (PDF)](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/resources/mit18_s096iap23_lec14_pdf/)

#### Further Readings (Part 1)

- Computing derivatives on curved surfaces (“manifolds”) is closely related to [tangent spaces](https://en.wikipedia.org/wiki/Tangent_space) in differential geometry. The effect of constraints can also be expressed in terms of [Lagrange multipliers](https://en.wikipedia.org/wiki/Lagrange_multiplier), which are useful in expressing optimization problems with constraints (see also chapter 5 of [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/) by Boyd and Vandenberghe). In physics, first and second derivatives of eigenvalues and first derivatives of eigenvectors are often presented as part of [“time-independent” perturbation theory](https://en.wikipedia.org/wiki/Perturbation_theory_%28quantum_mechanics%29) in quantum mechanics, or as the [Hellmann–Feynmann theorem](https://en.wikipedia.org/wiki/Hellmann%E2%80%93Feynman_theorem) for the case of dλ. The derivative of an eigenvector involves *all* of the other eigenvectors, but a much simpler “vector–Jacobian product” (involving only a single eigenvector and eigenvalue) can be obtained from left-to-right differentiation of a *scalar function* of an eigenvector, as reviewed in the [Notes on Adjoint Methods for 18.335 (PDF)](https://github.com/mitmath/18335/blob/spring21/notes/adjoint/adjoint.pdf).

#### Further Readings (Part 2)

- See Lecture 5, above.

#### Further Readings (Part 3)

There are many topics that we did not have time to cover, even in 16 hours of lectures. If you came into this class thinking that taking derivatives is easy and you already learned everything there is to know about it in first-year calculus, hopefully we’ve convinced you that it is an enormously rich subject that is impossible to exhaust in a single course. Some of the things it might have been nice to include are:

- When AD hits something it can’t handle, you may have to write a custom Jacobian–vector product (a “Jvp”, “frule”, or “pushforward”) in forward mode, and/or a custom rowvector–Jacobian product (a “vJp”, “rrule”, “pullback”, or Jacobianᵀ–vector product) in reverse mode. In Julia with Zygote AD, this is done using [the ChainRules packages](https://github.com/JuliaDiff/ChainRulesCore.jl). In Python with JAX, this is done with [`jax.custom_jvp`](https://jax.readthedocs.io/en/latest/_autosummary/jax.custom_jvp.html) and/or [`jax.custom_vjp`](https://jax.readthedocs.io/en/latest/_autosummary/jax.custom_vjp.html), respectively. In principle this is straightforward, but the APIs can take some getting used to because of the generality that they support.
- For functions f(z) of complex arguments z (complex vector spaces), you cannot take “ordinary” complex derivatives whenever the function involves the conjugate z̄ (e.g. for |z|, Re z, or Im z); this *must* occur if f(z) is purely real-valued (and not constant). One option is to write z = x + iy and treat f(z) as a two-argument function f(x,y) with real derivatives, but this can be awkward if your problem is “naturally” expressed in terms of complex variables (e.g. in the [Fourier frequency domain](https://en.wikipedia.org/wiki/Frequency_domain)). A common alternative is “CR calculus” (or “Wirtinger calculus”), in which you write df = (∂f/∂z)dz + (∂f/∂z̄)dz̄ as if z and z̄ were independent variables. This can be extended to gradients, Jacobians, steepest-descent, and Newton iterations, for example. A nice review can be found in [The Complex Gradient Operator and the CR-Calculus](https://arxiv.org/abs/0906.4835) by Ken Kreuz-Delgado.
- Many, many more derivative results for matrix functions and factorizations can be found in the literature, some of them quite tricky to derive. For example, a number of references are listed in this GitHub issue for the [ChainRules package](https://github.com/JuliaDiff/ChainRules.jl/issues/117).
- Another important generalization of differential calculus is to derivatives on curved manifolds and differential geometry, leading to the [exterior derivative](https://en.wikipedia.org/wiki/Exterior_derivative).
- When differentiating eigenvalues λ of matrices A(x), a complication arises at eigenvalue crossings (multiplicity k > 1), where in general the eigenvalues (and eigenvectors) cease to be differentiable. (More generally, this problem arises for any [implicit function](https://en.wikipedia.org/wiki/Implicit_function) with a repeated root.) In this case, one option is to use an expanded definition of sensitivity analysis called a **generalized gradient** (a k × k matrix-valued linear operator G(x)[dx] whose eigenvalues are the perturbations dλ); see e.g. [Cox (1995)](https://doi.org/10.1006/jfan.1995.1117), [Seyranian et al. (1994)](https://doi.org/10.1007/BF01742705), and [Stechlinski (2022)](https://doi.org/10.1016/j.laa.2022.04.019). (Physicists call this idea [degenerate perturbation theory (PDF)](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/a0889c5ca8a479c3e56c544d646fb770_MIT8_06S18ch1.pdf).) A recent formulation of similar ideas is called a **lexicographic directional derivative**; see [Nesterov (2005)](https://doi.org/10.1007/s10107-005-0633-0) and [Barton et al. (2017)](https://doi.org/10.1080/10556788.2017.1374385). Sometimes, optimization problems involving eigenvalues can be reformulated to avoid this difficulty by using [SDP](https://en.wikipedia.org/wiki/Semidefinite_programming) constraints [(Men et al. 2014)](http://doi.org/10.1364/OE.22.022632). For a [defective matrix](https://en.wikipedia.org/wiki/Defective_matrix) the situation is worse: even the generalized derivatives blow up, because dλ is proportional to the *square root* of the perturbation ‖dA‖.
- Famous generalizations of differentiation are the [“distributional”](https://en.wikipedia.org/wiki/Distributional_derivative) and [“weak”](https://en.wikipedia.org/wiki/Weak_derivative) derivatives, for example to obtain [Dirac delta “functions”](https://en.wikipedia.org/wiki/Dirac_delta_function) by differentiating discontinuities. This requires changing not only the definition of “derivative” but also *changing the definition of “function,”* as reviewed in [When Functions Have No Value(s): Delta Functions and Distributions (PDF)](https://math.mit.edu/~stevenj/18.303/delta-notes.pdf).
