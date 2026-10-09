- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec6/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 6: Indexing and Access Methods

This lecture will cover various issues related to the physical storage of relations on disk, as well as index data structures we might use to efficient access those stored relations. Read the following (short) papers and book sections:

- In *Database Management Systems*, read:
  - Pages 273-289. If you are using another book, this is the introduction to the section on Storage and Indexing which discusses different access methods and their relative performance.
  - Pages 344-358. This is an in-depth discussion of the B+Tree data structure and its implementation. Most database books, as well as any algorithms text (such as CLR or Knuth) will provide an equivalent discussion of B+Trees.
- “The R*-Tree: An Efficient and Robust Access Method for Points and Rectangles.” Beckmann et al, in the Red Book.

As you read, think about and come to class prepared to answer the following questions:

- Under what circumstances is a secondary index superior to a sequential (in-order) scan of a heap file? Under what circumstances would the secondary index scan be preferable?
- What is the purpose of the neighbor pointers in a B+Tree? When are they useful?
- Why are B+Trees insufficient for storing and indexing the types of data stored by R*-Trees?
