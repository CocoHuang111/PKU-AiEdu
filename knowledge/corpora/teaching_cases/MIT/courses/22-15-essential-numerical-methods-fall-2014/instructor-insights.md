> 检索摘要：22.15 Essential Numerical Methods（Fall 2014，Graduate）的「Instructor Insights」。页内标题：Instructor Insights；Course Overview；Course Outcomes；Course Goals for Students；Instructor Interview；A Foundational Course for Graduate Study and Research；Balancing Breadth and Detail in a Half-Term Course；Curriculum Information；Prerequisites；Requirements Satisfied；Offered；Assessment。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/22-15-essential-numerical-methods-fall-2014/pages/instructor-insights/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Instructor Insights

### Course Overview

This page focuses on the course *22.15 Essential Numerical Methods* as it was taught by Prof. Ian Hutchinson in the first half of the Fall 2014 term.

This half-semester course introduces computational methods for solving physical problems, especially in nuclear applications. The course covers ordinary and partial differential equations and their representation and solution by finite difference numerical approximations; iterative matrix inversion methods; stability, convergence, accuracy and statistics; and particle representations of Boltzmann’s equation and methods of solution such as Monte-Carlo and particle-in-cell techniques. It employs software like MATLAB® or Octave.

### Course Outcomes

#### Course Goals for Students

Students who complete this module will:

- Become familiar with computational engineering and its mathematical foundations, at an elementary level.
- Deepen their understanding of the basic equations governing the phenomena in Nuclear Science and Engineering.
- Understand the methods by which physical problems can be solved using computation.
- Develop experience, confidence, and good critical judgment in the application of numerical methods to the solution of physical problems.
- Strengthen their ability to use computation in theoretical analysis and experimental data interpretation.

### Instructor Interview

> "“…[E]very advanced engineering and physical science student needs to be able to use numerical methods in their research and professional activities, and they need to know the rudiments of how those methods work."

—Ian Hutchinson

*Below, Prof. Ian Hutchinson describes various aspects of how he taught* 22.15 Essential Numerical Methods.

#### A Foundational Course for Graduate Study and Research

The rationale behind the course is that every advanced engineering and physical science student needs to be able to use numerical methods in their research and professional activities, and they need to know the rudiments of how those methods work. Especially in the nuclear field, many large codes are routinely used for all sorts of design and performance calculations. An MIT-trained student should have some basic understanding of the sorts of things that such codes contain, and what their constraints, strengths, weaknesses, and limitations are. Just as every serious engineer should know how an internal combustion engine works, but not the details of every car’s design, so they should know, for example, how a thermal hydraulics code they might use works, but not necessarily its detailed design.

Many Nuclear Science and Engineering graduate students become not just code users, but code developers in their research activities, developing scripts and programs to analyze data, to link large calculations together, or even to implement large-scale parallel numerical calculations. Those that specialize in computational research are going to need more than is in the course Essential Numerical Methods, but the course gives a wide perspective on computational engineering. That helps a specialist to see their detailed application in context, and understand the framework of computational science and engineering.

In developing this course, I first made the decision on principle that it would be language-agnostic. That is, it does not require anyone to use a particular programming language or mathematical system. However, since I also decided (partly for lack of time) that no direct matrix algorithms (multiplication, inversion, decomposition, or eigenanalysis) would be taught, students need access to a system that has those algorithms as libraries or built in. MATLAB® and its open source alternative Octave are the easiest to use because of their focus on matrices and their use of matrix notation. However, Python, Mathematica®, and C have also been used by students, and IDL® would certainly also work fine.

#### Balancing Breadth and Detail in a Half-Term Course

The course is constrained to occupy only half a term, because there are several other required “modules” common to all students in their first year. That forces the course to be concise, which is a challenge to both students and instructor.

Because the course is so compressed, tough choices have to be made about material to leave out. One thing that is omitted is formal mathematical proofs. That worries some students with mathematical aspirations, but it shouldn’t. I believe it is much more important in this topic to develop mathematical insight than to learn rigorous proofs. There is still a lot of mathematics in the course, because we really dig into questions like order of convergence, stability, and computational cost. So this is not just a “survey” course, floating at high altitude and never getting our boots dirty. What we do is drill down into certain topics chosen from the whole field and erect some solid knowledge posts. They are very spaced out, but they serve as an anchor framework that enables students to understand the field as a whole, and to construct more detailed knowledge structures in particular areas later as they might have need.

I have no qualms about the material or the abbreviated style of the module and how the course is taught. But I do think that less experienced students find a serious challenge in the required speed of assimilation. The intensity of the course—like a boot camp—is exciting; but sometimes a learner just needs time to let the ideas soak in and become a part of one’s unconscious mental framework. A half-term module just doesn’t have the leisure for that. My hope is that it gives a big push forward in understanding computational methods, and the resultant momentum carries the students beyond the end of the module so that the assimilation takes place more fully in succeeding months and years.

### Curriculum Information

#### Prerequisites

[*12.010 Computational Methods of Scientific Programming*](https://ocw.mit.edu/courses/12-010-computational-methods-of-scientific-programming-fall-2011) or permission of instructor.

#### Requirements Satisfied

This course is one of six half-semester courses that comprise the core course requirement for [PhD students in Nuclear Science and Engineering]([http://catalog.mit.edu/schools/engineering/nuclear-science-engineering/#phd-dsc](http://catalog.mit.edu/schools/engineering/nuclear-science-engineering/)
). Students must pass the final exam with a B or better. They can take the exam without taking the course, but hardly any do.

#### Offered

Every fall semester, during the first half of the term.

### Assessment

The students’ grades were based on the following activities:

- 20% Homework exercises (best 5 of 9 scores)
- 5% Class interaction
- 75% Final exam

### Student Information

#### Enrollment

34 students

#### Breakdown by Year

All first-year and second-year PhD students.

#### Breakdown by Major

Essentially all the students were from Course 22, but I believe that almost any MIT engineering graduate student could benefit from it, since the numerical aspects are not particularly unique to Nuclear Engineering.

### How Student Time Was Spent

During an average week, students were expected to spend 12.5 hours on the course, roughly divided as follows:

#### Lecture

Met 2 times per week for 1.5 hours per session; 13 sessions total.

#### Recitation

Recitations can help greatly, although we do not always have the teaching assistant resources to hold them.

#### Out of Class

Outside of class, students read the [course notes](https://ocw.mit.edu/courses/22-15-essential-numerical-methods-fall-2014/pages/lecture-notes/) and work on [exercise assignments](https://ocw.mit.edu/courses/22-15-essential-numerical-methods-fall-2014/pages/assignments/).

Each lecture has a set of exercises associated with it. Most of these include programming assignments. Naturally students vary greatly in their experience and expertise in programming. One objective of the course is to help students gain confidence using numerical languages or systems in solving problems. A student with little computation background naturally has to work a bit harder on the programming exercises. The result is that the inexperienced students gain the most. However, I have found that essentially all of them are able to get the exercises done with sufficient consultation. The students report that it does not take them excessive time to complete the assignments, which are considered to be allocated about 3 times as much as the lecture durations.
