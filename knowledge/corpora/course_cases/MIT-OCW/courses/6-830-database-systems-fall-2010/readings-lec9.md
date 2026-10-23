- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec9/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 9: Query Optimization

In this lecture, we will discuss the problem of query optimization, focusing on the algorithms proposed in the classic “Selinger” paper.

Read the following papers:

- Selinger, Patricia, M. Astrahan, D. Chamberlin, Raymond Lorie, and T. Price. “Access Path Selection in a Relational Database Management System.” *Proceedings of ACM SIGMOD* (1979): 23-34.
- *Optionally*, you may also wish to look at: Mannino, Michael, Paichen Chu, and Thomas Sager. “Statistical Profile Estimation in Database Systems.” *ACM Computing Surveys* 20, no. 3 (1988): 191-221. This paper discusses many of the techniques that used to make query optimization and cost estimation practical in modern database systems. We will cover some of the ideas at a high level in class.

As you read, think about and come to class prepared to answer the following questions:

- The Selinger paper claims to be ‘optimal’. Under what assumptions is this optimality true? Can you think of a situation in which Selinger will definitely be non-optimal?
- Query optimization is highly dependent on the effectiveness of cost estimation. The cost metrics that Selinger proposes are very simple; how would you make them more sophisticated? What is the impact of more sophisticated cost metrics on the performance of a database system?
