- Source: https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### Description

The goal of the final project is to carry out a thoughtful experiment or analysis on an underactuated robot, an algorithm for an underactuated control, or a combination of both. It should involve some elements of dynamics (designing the dynamics or analysis of dynamics with or without control) and/or control, depending on the emphasis of your project. Use of the computational machinery emphasized in class, however, is required. The use of real hardware (if and when it is possible) is cautiously encouraged, providing that it does not come at the expense of a careful analysis.

### Project Components

| COMPONENTS | DESCRIPTIONS |
| --- | --- |
| Proposal | A half-page description of the final project topic |
| Presentation | An 8-minute discussion of your analysis and results |
| Report | A 6-8 page, two-column paper similar to those found in conference proceedings |

In the presentation, you should describe the problem you chose, explain why it is interesting or important, describe the technical approach you took, explain why you chose that approach, report results, and comment on implementation details. In the report, cover the same points as in the presentation but with more details on implementation.

### Project Topics

Some potential topics are described below. The course staff will provide you with feedback on the scope and direction of your proposal shortly after we receive it. If you plan on doing a team project, please make this clear in your proposal.

**Value iteration in continuous space with discontinuities**. Many of you correctly observed that the value iteration solution of the bang-bang double integrator had a systematic error in the switching surface (due to the meshing representation). Propose a variant of value iteration, or simply a different mesh representation, which is better suited for problems with discontinuous policies or value functions. The torque-limit simple pendulum swing-up task should be rich enough to validate your method.

**Hopper gymnastics**. Can you modify the existing Raibert hopper simulation to accomplish some of the gymnastic maneuvers (e.g. flip, aerial) shown in the videos in class? Are two legs necessary?

**Value iteration struggles with high-dimensional problems**. Is it possible to combine value interation with some of the other control ideas in class to effectively reduce the dimensionality of the problem? At what cost?

**Challenge problems**. Tackle one (or more) of the challenge problems in the course lecture notes.

**Research-related topics**. Many of you will be able to do a project that is closely related to your current research. This is completely acceptable provided that the subproblem you are solving for this class is clearly defined.

**Other topics**. Please feel free to contact the course staff for other ideas or to discuss potential ideas.
