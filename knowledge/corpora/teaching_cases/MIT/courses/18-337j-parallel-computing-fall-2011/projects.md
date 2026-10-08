> 检索摘要：18.337J Parallel Computing（Fall 2011，Graduate）的「Projects」。页内标题：Projects；Kinds of Projects；Julia-related Project Ideas；Modern Parallel Linear Algebra Project Ideas；Parallel Algorithms, Libraries Project Ideas；Abstractions and Infrastructure Project Ideas；Tools；Sample Student Final Projects。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

[Kinds of Projects](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

[Julia-related Project Ideas](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

[Modern Parallel Linear Algebra Project Ideas](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

[Parallel Algorithms, Libraries Project Ideas](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

[Abstractions and Infrastructure Project Ideas](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

[Tools](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

[Sample Student Projects](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/pages/projects/)

### Kinds of Projects

- problem X on parallel architecture/environment Y
- parallel algorithm for X
- performance comparisons
  - what is best algorithm in environment X?
  - or in input data case X?
  - how good is, e.g. MPI message latency and could it be better?
- debugging and monitoring parallel programs
- parallel abstractions, platforms (e.g. MapReduce)
- resource sharing infrastructure
- cloud infrastructure
- making technical computing more fun

### Julia-related Project Ideas

- Can use as an implementation language
  - many parallel algorithms are likely to be much easier in Julia than MPI
- Or work on the platform itself
  - whole parallel computing system written in Julia, quite compact
  - parallel computing base: 1600 lines (multi.j)
  - distributed arrays: 762 lines

### Modern Parallel Linear Algebra Project Ideas

- LU without block-cyclic
- LU with dynamic # of CPUs
- new SVD algorithm

### Parallel Algorithms, Libraries Project Ideas

- optimization
- numerical integration
- multigrid
- parallel data structures other than arrays
  - graphs, tables, sparse arrays

### Abstractions and Infrastructure Project Ideas

- a MapReduce or dataflow framework in Julia
- some other highly-reusable parallel computation
- high-level EC2 interface
- storage
  - persistent distributed arrays
  - integrate a distributed FS (HDFS, scidb, sector)
- cluster sharing tools

### Tools

- What would make technical computing more fun?
- Watching/choreographing parallel computations
- Social coding features
  - collaboration
  - shared “wisdom”
- Visualization

### Sample Student Final Projects

Three of the students in the class have provided their final projects for publication on OCW and they are presented here with their permission.

Parallel FFT in Julia: [Slide (PDF - 1.6MB)](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mit18_337jf11_fft_pres/), [Code (TXT)](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/parallel_fft/), [Report (PDF)](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mit18_337jf11_fft_rpt/) (Courtesy of anonymous MIT student. Used with permission.)

Social coding: [Slides (PDF)](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mit18_337jf11_social_pres/), [Report (PDF)](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mit18_337jf11_social_rpt/) (Courtesy of anonymous MIT student. Used with permission.)

Replica-Exchange Molecular Dynamics on Hadoop: [Report (PDF)](https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/resources/mit18_337jf11_hadoop_rpt/) (Courtesy of Zachary Ulissi. Used with permission.)
