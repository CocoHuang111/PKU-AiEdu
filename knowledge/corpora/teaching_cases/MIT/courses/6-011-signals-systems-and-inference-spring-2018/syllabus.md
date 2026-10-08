> 检索摘要：6.011 Signals, Systems and Inference（Spring 2018，Undergraduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Prerequisites；About This Course；Textbooks；**Required:**；**Recommended:**；Learning Objectives；Grading；Lower-Friction Option；Project Option；Assignments。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-011-signals-systems-and-inference-spring-2018/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1 hour / session

Recitations: 2 sessions / week, 1 hour / session

### Prerequisites

The essential prerequisites for this course are *[6.003 Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011)* and *[6.041A Intro to Probability I](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013)* (or equivalents), and the *[18.03 Differential Equations](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011)* material related to solving linear, time-invariant sytems of first-order differential equations using eigenvalues and eigenvectors.

No matter how fresh and comfortable you are with the prerequisite material, it can take some time to connect it to what’s going on in a new class, so make some allowance for that fact—we on the staff certainly will. If we say “xyz should be familiar from 6.003/6.041A” and you don’t recall ever having seen “xyz” in your life, ask questions, do some reading, discuss things with your fellow students or the staff, until you are able to connect the dots.

### About This Course

The lectures, recitations, and homework in 6.011 will expand on signals, systems and probabilistic models. We will also explore prototype problems and applications from communication, control and signal processing. The topics will involve aspects of analysis, synthesis and optimization, for both continuous-time (CT) and discrete-time (DT) systems. The ideas, approaches and methods you learn here will significantly expand the range of engineering applications that you will be able to understand and work with at some level.

What will be new relative to 6.003 and 6.041A? The list includes most of the following:

- new kinds of signals (e.g., random processes)
- new signal characterizations (e.g., autocorrelation functions, energy/power spectral densities)
- new kinds of system descriptions (e.g., state-space models for causal systems)
- new system properties (e.g., reachability/observability)
- new signal processing tasks (e.g., optimal estimation)
- new communication tasks (e.g., optimal detection)
- new control tasks (e.g., state estimation, observer-based controller design)
- more intimate mixing of DT and CT in several applications

These topics do not fall in a linear path away from 6.003/6.041A. Rather, we will be expanding out in a spiral, sampling the many routes that lead out from 6.003/6.041A, coming back to some of them one or two times. At the end you may be surprised to find how much territory you have covered without moving all that far away from the basics in 6.003 and 6.041A.

### Textbooks

#### **Required:**

There are two versions of the book for purchase. Problem numbers for both the hardcover and softcover versions will be given in assignments.

- *Hardcover*: Oppenheim, Alan, and George Verghese. *Signals, Systems and Inference*. Pearson, 2015. ISBN: 9180133943283
- *Softcover*: Oppenheim, Alan, and George Verghese. *Signals, Systems and Inference*. Pearson, 2017. ISBN: 9781292156200

#### **Recommended:**

- Oppenheim, Alan, and Alan Willsky, with S. Hamid Nawab. *Signals and Systems*. 2nd ed. Prentice-Hall, 1996.
- Bertsekas, Dimitri, and John Tsitsiklis. *Introduction to Probability*. 2nd ed. Athena Scientific, 2008.

### Learning Objectives

We’ll aim to (un)cover the following topics:

- Brief review of linear, time-invariant (LTI) system models in continuous and discrete time (CT and DT), and in the frequency domain. Deterministic autocorrelation.
- State-space models (mainly LTI).
- Brief review of random variables.
- Estimation.
- Stationary random processes in time and frequency domains.
- Signal estimation.
- Hypothesis testing.
- Some intimations of machine learning: training and applying quadratic discriminators in feature space.
- Signal detection.

### Grading

| activities | Percentages |
| --- | --- |
| Participation | 15% |
| Weekly Assignments | 25% |
| Quiz 1 | 20% |
| Quiz 2 | 15% |
| Final Exam | 25% |

Attendance and participation in lectures and recitations are expected and necessary, in order for you to engage with and learn the subject well. We recognize “participation” as including

- engagement with the course material
- keeping up week-to-week
- contributions to class discussions
- responsiveness to questions and questionnaires

We encourage you to view each homework as an occasion for learning, on your own or/and in a study group, and through discussions with the staff. The problem sets are not intended as weekly tests, and will be graded liberally on a 0, 1, 2, 3 scale. If you attend, participate, and do your homework, you will have earned at least a C in the class.

The tests will all be closed-book, but you will be allowed two two-sided sheets of notes for Quiz 1, three sheets for Quiz 2, and four sheets for the final exam.

#### Lower-Friction Option

