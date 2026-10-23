- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec19/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 19: NOSQL

Read:

Chang, Fay, et al. “Bigtable: A Distributed Storage System for Structured Data.” OSDI, 2006. ([PDF](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf))

Bigtable is a storage system for structured data; it is essentially a compressed, horizontally partitioned, column-oriented database with some interesting properties that allow it to reach “web scale”.

As you read the paper, consider the following questions:

1. In what ways does Bigtable replicate the behavior of a relational database? How is it different?
2. Could Google have built Bigtable using a relational system? Would that have been a good idea? Why or why not?
3. What consistency guarantees does Bigtable provide in the face of failures?
4. What is a distributed lock service?
