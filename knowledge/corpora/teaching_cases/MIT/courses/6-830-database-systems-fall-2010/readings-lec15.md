> 检索摘要：6.830 Database Systems（Fall 2010，Graduate、Undergraduate）的「Readings Lecture 15: C-Store」。页内标题：Readings Lecture 15: C-Store。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec15/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 15: C-Store

Read:

Stonebraker, Michael, et al. *C-Store: A Column-oriented DBMS*. Proceedings of the 31st VLDB Conference, 2005. ([PDF](https://w6113.github.io/files/papers/cstore-vldb05.pdf))

This paper discusses the C-Store system, which is a read-optimized database system with a novel physical arrangement of data on disk, as well as an unusual approach to recovery and query processing

As you read the paper, consider the following questions:

1. Why does the C-Store idea of arranging data as columns improve query performance?
2. How does C-Store propose to do recovery? Is there an advantage to this approach?
3. How does C-Store isolate transactions? Do you think this is a good idea?
