- Source: https://ocw.mit.edu/courses/6-1810-operating-system-engineering-fall-2023/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Prerequisites

[6.191/6.004 Computation Structures](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)

### Course Description

This is a course on the design and implementation of operating systems and their use as a foundation for systems programming. Topics covered include virtual memory; file systems; threads; context switches; kernels; interrupts; system calls; and interprocess communication, coordination, and interaction between software and hardware. A multi-processor operating system for RISC-V, [xv6](https://en.wikipedia.org/wiki/Xv6), is used to illustrate these topics. Individual laboratory assignments involve extending the xv6 operating system, for example to support sophisticated virtual memory features and networking.

You may wonder why we are studying xv6, an operating system that resembles Unix v6, instead of the latest and greatest version of Linux, Windows, or BSD Unix. xv6 is big enough to illustrate the basic design and implementation ideas in operating systems. On the other hand, xv6 is far smaller than any modern production O/S, and correspondingly easier to understand. xv6 has a structure similar to many modern operating systems; once you’ve explored xv6 you will find that much is familiar inside kernels such as Linux.

### Who should take 6.1810

6.1810 is intended for undergraduates who enjoyed 6.191/6.004 and want to learn about design and implementation of operating systems, and their use as a foundation for systems programming.

### Grading policy

Grades in 6.1810 will be based on the following elements:

- Labs (70%). The score for each individual lab is automatically calculated. All labs are weighted equally.
- Check-off meetings (20%). During the check-off meetings we will ask you a few questions about your lab solution. We expect to hold three check-off meetings per student for randomly-selected labs. The check-off meetings will be graded on scale of 0 to 5.
- Homework assignments and class / online forum participation (together 10%).

You must submit all labs in order to pass the class.

There will be no quizzes and no exams.

### Labs

To turn in each lab, run “make zipball” in your lab directory and upload the resulting lab.zip file to Gradescope. The submission deadline is 11:59:59 PM on the day that the lab is due. You can turn in as many times as you like before the deadline. The Gradescope autograder uses “make grade” to assign a grade to your submission.

You have a total of 72 late hours for the semester. Each hour late in excess of 72 hours will penalize your total lab grade by 1%, up to a maximum of 50%. Late hours are allocated greedily, so they are allocated to earlier labs before later labs. Due to institute regulations, late hours may not be used for the last lab (due in the last full week of classes).

We suggest that you save your late hours for unexpected emergencies. For predictable situations (athletic events, deadlines in other classes, job interviews, etc.) we expect you to manage your time so as to finish assignments by the due date. If you have exhausted your late hours but nevertheless encounter an emergency that causes you to need an extension, we ask that you talk to [Student Support Services](https://studentlife.mit.edu/s3) and ask them to send us a letter supporting your request.

### Lecture Questions / Homeworks

The lecture questions / homeworks are intended to make you think about the lecture topic. They are due before the start of lecture (i.e., 1 PM) on the specified due dates. We would appreciate if you submit lecture questions well before 1 PM (e.g., the night before) so that we can prepare to answer your questions during lecture. You can miss a few lecture questions / homeworks over the semester without any penalty.

### Textbooks

6.1810 relies on the following books:

- [*xv6: A Simple, Unix-Like Teaching Operating System*](https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf) by Russ Cox, Frans Kaashoek, and Robert Morris. 2022.
- *The C Programming Language, second edition* by Brian W. Kernighan and Dennis M. Ritchie. Prentice Hall, 1988. ISBN: 9780131103627

### Collaboration

You are welcome to discuss the labs (and homeworks) with other students, but all of your written work and code must be your own and must carefully acknowledge all contributions of ideas by others, whether from classmates or from sources you have read. Please don’t look at anyone else’s code for the labs or homework. Please feel free to ask and answer questions on the online forum, about labs, homework, readings, and lectures.

Do not post your lab or homework solutions on publicly accessible web sites or file spaces.

### Acknowledgments

6.1810 would not exist today had it not been for a wonderful set of past TAs (Josh Cates, Austin Clements, Russ Cox, Cody Cutler, Bryan Ford, Max Krohn, Emil Sit, Jonathan Behrens, and Anish Athalye). They made this class a reality. Collectively we dedicate 6.1810 to the memory of Josh Cates; we hope that many students will be inspired by Josh’s enthusiasm for operating systems.

We are also grateful to the students and teaching staff at MIT (including [SIPB](https://sipb.mit.edu/)) and other schools for their many contributions.