If your particular optimization of your route through MIT causes you to prefer a “lower-friction” version of the course, please inform Prof. Verghese and he will switch your grading to eliminate the 15% allotted to attendance and participation. (Keep in mind, however, that anything covered in lecture and recitation is fair game on quizzes and the final exam.) If you elect this option, it will be irreversible. Homework will still count for 25% of your grade, but the two quizzes and final will count for 25%, 20%, and 30% of the course grade respectively. Also, if you select this option, the sign-up tutorials with a teaching assistant (TA) will not be available to you (as we cannot have the TAs providing private make-ups for missed lectures and recitations), but you are welcome to all other components of the class. Finally, if you elect this option, you do not need to email your instructor to let them know in advance of any lecture or recitation you will miss.

#### Project Option

If you are interested in doing a project related to the class material, and provided you are not in the lower-friction version of the class (see above), please talk to Prof. Verghese. If your project proposal is accepted, you will have until the last day to add a class to commit to doing it, submitting a one-page written proposal. In this case, the relative weightings of the course components in determining your final grade will be: attendance & participation 15%; homework 25%; Quiz 1 for 15%; Quiz 2 for 15%; Final 20%, and project 10%. You will not be allowed to return to the non-project option after committing, so don’t commit unless you are sure you will follow through all the way. A written (roughly 10-page) report on the project will be due at the end of the term.

### Assignments

Some part of the homework may involve computer exercises. We assume that you already have some familiarity with using Matlab or Python or Mathematica or some such environment to tackle these exercises.

Each problem set will be given a score of 0–3, with the 0 indicating little evidence of any original thought or work (e.g., if a solution is quite clearly lifted from solutions distributed in an earlier term—if this happens more than once, the consequences will be worse than just a 0 on the homework), and with the 3 indicating a good homework submission, demonstrating understanding and careful work. If you’re following the course well and doing the problem sets attentively, you should expect to be getting 2’s and 3’s.

Don’t leave the comparison and study of our solutions and yours until the night before a test! Make sure this is a weekly effort, and feel free to see the staff for further discussion on the homework solutions. To facilitate this effort, you may want to make a copy of your homework solutions for yourself before you turn them in! This will allow you to begin comparing your solutions with ours as soon as you receive ours, rather than waiting until your solutions are returned to you one week later (by which time we will be into other topics).

It should be evident from our grading policy that we do not intend the homeworks as tests, but as vehicles for learning. Therefore, we will not hesitate to use problems from previous terms. Relying upon “bibles” to get you through the homeworks—rather than on your own thinking and understanding—will undoubtedly cause you difficulties on the tests. You may expect that each test will include some problems of the same flavor and difficulty as those encountered on the homework, but sufficiently modified to assess your thinking and understanding, rather than your ability to “pattern match.” The tests will also include problems that require you to integrate and reason with the course material.

Solutions to problems labeled as “Optional” on the homework do not need to be turned in. However, we select these problems with the same care as the assigned problems. They will give you valuable practice and/or bring up important issues, so you are likely to find them helpful to do as time permits, either along with the other problems, or in reviewing for tests.

We expect each of you to put in enough time alone to understand the specific difficulties and issues raised by each problem. Moderate collaboration on homework problems with one or two of your classmates may be useful for some of you. Discussions with the staff are encouraged, especially since this is the best way for the staff to get to know you. There is no harm in seeking minor assistance from others who are knowledgeable but not involved in the class, although we would much prefer that your discussion be with those in the class. We expect you to independently write up the actual solutions that you turn in, and to note on your solutions the name of anyone you have collaborated with or obtained help from.

### Tutorials

The tutorial sessions run by the teaching assistants (TAs) are optional. The sessions are an hour each and will be strictly limited to five students at a time. These will start from the second week of term. We will be arranging for on-line sign-up. Please sign up for only one slot at a time each week. If you do sign up for a tutorial slot, you will be expected to attend. If, after signing up, you find you will be unable to attend for whatever reason, please remove yourself from the schedule so that the slot can be cleared for someone else. If all posted slots fill up, we will try to schedule additional ones. The tutorials will, in effect, function as the TAs’ primary office hours, so bring your questions to them. While the TAs may have prepared questions and problems for you to work through interactively at the board, the burden will be largely on you to articulate what you are having trouble with, and to give examples of the kinds of things you are getting stuck on. You should expect to go to the board and help work things out alongside your TA or fellow students. The tutorials are not intended to be mini-lectures or mini-recitations, and are emphatically not intended to help you make up for missed lectures or recitations or prerequisite subjects! At the end of each term, several students invariably suggest that tutorials should have been required rather than optional, either because they benefited greatly from them, or because they recognized (too late!) that they would have benefited from them.
