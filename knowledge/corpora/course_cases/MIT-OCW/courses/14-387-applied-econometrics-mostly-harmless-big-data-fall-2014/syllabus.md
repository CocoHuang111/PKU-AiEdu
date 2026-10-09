- Source: https://ocw.mit.edu/courses/14-387-applied-econometrics-mostly-harmless-big-data-fall-2014/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Prerequisites

[*14.382 Econometrics*](https://ocw.mit.edu/courses/economics/14-382-econometrics-spring-2017/)

is the prerequisite for this course.

### Course Requirements and Grading

Students are expected to do the readings. In addition, there are three graded problem sets, which must be submitted on time to be graded for credit (the course is graded pass / fail). The atmosphere is informal, but we ask you to put all electronic devices away when class is in session. We encourage questions and class discussion—we’ll be asking you questions too!

### Text

Angrist, J. D., and J. S. Pischke. *Mostly Harmless Econometrics: An Empiricist’s Companion*. Princeton University Press, 2009. ISBN: 9780691120355. [Preview with [Google Books](http://books.google.com/books?id=ztXL21Xd8v8C&pg=PAfrontcover)]

Basic and review material for the first two-thirds of the course come mostly from this book. A few core and frontier articles are also listed for each topic.

### Instructors

This course is co-taught by [Prof. Joshua Angrist](http://economics.mit.edu/faculty/angrist) and [Prof. Victor Chernozhukov](http://www.mit.edu/~vchern/). Prof Angrist teaches topics I–VII. Prof. Chernozhukov’s section begins at topic VIII.

### Topics

1. **Regression Recap**
  - 3 reasons to love
  - The CEF is all you need
  - The long and short of regression anatomy
  - Omitted variables bias
  - Casual vs causal (3.2)
  - Limited dependent variables (3.4.2)
2. **Matching and Training**
  - Matching
  - Training and the propensity score
3. **Instrumental Variables**
  - Part 1
    - *Constant-effect models*
      - IV and omitted variables bias: estimating a “long regression” without controls
      - 2SLS: walk the walk, talk the talk
      - The Wald estimator and grouped data
      - Two-sample IV and related methods (4.3)
      - Examples
    - *IV details*
      - 2SLS mistakes: MHE, Section 4.6.1
      - The bias of 2SLS: MHE, Section 4.6.4
  - Part 2
    - *Instrumental variables with heterogeneous potential outcomes*
      - Local average treatment effects
      - The *compliers* concept; identification of effects on the treated and ATE
      - IV in randomized trials
      - Counting and characterizing compliers
      - Distribution Treatment Effects
      - Kappa and QTE
    - *Models with variable and continuous treatment intensity*
      - Average causal response
      - Average derivatives
      - Examples
4. **IV Topics**
  - *External Validity*
    - Labor supply consequences of childbearing
    - Quantity-quality trade-offs
  - *The Perils of Peer Effects*
5. **Differences-in-Differences**
  - Straight DD
  - Regression DD
  - DD spec checks
  - *The DD Frontier*
    - Synthetic control
    - Semiparametric DD
    - Changes-in-changes
6. **Regression-Discontinuuity Designs**
  - Sharp RD
  - Nonpara-‘Metrics
  - Extrapolation
  - Fuzzy RD
7. **Inference**
  - Review of asymptotic OLS inference (3.1.3; notes)
  - *The bias of robust standard errors*
    - Robust s.e.s are more biased than you think
    - An example
  - *Clustering and serial correlation*
    - Clustering and the Moulton factor
    - Serial correlation in differences-in-differences models
    - Fewer than 42 clusters
    - Evidence on the bootstrap for clustering
    - Endogenous Stratification
8. **Prediction with a Large Number of Covariates (“Big P”)**
  - The role of penalization in simplifying the model and avoiding overfitting. Lasso and Post-Lasso and its variants as a leading method for penalization and model simplification. Dealing with heteroscedasticity and clustering issues.
9. **Valid Confidence Intervals with a Large Number of Covariates (“Big P”)**
  - Inference in a linear model with many instruments. Inference in a partially linear model model with many controls. Inference in a partially linear model with many instruments and many controls. Inference in program evaluation with exogenous and endogenous receipt of treatment. Dealing with heteroscedasticity and clustering issues.
10. **Analysis with Large Sample Sizes (“Big N”)**
  - Analysis of moderately large samples and very large samples. Parallelization and Clustering. Google Map Reduce and Apache Hadoop.
