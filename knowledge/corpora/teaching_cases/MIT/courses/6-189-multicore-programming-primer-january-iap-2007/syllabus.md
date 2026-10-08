> 检索摘要：6.189 Multicore Programming Primer（January IAP 2007，Undergraduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Course Overview；Course Highlights；Course Description；Grading；Target Student Population；Calendar。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-189-multicore-programming-primer-january-iap-2007/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: Three sessions / week, 2 hours / session

Recitations: Two sessions / week, 1 hour / session

### Course Overview

The era of Moore’s law induced performance gains of sequential programs is over. In the future, the primary method of increasing program performance will require the utilization of multicore parallelism. The processing platforms of the future will have hundreds or even thousands of processor cores that are tightly integrated for parallel processing. Unfortunately, very few programmers know how to program these multicore systems. This pain will be felt in all tiers of the market because of the increasing reliance on computing power for scientific discovery and day-to-day activities. There will be a deep impact on academic institutions as well because they have done little to train the programmers of the future with the right concepts and tools so that they can harness the computing power of multicores and massively parallel systems.

Some leading vendors are already offering parallel processors on a chip. Today, most general purpose processors in the market are multicores. The Cell processor from IBM, Sony, and Toshiba is a 9-core heterogeneous processor that powers the [Sony PLAYSTATION®3](http://www.us.playstation.com/PS3) and also appears in various broadband markets. At their Developer Forum a few months ago, Intel announced an 80-core homogeneous processor slated for fabrication in just a few years. These new architectures offer the unique opportunity to have parallel systems on a chip available to the masses in gaming consoles, mobile devices, personal computers, and embedded platforms. The ubiquitous presence of parallelism will make it necessary to train a new breed of programmers so that parallel programming is as easy and tractable as the conventional sequential programming that millions of programmers are accustomed to today.

### Course Highlights

The course serves as an introductory course in parallel programming. It offers a series of lectures on parallel programming concepts as well as a group project that provides hands-on experience with parallel programming. Students will have the unique opportunity to use the cutting-edge [PLAYSTATION 3](http://www.us.playstation.com/PS3) development platform, as they learn how to design and implement exciting applications for multicore architectures. At the end of the course, students will have an understanding of:

- Fundamental design philosophies that multicore architectures address.
- Parallel programming philosophies and emerging best practices.

### Course Description

The course briefly covers the history of the microprocessor evolution and discusses the reasons for the recent shift in architecture design toward multicores. Students will become familiar with the Cell processor that powers the [PLAYSTATION 3](http://www.us.playstation.com/PS3) and how its design choices compare to other emerging architectures.

Students will also learn about the various programming models currently used for programming parallel architectures. The course combines lectures with hands-on labs so that students can experiment with the different models of computation and learn about the pros and cons of the different programming models. Students will also learn [StreamIt](http://cag.csail.mit.edu/streamit/), a new, simple, and natural to understand programming language for stream computing. The course will explore broader implications of the stream programming model to various kinds of traditional parallelization technology.

Students will participate in a course long project drawn from any of several exciting domains that include gaming engines, media applications, algorithms for molecular dynamics, and protein folding challenge problems. Students are expected to participate in small project teams. Course projects are evaluated based on their performance, complexity, and completeness. Students will compete for exciting prizes to be awarded to the best project as selected by a panel of judges.

### Grading

Grades will be determined using the following weights:

| ACTIVITIES | PERCENTAGES |
| --- | --- |
| Mini-quizzes | 16% |
| Exercises and labs | 24% |
| Final group project | 60% |

### Target Student Population

The course is open to all students (undergraduates and graduates). Students who are interested in the course are strongly encouraged to discuss project ideas with the instructors before enlisting in the course. We have several projects that we can suggest and discuss with you, or we can discuss some of your own project ideas. We strongly encourage small teams of students per project. Teams of 4-5 students are likely to work best, but smaller teams are also plausible. We can help you assemble a team as necessary, although it is best if you know someone that will want to work on the same project with you. Each team will have dedicated access to a PLAYSTATION 3 console, along with programming and debugging tools, tutorials, and hands-on help.

### Calendar

The calendar below provides information on the course’s lecture (L) and recitation (R) sessions.

<table><tr><th>SES #</th><th>TOPICS</th><th>LECTURERS</th></tr><tr><td colspan="3">Week 1</td></tr><tr><td>L1</td><td>Course introduction</td><td>Saman Amarasinghe</td></tr><tr><td>L2</td><td>Introduction to Cell processor</td><td>Michael Perrone, IBM</td></tr><tr><td>R1</td><td>Getting to know Cell</td><td></td></tr><tr><td>L3</td><td>Introduction to parallel architectures</td><td>Saman Amarasinghe</td></tr><tr><td></td><td>Quiz 1</td><td></td></tr><tr><td>L4</td><td>Introduction to concurrent programming</td><td>Saman Amarasinghe</td></tr><tr><td></td><td>Project reviews</td><td></td></tr><tr><td>L5</td><td>Parallel programming concepts</td><td>Rodric Rabbah, IBM</td></tr><tr><td></td><td>Quiz 2</td><td></td></tr><tr><td>L6</td><td>Design patterns for parallel programming I</td><td>Rodric Rabbah, IBM</td></tr><tr><td colspan="3">Week 2</td></tr><tr><td>R2-R3</td><td>Cell programming hands-on</td><td></td></tr><tr><td>L7</td><td>Design patterns for parallel programming II</td><td>Rodric Rabbah, IBM</td></tr><tr><td></td><td>Quiz 3</td><td></td></tr><tr><td>L8</td><td>StreamIt language</td><td>Bill Thies</td></tr><tr><td>R4</td><td>Cell debugging tools</td><td></td></tr><tr><td>L9</td><td>Debugging parallel programs</td><td>Rodric Rabbah, IBM</td></tr><tr><td></td><td>Quiz 4</td><td></td></tr><tr><td>L10</td><td>Performance monitoring and optimizations</td><td>Rodric Rabbah, IBM</td></tr><tr><td colspan="3">Week 3</td></tr><tr><td>L11</td><td>Parallelizing compilers</td><td>Saman Amarasinghe</td></tr><tr><td></td><td>Quiz 5</td><td></td></tr><tr><td>L12</td><td>StreamIt parallelizing compiler</td><td>Saman Amarasinghe</td></tr><tr><td>R5</td><td>Cell profiling tools</td><td></td></tr><tr><td>R6</td><td>SIMD programming on Cell</td><td></td></tr><tr><td>L13</td><td>Star-P</td><td>Alan Edelman</td></tr><tr><td></td><td>Quiz 6</td><td></td></tr><tr><td>L14</td><td>Synthesizing parallel programs</td><td>Arvind</td></tr><tr><td>L15</td><td>Cilk</td><td>Bradley Kuszmaul</td></tr><tr><td>L16</td><td>Introduction to game development</td><td>Mike Acton, Insomiac Games</td></tr><tr><td colspan="3">Week 4</td></tr><tr><td>L17</td><td>The Raw experience</td><td>Rodric Rabbah, IBM</td></tr><tr><td>L18</td><td>The future</td><td>Saman Amarasinghe</td></tr><tr><td></td><td>Student project competition</td><td></td></tr><tr><td></td><td>Award ceremony</td><td></td></tr></table>
