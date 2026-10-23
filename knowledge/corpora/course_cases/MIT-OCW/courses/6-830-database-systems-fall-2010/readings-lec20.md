- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec20/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 20: ORM, DryadLINQ

Read:

Yu, Yuan, et al. “DryadLINQ: A System for General-Purpose Distributed Data-Parallel Computing Using a High-Level Language.” OSDI, 2008. ([PDF](http://research.microsoft.com/en-us/projects/dryadlinq/dryadlinq.pdf))

DryadLINQ is a programming language for manipulating structured data in a distributed setting. It provides a collection of SQL-like constructs that are well-integrated into C# (with a common type and object system), and compiles down to a graph of operators spread across a distributed network of machines in a way similar to how distributed databases work.

As you read the paper, consider the following questions:

1. What are the advantages of a query language that is integrated into the programming language? Are there disadvantages?
2. Dryad execution plans look a lot like database query plans, but are different in some ways — in particular, operators can have multiple outputs; what are the implications of this from a query execution perspective?
