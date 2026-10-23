- Source: https://ocw.mit.edu/courses/6-852j-distributed-algorithms-fall-2009/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Description

Distributed algorithms are algorithms designed to run on multiple processors, without tight centralized control. In general, they are harder to design and harder to understand than single-processor sequential algorithms. Distributed algorithms are used in many practical systems, ranging from large computer networks to multiprocessor shared-memory systems. They also have a rich theory, which forms the subject matter for this course.

Theoretical results about distributed algorithms appear in research conferences such as PODC (Principles Of Distributed Computing), DISC (International Symposium on DIStributed Computing), OPODIS (International Conference On Principles Of DIStributed Systems), and SPAA (ACM Symposium on Parallelism in Algorithms and Architectures). They also appear in general theoretical computer science conferences such as FOCS (Foundations Of Computer Science) and STOC (Symposium on Theory Of Computing), and in broad conferences involving distributed computing, such as ICDCS (International Conference on Distributed Computing Systems).

What do distributed algorithms researchers do? They (we) define various kinds of distributed computing environments, including shared-memory and network-based environments, and identify problems to be solved in those environments. They design new algorithms for these problems, and analyze the correctness, performance, and fault-tolerance of their algorithms. They also prove lower bounds and other impossibility results, which explain why certain tasks cannot be carried out in certain kinds of distributed settings, or cannot be carried out within certain cost constraints. Researchers typically study problems that arise in practical distributed systems, including problems of communication, data management, resource management, synchronization, and distributed agreement. Sometimes, the results have impact on practical distributed system design.

This year, the course will be taught by Prof. Nancy Lynch, with some help from Dr. Victor Luchangco, a member of the Scalable Systems research group at Sun Microsystems Research. The core of the material will consist of basic distributed algorithms and impossibility results, as covered in Prof. Lynch’s book *Distributed Algorithms*. This will be supplemented by some updated material on topics such as self-stabilization, wait-free computability, and failure detectors, and some new material on scalable shared-memory concurrent programming.

6.852 is a graduate-level course that is intended to do two things: provide an introduction to the most important basic results in the area of distributed algorithms, and prepare interested students to begin independent research or take a more advanced course in distributed algorithms. Usually, the students who take the course are a mixture of PhD students and MEng students. Since the course is run at a PhD level, most MEng students should find it challenging.

### Prerequisites

To take 6.852/18.437, you should have:

- “Mathematical maturity.” In particular, you should be very good at reading and writing mathematical proofs.
- General knowledge about some distributed systems. For instance, MIT’s undergraduate course *6.033 Computer System Engineering* would be good background.
- Experience with sequential algorithms and their analysis. MIT’s undergraduate course *6.046J/18.410J Design and Analysis of Algorithms* is sufficient.
- Experience with formal models of computation (desirable, but not essential). MIT’s courses *6.045J/18.400J Automata, Computability, and Complexity* or *18.404J/6.840J Theory of Computation* would be fine for this.

### Texts

#### Required

The primary source will be the book *Distributed Algorithms* by Prof. Nancy Lynch.

Lynch, Nancy. *Distributed Algorithms*. Burlington, MA: Morgan Kaufmann, 1996. ISBN:9781558603486.

