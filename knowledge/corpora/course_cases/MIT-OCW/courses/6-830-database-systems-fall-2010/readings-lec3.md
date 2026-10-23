- Source: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/readings/lec3/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Lecture 3: Schema Design

The reading for this lecture is:

1. The start of chapter 2 to end of section 2.6 (pages 25-46) of Ramakrishnan and Gehrke
2. Section 3.5 (pages 75-86) of Ramakrishnan and Gehrke
3. The start of chapter 19 to end of section 19.4 (pages 605-619) of Ramakrishnan and Gehrke

The first two readings discuss ER modeling, which is one practical way which can be used to model a database and generate database schemas.

The third reading discusses a formal model based on the notion of functional dependencies that makes it possible to reason about whether schemas are free of anomalies that lead to operational problems in database system execution. You should focus on understanding BCNF and 3NF; we will not discuss the higher normal forms in much detail.

The relationship between these three readings is that ER modeling generally produces schemas that conform to 3NF/BCNF, though this isn’t strictly true (see section 19.7 for a discussion of cases when ER modeling doesn’t lead to BCNF or 3NF schemas.) For those who are interested, it turns out that there are relatively straightforward algorithms for generating BCNF/3NF schemas given a collection of functional dependencies — these are given in Sections 19.5 and 19.6 of Ramakrishnan and Gehrke, but you don’t need to know these in detail.

As you read these chapters, think about and be prepared to answer the following questions in lecture:

- What problems does schema normalization solve? Do you believe that these are important problems?
- What is the distinction between BCNF and 3NF? Is there a reason to prefer one over the other?
- Think about a data set you have worked with recently, and try to derive a set of functional dependencies that correspond to it. What assumptions did you have to make in modeling your data in this way?
- How is it that ER modeling generally leads to BCNF/3NF schemas?
