> 检索摘要：6.02 Introduction to EECS II: Digital Communication Systems（Fall 2012，Undergraduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Prerequisites；Course Objectives；Software；Problem Sets；Participation；Grading。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-02-introduction-to-eecs-ii-digital-communication-systems-fall-2012/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1 hour / session

Recitations: 2 sessions / week, 1 hour / session

### Prerequisites

[18.03](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011), [6.01](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011). The problem sets involve programming; they require knowledge of Python at the level of [6.00](https://ocw.mit.edu/courses/6-00sc-introduction-to-computer-science-and-programming-spring-2011) or [6.01](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011).

### Course Objectives

An introduction to several fundamental ideas in electrical engineering and computer science, using digital communication systems as the vehicle. The three parts of the course—**bits, signals, and packets**—cover three corresponding layers of abstraction relevant to the system:

- binary representation, compression (source coding), and error correction (channel coding) for messages transmitted across a noisy link;
- signal representation of binary messages for transmission across a shared physical channel subject to distortion and noise;
- efficient, reliable communication across networks made up of multiple links.

Topics investigated in depth include:

- *Bits*: Information and entropy, Huffman coding and LZW compression, error correction with linear block codes and convolutional codes (Viterbi decoding).
- *Signals*: Additive Gaussian noise and the relationship between noise variance and bit errors, linear-time invariant channel models, frequency-domain (Fourier) analysis, spectral content of signals and filtering, modulation and demodulation.
- *Packets*: Media access protocols (TDMA, Aloha, and carrier sense), packet-switched networks, queues, and Little’s law, network routing (distance/path vector & link-state protocols), and reliable data transport (adaptive timers, stop-and-wait, sliding windows, round-trip time and bandwidth-delay product concepts).

These topics form the basis of communication systems like the Internet.

The course teaches ideas that are useful in other parts of EECS: abstraction, probabilistic analysis, superposition, time- and frequency-domain representations, system design principles and trade-offs, and centralized and distributed algorithms. The course emphasizes connections between theoretical concepts and practice using programming tasks and some experiments with real-world communication channels.

At the end of the course, a successful student will understand these topics and be able to apply them to the design and analysis of communication systems and networks. In particular, they will appreciate how to build reliable and efficient communication systems: cleverly applying redundancy for reliability and sharing via multiplexing channels, links, and paths for efficiency.

### Software

[Instructions for setting up the 6.02 environment on your computer](https://ocw.mit.edu/courses/6-02-introduction-to-eecs-ii-digital-communication-systems-fall-2012/pages/syllabus/software/)

### Problem Sets

There are nine problem sets, assigned more-or-less weekly most Wednesdays. Problem sets are usually due at midnight the following Wednesday (we’ll let that deadline slide to 6am the following Thursday morning in keeping with MIT tradition).

Each problem set includes problems that involve writing Python code, so be sure to start early and leave enough time to debug your implementation before the due date. There will be six checkoff interviews during the semester, lasting 15–20 minutes each on average, which you must complete with your assigned TA on or before the dates specified on the problem set. Your TA will contact you to schedule these interviews.

Completing the interviews is a pre-requisite for passing the course. A missing interview will result in a failing grade; we will not grant “incomplete” for missing interviews.

Please note that working through the problem sets (and other practice problems we provide) is the best way to test your understanding of what we teach and to prepare for the quizzes.

*Late policy*: You may use up to five extension days (in total) over the course of the semester for the nine problem set, apportioned in any way. For any other late problem sets, your score will be multiplied by 0.5; moreover, you must submit it within 7 days of the original due date to get any credit.

*Collaboration policy*: The problem sets must be done individually. You may get help from the course staff and other students on the underlying material in the problem sets, but the work you hand in must be your own. In particular, you must not copy another person’s solution, code, or other work. Someone telling you the solution to a problem is also not acceptable. Copying another person’s work or allowing your work to be copied by others is a serious academic offense and will be treated as such. We will spot-check your submissions using a software utility, as well as manually, for cheating, so please don’t tempt fate by submitting someone else’s work as your own; it will save us all a lot of grief.

### Participation

We expect you to attend all lectures and recitations, unless there are pressing or unforeseen conflicts. Conflicts that are persistent (e.g., registering for another class at the same time and “splitting” attendance between them) are not excused. Attending recitations is not merely optional. Things we teach in lecture and recitation are fair game on quizzes and problem sets.

To assess and encourage participation, recitations (and perhaps some lectures) will include simple “spot questions” that we will ask from time to time. Over the duration of the term, between lectures and recitations, we anticipate many dozens of such questions; if you pay a little attention, answering them will be trivial. At the end of the term we will take your responses to all these questions into consideration to assess a participation score, which will count toward a small portion (3%) of the overall grade.

If you miss a few lectures and recitations, it shouldn’t materially affect this score. If you miss more, it probably will, and may affect your grade if you end up at the border between two letter grades.

### Grading

Your final grade will be determined as follows:

| ACTIVITIES | PERCENTAGES |
| --- | --- |
| Quiz 1 | 17% |
| Quiz 2 | 18% |
| Quiz 3 | 17% |
| Problem sets | 5% each, 45% total |
| Participation | 3% |