Errata ([PDF](https://ocw.mit.edu/courses/6-852j-distributed-algorithms-fall-2009/resources/mit6_852jf09_errata/))

This book has gone through many printings, but we have made no changes since the fourth printing, so fourth printings or later are just fine. Known errata for early printings are collected in errata lists. The book refers to many papers from the research literature on distributed algorithms; you might want to track down and read some of these.

#### Recommended

Other books that you will find useful are:

Attiya, Hagit, and Jennifer Welch. *Distributed Computing: Fundamentals, Simulations, and Advanced Topics*. 2nd ed. New York, NY: Wiley-Interscience, 2004. ISBN: 9780471453246.

This is another textbook on distributed algorithms, initially published a little after the Lynch book. It now has a second edition. The material covered overlaps quite a lot with the Lynch book, though Attiya and Welch do cover some topics, like clock synchronization, that Lynch does not cover. The style is a little less formal.

Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*. Burlington, MA: Morgan Kaufmann, 2008. ISBN: 9780123705914.

This undergraduate textbook covers basic algorithms and techniques for multiprocessor programming.

Guerraoui, Rachid, and Michal Kapalka. *Transactional Memory*: *The Theory.* San Rafael, CA: Morgan and Claypool, 2010. ISBN: 9781608450114.

This monograph presents basic theoretical results about the possibility and costs of implementing transactional memory for shared-memory multiprocessors.

[Buy at MIT Press](https://mitpress.mit.edu/9780262041782) Dolev, Shlomi. *Self-Stabilization*. Cambridge, MA: MIT Press, 2000. ISBN:9780262041782.

This book gives a good description of self-stabilizing distributed algorithms. Self-stabilization is a strong kind of fault-tolerance, which we will study near the end of the course.

Kaynar, Disun, Nancy Lynch, Roberto Segala, and Frits Vaandrager. *The Theory of Timed I/O Automata*. 2nd ed. San Rafael, CA: Morgan and Claypool, 2010. ISBN:9781608450022.

This monograph presents a basic modeling framework, Timed I/O Automata (TIOA), for describing and analyzing distributed algorithms.

In addition, some research papers that are not covered in the textbook will be covered in class and on problem sets. These papers are listed in the [Readings](https://ocw.mit.edu/courses/6-852j-distributed-algorithms-fall-2009/pages/readings/) as supplementary readings.

### Course Requirements

#### Readings

Readings that cover the material for each class will be announced ahead of time. For most classes, these will be sections from the textbook. For some classes, they will be research papers from the supplementary reading list. Reading a research paper will generally take more time than reading sections from the textbook, so be prepared to put in the extra time. We expect students to read the assigned material ahead of time and to come to class prepared to discuss it.

#### Problem Sets

These are intended to help you to understand the material covered in class. Most problems involve algorithms and problems already covered; some will be designed to get you started thinking about ideas to be discussed in later classes.

Specifically, approximately five problems will be given out every Thursday. The problems will be batched and due every two weeks, at the beginning of class on alternate Thursdays. There will be a total of seven problem set due dates. No late homework assignments will be accepted. If you haven’t finished, just hand in what you have completed. However, in the case of a serious emergency, please talk to the course instructors or the teaching assistant.

Homework is an important part of your grade. When grading homework problems, we will try to give full credit to solutions that include all the important logical steps and ideas. We consider it a minus for a write-up to be lengthy and overly detailed. An exception is when we specifically ask for details, for instance, in formal proofs of correctness of algorithms.

We have software available to assist you in writing syntactically-correct distributed algorithms; we are requiring that you use it for your homework assignments. This software consists mainly of the Tempo language processor, which allows specification of algorithms as interacting state machines. Information about how to download the software and how to get started using it appears at VeroModo. You will notice that the Tempo language has a home-grown simulator, connections to the PVS theorem-prover and UPPAAL model-checker. We are not requiring you to use any of these tools, but of course, you are welcome to try them. You will probably find the Tempo User Guide and test examples useful.

The Tempo language is based on Timed I/O Automata, a mathematical modeling framework consisting of interacting state machines, possibly with timing constraints. To learn about the mathematical framework, you should consult the monograph *The Theory of Timed I/O Automata,* by Kaynar, Lynch, Segala, and Vaandrager. This is part of the Synthesis series of computer science monographs, published by Morgan and Claypool.

#### Policy on Homework Collaboration

You are strongly encouraged to discuss possible solutions with other class members. Many students in past incarnations of this course have formed homework discussion groups. However, you must always write up the solutions entirely on your own.

#### Problem Set Grading

For each problem set, a group of 3-4 students will be responsible for working with the course staff to grade the solutions. If possible, we would like the grading to be completed by the Monday afternoon after the homework assignments are handed in, so that we can record the grades and hand them back on Tuesday. The number of times you have to grade over the course of the semester will depend on the size of the class. Part of your grade will depend on the quality and promptness of your work on problem set grading.

#### Exams

There will be no exams. No midterm, no final. You can go home after the last class.

### Grading

Your course grade will be based on problem set grades, problem set grading, and class participation. Problem sets will be graded on inclusion of the important logical steps and ideas. Class participation will be evaluated based on attendance and quality and quantity of participation. Problem set grading will be judged by quality and promptness.

| ACTIVITIES | PERCENTAGES |
| --- | --- |
| Problem sets (7) | 70% |
| Class participation | 20% |
| Problem set grading | 10% |
