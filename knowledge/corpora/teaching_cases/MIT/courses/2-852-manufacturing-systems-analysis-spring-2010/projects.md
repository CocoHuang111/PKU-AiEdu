> 检索摘要：2.852 Manufacturing Systems Analysis（Spring 2010，Graduate）的「Projects」。页内标题：Projects；Procedure；Grading；Sample Ideas。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/2-852-manufacturing-systems-analysis-spring-2010/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

The goal of the project is to give you an opportunity to demonstrate your mastery of the ideas of the course in a less restrictive, more realistic manner than in an exam or a homework assignment. This means there must be some mathematical modeling and/or analysis similar in style to the material in the book or in my slides. A report will be required, and it should be written in a professional manner.

### Procedure

1. Discuss project ideas informally with me.
2. Write a one-to-two page project proposal by Session #11. In the proposal, describe the goal of the work and the procedure that you will follow. If I approve, you may do the project.
3. I may ask for a revision of the proposal.
4. Discuss the project with me as you are proceeding. Ask for help if needed.
5. Give me an informal written progress report by Session #15.
6. Give me an informal written progress report by Session #20.
7. Continue discussing the project with me as you are proceeding. Ask for help if needed.
8. If time permits, presentations will be encouraged.
9. Write a final report and hand it in by the last day of class.

Talking with me is very important. I will do my best to prevent you from doing something infeasible, trivial, or inappropriate.

If you would like to do your project as a team, I will consider it. However:

1. Such a project must have sections that are clearly marked to indicate who wrote what.
2. Each participant must demonstrate mastery of the course material as described above. For example, if one member of the team developed a mathematical model and analyzed it, and another member wrote a simulation and tested the validity of the model, this would not be acceptable.
3. The result should be at least as great as the sum of its parts.

### Grading

Creativity, thoroughness, professionalism, and punctuality will be rewarded. If we have time to do presentations, a good presentation will also contribute to your grade.

### Sample Ideas

The following is a set of sample ideas. You are not restricted to them. In fact, if too many people want to do the same thing, some proposals may be rejected for that reason alone. Feel free to submit other ideas.

- If you have some factory experience, apply the models and methods of this course to a factory (or a portion of a factory) that you are familiar with. Show how to improve the design of the factory, or how to design an operating policy.
- If you have some factory experience, critique the models and methods of this course. Describe their limitations, that is, why they would not be helpful in redesigning or operating the factory you are familiar with. Propose one or more alternate models, and go as far as possible in analyzing and developing them.
- Develop some tools that will help the optimization of a production system design.
- Add financial calculations to the transfer line models. That is, do a present value analysis, cash-flow analysis, etc.
- Write software to implement some models (from the course, from MIT theses, from the literature) that have not already been implemented.

If you do not have access to a factory, you may need a more mathematical/theoretical approach.

- Extend the quality model with an LIFO buffer. Does it improve performance?
- Optimize a line with non-exponential models. How do up-time/down-time variances influence optimal buffer size?
- Do a numerical study of the push-pull boundary. (The boundary is a relatively big buffer. Upstream of the boundary is a tandem line – push. Downstream is a CONWIP loop – pull.)
- Extend optimization to split-merge (**not** assembly-disassembly) systems.
- Model a 2-machine, one-shared-buffer line with two part types. Model a 2-machine, two-separate-buffer line with two part types. (In both cases, it will be important to propose a policy for choosing which part to work on when both are possible. Assume no setup costs or times. Assume specified demands for each part type or a specified ratio of demands.) Questions to answer: How much do we gain in production rate by sharing one big buffer instead of having two homogeneous buffers? What is the impact on inventory?
- Do some interesting, but not too ambitious, original mathematics. It is hard to know in advance what will be easy and what will be difficult. (That makes it hard to make suggestions, and impossible to guarantee that the suggestions are doable.) For me to approve such a project, you must include an outline of the proof (or preliminary simulation results, or whatever) when you hand in the proposal.
