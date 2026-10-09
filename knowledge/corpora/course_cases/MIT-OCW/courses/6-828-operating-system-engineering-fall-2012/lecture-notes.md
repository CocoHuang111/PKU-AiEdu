- Source: https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/pages/lecture-notes-and-readings/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Lecture Notes and Readings

Some of the readings require the [xv6 code (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_xv6-sourc-rev7/), as well as the [xv6 book (PDF - 1.3MB)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_xv6-book-rev7/), which are provided courtesy of Frans Kaashoek, Robert Morris, and Russ Cox and are used here with permission.

| LEC # | LECTURE TOPICS AND NOTES | READINGS AND HANDOUTS |
| --- | --- | --- |
| 1 | [Operating Systems (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec1_notes/) | “Chapter 0: Operating System Interfaces” of xv6 book |
| 2 | [PC Hardware and x86 Programming (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec2_notes/) | “Appendix A: PC Hardware” and “Appendix B: The Boot Loader” of xv6 book, and the related xv6 source files |
| 3 | [Overview of Major Internals, System Call Interface (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec3_notes/) | “Chapter 1: The first process” and the related xv6 source files |
| 4 | [Virtual Memory (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec4_notes/) | “Chapter 2: Page Tables” <br> [Page Table Translation and Registers (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec4_handout/) |
| 5 | [Interrupts, Exceptions (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec5_notes/) | “Chapter 3: Traps, interrupts, and drivers” and the related xv6 source files <br> [IDT (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec5_handout/) |
| 6 | [Multiprocessors and Locking (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec6_notes/) | “Chapter 4: Locking” with spinlock.c and skim mp.c |
| 7 | [Processes and Switching (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec7_notes/) | “Chapter 5: Scheduling” up to “Sleep and wakeup” with proc.c, setjmp.S, and sys_fork (in sysproc.c) |
| 8 | [Sleep & Wakeup (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec8_notes/) | Read remainder of “Chapter 5: Scheduling”; read remainder of proc.c and sys_wait, sys_exit, sys_kill |
| 9 | [File Systems (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec9_notes/) | “Chapter 6: File system” and bio.c, fs.c, sysfile.c, file.c, except for the logging sections |
| 10 | [Crash Recovery (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec10_notes/) | Read log.c and the logging sections of “Chapter 6: File system” |
| 11 | [File System Performance and Fast Crash Recovery (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec11_notes/) | Tweedie, Stephen C. “ <br> [Journaling the Linux ext2fs Filesystem](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.307.9137) <br> .” [Paper Presented at LinuxExpo 1998]. |
| 12 | Project Introduction and Discussion |  |
| 13 | [OS Organization (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec13_notes/) | Engler, Dawson R., M. Frans Kaashoek, and James O’Toole Jr. “ <br> [Exokernel: An Operating System Architecture for Application-Level Resource Management](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.2893) <br> .” |
| 14 | In-class Hacking Session |  |
| 15 | Project Conferences |  |
| 16 | Project Conferences (cont.) |  |
| 17 | [Language / OS Co-design (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec17_notes/) | Hunt, Galen C., and James R. Larus. “ <br> [Singularity: Rethinking the Software Stack](http://dx.doi.org/10.1145/1243418.1243424) <br> .” <br> Microsoft Research Redmond <br> 41, no. 2 (2007): 37–49. |
| Quiz | Quiz (Open Book and Notes) |  |
| 18 | [Scalable Locks (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec18_notes/) | Boyd-Wickizer, Silas, M. Frans Kaashoek, et al. “ <br> [Non-Scalable Locks are Dangerous](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.261.196) <br> .” |
| 19 | Project Conferences |  |
| 20 | Project Conferences (cont.) | Boyd-Wickizer, Silas, Austin T. Clements, et al. “ <br> [An Analysis of Linux Scalability to Many Cores](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.174.5191) <br> .” |
| 21 | [Lock-free Coordination (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec21_notes/) |  |
| 22 | [Virtual Machines (PDF)](https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/resources/mit6_828f12_lec22_notes/) | Adams, Keith, and Ole Agesen. “ <br> [A Comparison of Software and Hardware Techniques for x86 Virtualization](http://dx.doi.org/10.1145/1168857.1168860) <br> .” <br> ACM Digital Library <br> 34, no. 5 (2006): 2–13. |
| 23 | No lecture; work on final projects |  |
| 24 | Demos in class |  |
| 25 | Demos in class (cont.) |  |
