- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec16/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 16: Distributed Transactions

We will continue our discussion of parallel and distributed query processing. You should read:

Mohan, C., B. Lindsay, and R. Obermarck. “Transaction Management in the R* Distributed Database Management Systems.” *ACM Transactions on Database Systems* 11, no. 4 (1986): 378-396. In the Red Book.

This paper discusses distributed transactions, addressing the problem of providing ACID-style semantics in a shared nothing environment.

As you read the paper, consider the following questions:

1. In the “R*” paper, how does the two phase commit (2PC) protocol work? What problem does it solve? What are the costs of using it?
2. What is the significance of the Presumed Abort/Presumed Commit variants of 2PC? How do they reduce the overhead of 2PC? When should you choose one over the other?
