- Source: https://ocw.mit.edu/courses/18-783-elliptic-curves-fall-2025/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions/week, 1.5 hours/session

### Prerequisite

[*18.702 Algebra II*](https://ocw.mit.edu/courses/18-702-algebra-ii-spring-2011/), [*18.703 Modern Algebra*](https://ocw.mit.edu/courses/18-703-modern-algebra-spring-2013/), or permission of instructor

### Description

This course offers a computationally focused introduction to elliptic curves, emphasizing their deep connections to number theory and cryptography. Core topics include point-counting, isogenies, pairings, and the theory of complex multiplication. Throughout the course, these concepts are applied to practical problems such as integer factorization, primality proving, and elliptic curve cryptography.

Each of the topics listed below corresponds to roughly one week of lectures (a total of three hours).

1. **Introduction** Elliptic curves, the group law, Weierstrass and Edwards equations.
2. **Efficient computation** Integer arithmetic, finite field arithmetic, root-finding, and polynomial factorization.
3. **Isogenies and endomorphisms** The Frobenius endomorphism, division polynomials, and Hasse’s theorem.
4. **Elliptic curves over finite fields** Point counting, baby-steps giant-steps, and Schoof’s algorithm.
5. **The discrete logarithm problem** ECEDH, Pollard rho, Pohlig-Hellman, generic lower bounds, and index calculus.
6. **Integer factorization and primality proving** Lenstra ECM, Goldwasser-Kilian ECPP, and Montgomery curves.
7. **Endomorphism rings** The dual isogeny, quadratic orders, quaternion algebras, and supersingular curves.
8. **Elliptic curves over the complex numbers** Elliptic functions, Eisenstein series, the Weierstrass ℘-function, complex tori, the *j*-function, the uniformization theorem, and isogenies.
9. **Modular curves** Congruence subgroups, Riemann surfaces, and modular functions.
10. **The theory of complex multiplication** Ring class fields, Hilbert class polynomials, and the CM method.
11. **Isogeny graphs** Isogeny volcanoes, supersingular isogeny graphs, and isogeny-based cryptography.
12. **Divisors and pairings** Divisor class groups, pairings, Miller’s algorithm, and pairing-based cryptography.
13. **Elliptic curves over Q** Mordell’s theorem, 2-descent, Weil-Châtelet, Selmer, and Shafarevich–Tate groups.
14. **L-functions** Modular forms, modularity, the Birch and Swinnerton-Dyer conjecture.

### Textbook and Notes

There is no required textbook; [lecture notes](https://ocw.mit.edu/courses/18-783-elliptic-curves-fall-2025/pages/lecture-notes-and-worksheets/) are provided. We make reference to material in the following books.

Washington, Lawrence C. *Elliptic Curves: Number Theory and Cryptography*. Second edition. Chapman & Hall / CRC, 2008. ISBN: 9781420071467. ([Errata (PDF)](https://www.math.umd.edu/~lcw/ECerrata.pdf)) [Online version](https://www.taylorfrancis.com/books/mono/10.1201/9781420071474/elliptic-curves-lawrence-washington).

Milne, James S. *Elliptic Curves*. BookSurge Publishing, 2006. ISBN: 9781419652578. ([Addendum / erratum (PDF)](https://www.jmilne.org/math/Books/add/EC2006.pdf)). [Online version (PDF)](https://www.jmilne.org/math/Books/ectext6.pdf).

Silverman, Joseph H. *The Arithmetic of Elliptic Curves*. Springer-Verlag, 2009. ISBN: 9780387094939. ([Errata (PDF)](https://www.math.brown.edu/johsilve/AEC/AECErrata.pdf)) [Online version](https://link.springer.com/book/10.1007/978-0-387-09494-6).

———. *Advanced Topics in the Arithmetic of Elliptic Curves*. Springer-Verlag, 1994. ISBN: 9780387943251. ([Errata (PDF)](https://www.math.brown.edu/johsilve/ATAEC/ATAECErrata.pdf)). [Online version](https://link.springer.com/book/10.1007/978-1-4612-0851-8).

Cox, David A. *Primes of the Form* \(x^2 + ny^2\)*:* *Fermat, Class Field Theory, and Complex Multiplication*. Wiley-Interscience, 1989. ISBN: 9780471506546. ([Errata (PDF)](https://dacox.people.amherst.edu/primes/typos.2ed.pdf)). [Online version](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118400722).

The following two books give quite accessible introductions to elliptic curves from different perspectives. You may find them useful as supplemental reading, but we don’t use them in the course.

Blake, Ian F., Gadiel Seroussi, and Nigel P. Smart. *Elliptic Curves in Cryptography*. Cambridge University Press, 1999. ISBN: 9780521653749. [Preview with [Google Books](https://books.google.com/books?id=0_vegzgyqGMC&pg=PAfrontcover)]

Silverman, Joseph H., and John T. Tate. *Rational Points on Elliptic Curves*. Springer-Verlag, 1994. ISBN: 9780387978253. [Online version](https://link.springer.com/book/10.1007/978-1-4757-4252-7).

The following references provide introductions to algebraic number theory and complex analysis; neither of these topics is an official prerequisite for this course, but we occasionally need to make use of their results.

[Algebraic Number Theory Course Notes](https://www.jmilne.org/math/CourseNotes/ant.html) by James S. Milne.

Lang, Serge. *Complex Analysis*. Springer-Verlag, 2003. ISBN: 9780387985923. [Online version](https://link.springer.com/book/10.1007/978-1-4757-3083-8).

### Software

Some of the theorems and algorithms presented in lecture are demonstrated using [Sage](https://www.sagemath.org/), a Python-based computer algebra system, hosted on [CoCalc](https://cocalc.com/). Most of the problem sets contain at least one computationally-focused problem, which you likely want to use Sage to solve, but you are free to use other packages, or roll your own code from scratch. You are graded on your results and your mathematical explanation and analysis of your algorithm, not your code.

### Problem Sets

There are weekly problem sets, each of which typically contains three to five multi-part problems. You are not expected to solve all of the problems on each problem set; you be given the option to choose a subset to turn in. Some problems are purely theoretical in nature, while others are more computationally focused; those who prefer proofs to programming (or vice versa) can choose problems that appeal to their interests.

Problem sets are to be prepared in typeset form (typically via LaTeX) and submitted electronically as PDF files. Collaboration is permitted, but you must write up your own solutions and identify any collaborators, as well as any resources you used that are not listed above. There are computational problems for which the correct answer is different for every student, based on a unique identifier derived from your MIT ID.

### Grading

There are 2 in-class mid-term exams and a 3-hour final exam. Sixty percent of your grade is determined by your problem set scores, and forty percent is determined by exams. When computing your scores I do whichever of the following gives you the best grade: (a) drop your two worst problem set scores, (b) drop your worst problem set score and your worst mid-term score, (c) drop your grade on the final. This means you can skip the final exam if you are happy with your grade at that point.
