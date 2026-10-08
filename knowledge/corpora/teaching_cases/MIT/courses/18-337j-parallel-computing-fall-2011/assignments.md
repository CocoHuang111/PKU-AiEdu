> 检索摘要：18.337J Parallel Computing（Fall 2011，Graduate）的「Assignments」。页内标题：Assignments；Homework 1；Homework 2；Analyzing bigrams。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

**NOTE**: The homework assignments for this class require access to the following online development tools and environments that **may not be freely available to OCW users**. The assignments are included here as examples of the work MIT students were expected to complete.

[Message Passing Interface (MPI)](http://www.mcs.anl.gov/research/projects/mpi/): Standardized and portable message-passing system designed by a group of researchers from academia and industry to function on a wide variety of parallel computers.

[Star-P:](http://www.scientificcomputing.com/product-release/2008/01/star-p) Technical computing software that offers an open platform architecture that helps to integrate software and hardware from various high performance computing (HPC) sources, and supports popular desktop tools, numerical libraries and hardware accelerators.

[The Julia Programming Language:](https://julialang.org/) A high-level, high-performance dynamic language for technical computing, with syntax that is familiar to users of other technical computing environments. It provides a sophisticated compiler, distributed parallel execution, numerical accuracy, and an extensive mathematical function library.

[Amazon Elastic Compute Cloud (Amazon EC2):](http://aws.amazon.com/ec2/) A web service that provides resizable compute capacity in the cloud. It is designed to make web-scale computing easier for developers.

[Hadoop MapReduce:](https://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html) A programming model and software framework for writing applications that rapidly process vast amounts of data in parallel on large clusters of compute nodes.

### Homework 1

In this assignment you will be exposed to different models of parallel computation. The goal is simply to say “hello world” through different tools and environments so you know how to access them.

We will use four combinations of tools and environments: MPI on a cluster, Star-P on a cluster, Julia on Amazon Elastic Compute Cloud (EC2), and Julia on multi-core. There is nothing too special about these combinations; it is also possible to run MPI on EC2 or Julia on a cluster, for example.

The tools and environments you will use are:

1. MPI on a cluster
2. MATLAB® with Star-P
3. Julia on EC2
4. Julia on multi-core

For each section of the assignment, copy a transcript of the interesting parts of your terminal session to a text file

Sample Files: MPI example program in C ([C](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mpipi/)), MPI example program in Fortran ([F](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mpipi-1/))

### Homework 2

In this assignment you will implement a statistical analysis using the MapReduce paradigm with Hadoop, and run your analysis at a reasonable scale on a cluster of Amazon EC2 instances.

The tools and environments you will use are:

1. Running Hadoop clusters
2. Running MapReduce jobs
  1. Using Java
  2. Using other languages

Suggested reading: Sections 3.1 through 3.3 of the book

Lin, Jimmy, and Chris Dyer. *Data-Intensive Text Processing with MapReduce*. Morgan & Claypool, 2010. ISBN: 9781608453429. [Preview with [Google Books](http://books.google.co.in/books?id=GxFYuVZHG60C&printsec=frontcover&dq=Data-Intensive+Text+Processing+with+MapReduce&hl=en&sa=X&ei=v0AdT9HoNYbUrQfhotyGDQ&ved=0CDgQ6AEwAA)]

Tasks to perform:

##### Analyzing bigrams

This exercise is adapted from material accompanying Lin and Dyer’s book. You are welcome to consult any material you want to help solve this problem. However, if you encounter a full solution to this particular problem on the internet, please do not use it.

Bigrams are sequences of two consecutive words. Understanding which bigrams occur in natural language is useful in a variety of search and textual analysis problems. We will use MapReduce first to count the unique bigrams in an input corpus, and then to compute relative frequencies (how likely you are to observe a word given the preceding word).

**Counting bigrams**

Modify the word count example code to count unique bigrams instead. How many unique bigrams are there? List the top ten most frequent bigrams and their counts.

**Relative frequencies**

Some bigrams may appear frequently simply because one of their words is especially common. We can obtain a more interesting statistic by dividing the number of occurrences of the bigram “A B” by the total number of occurrences of all bigrams starting with “A”. This gives *P*(*B*\*A*), the probability of seeing “B” given that it follows “A”.

Pick a word, and show the relative frequencies of words following it. What pairs of words are especially strongly correlated, i.e. *P*(*B*\*A*) is large?

Section 3.3 of the book discusses a technique for computing this result in a single MapReduce job, using fancy features of the framework. You do not have to use this technique, and may instead use multiple MapReduce jobs if you wish.

**Obtaining input data**

You can use the input data available on the homework page of the class website, or you may select your own corpus of input text. [Project Gutenberg](http://www.gutenberg.org/), is a good source of interesting texts. There is no particular requirement on the size of data to use, but it should be interestingly large, e.g. the complete novels of Charles Dickens. To make the assignment more fun, entirely at your option, you may wish to compare statistics of different authors, time periods, genres, etc.
