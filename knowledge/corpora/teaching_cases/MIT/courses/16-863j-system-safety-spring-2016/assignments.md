> 检索摘要：16.863J System Safety（Spring 2016，Graduate）的「Assignments and Class Project」。页内标题：Assignments and Class Project；List of Accidents。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/16-863j-system-safety-spring-2016/pages/assignments-and-class-project/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments and Class Project

**Assignment 1**: Citichem video

Watch the Citichem video [*Acceptable Risks*](http://www.imdb.com/title/tt0090586/). Directed by Rick Wallace. Color, 92 min. 1986 and identify the factors that contributed to the accident. Do you think there a “root cause”?

**Assignment 2**: Answer the “[How Safe is Safe Enough?](https://ocw.mit.edu/courses/16-863j-system-safety-spring-2016/pages/assignments-and-class-project/assignment-2-how-safe-is-safe-enough/)”

**Assignment 3**: Answer the reading questions on [Buy at MIT Press](https://mitpress.mit.edu/9780262016629) Leveson, Nancy G. Chapters 1–3 in *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press, 2012. ISBN: 9780262016629. [Preview with [Google Books](http://books.google.com/books?id=6dDxCwAAQBAJ&pg=PAfrontcover)]

- Chapter 1: Which of these factors are true for your field or industry? Are any of them not true?
- Chapter 2:

1. Section 2.1: Think of an example (not in the book) of a system that is reliable but not safe, safe but not reliable, conflicting?
2. Section 2.3: Chernobyl had a calculated PRA of 10<sup>-9</sup> per year (or a mean time between “failure” of 10,000 years) so what do you think went wrong in the analysis? Or did it? (There is a description of what happened at Chernobyl in Safeware Appendix D, but you do not have to read it to answer the question).
3. Section 2.5: Consider the hardware definition of failure. Does it make sense to talk about a failure of a pure abstraction like software? In what way could it make sense? In what ways is it different?
4. Section 2.7: Why do you think it is so hard for people to let go of the concept of blame?
5. Are there any other assumptions of the traditional approaches to safety that you think are no longer always true or additional goals for a new approach to safety?

- Chapter 3:

1. What is an example of another emergent system property besides safety? Why is it emergent?
2. Have you ever worked on a safety-critical system project? If so, how was safety handled?

**Assignment 4**: Accident report

1. Find at least 2 instances of hindsight bias in the [SBS Tank 731 overflow accident report (PDF)](https://ocw.mit.edu/courses/16-863j-system-safety-spring-2016/resources/mit16_863js16_tank_report/).
2. Summarize an accident report (from the list provided below) and answer questions on: What was cause? Is there a chain of events described? Do you see any hindsight bias? Who or what was blamed? Also, summarize the report it in a 5–10 minute presentation. Some of the reports are quite long. For this assignment you should read at least the introduction and conclusions of the report. Include in your presentation the main events, the causes identified in the report, and their recommendations. Did you find any hindsight bias in the report? If you can find a short (under 2 minute) video online about your accident, feel free to include a link to it in your presentation. We’ll download any videos to my computer before class. You will do the CAST assignment on this accident.

### List of Accidents

- Air France 447
- Anacortes Tesoro Refinery
- Texas City: BP Refinery explosion [West Texas explosion would be interesting also but I don’t know if there is enough information available]
- Chevron Richmond report (CSB)
- Gol 1907 and Embraer collision (interesting because investigated by both Brazil and NTSB and they reached different conclusions. What would CAST show? I have access to people in Brazil to question about this (both in Brazilian ATC and Embraer)
- Cali Columbia American Airlines crash (especially interesting human factors information provided)
- Deepwater Horizon (Presidental Oil Spill Commission report is very well done and lots of information available about this accident)
- Woodley Park DC Metro
- Mars Polar Lander
- Minneapolis highway bridge collapse
- Hudson river midair collision between a helicopter and small plane
- 2009 Schiphol airport (Amsterdam), Turkish Airlines B737 [Sidney Dekker wrote a human factors report on this accident that is up on the class website]
- Shell Moerdijk accident

You can also come up with one of your own, but please get my permission first to make sure it is a good accident to analyze (e.g., that enough public information available, etc.). Note that information in the press, before an official investigation is done, is almost always completely wrong.

**CAST Analysis Assignment** (can be done in groups of up to 2 people)

Create a CAST analysis for your accident. Compare your results with the results in the official report. Feel free to use information from online resources or news articles to supplement the information in the report if you want. Be sure to cite any resources you use. Some hints:

- Make sure your hazard describes the overall state of the system, and not specific behavior of an individual component like software, engines, pilots, etc.
- Your control structure should include the responsibilities for each controller, the possible control actions, and feedback arrows. Label each arrow with the particular actions / information they represent. Add controllers if necessary to capture any additional causes you found.
- Analyze the physical process / system. Identify:
  - Safety responsibilities of physical system (what must it do)
  - Physical controls (what design features were meant to fulfill the safety responsibilities)
  - Failures and inadequate controls (what went wrong)
  - Contextual factors (why did those things go wrong)
- Analyze the controllers: Remember that a controller can be automated software, human operator, human manager, or an organization like FAA or congress). Identify:
  - Safety-related responsibilities (what goals they should achieve)
  - Unsafe Decisions and Control Actions (what they did that was unsafe)
  - Process model flaws (what did they believe about the system that explains their actions)
  - Context (what other factors pressures, incentives, history, etc.—explain their actions)

**Project Instructions**: Do a hazard analysis of a real system.

[ESW] = [Buy at MIT Press](https://mitpress.mit.edu/9780262016629) Leveson, Nancy G. *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press, 2012. ISBN: 9780262016629. [Preview with [Google Books](http://books.google.com/books?id=6dDxCwAAQBAJ&pg=PAfrontcover)] as

1. Write a description of the system, what are the goals, have there been accidents in the past with it? (if it is not new). What are the technical system safety requirements? [ESW] 7.3 and the overall management or organizational requirements [ESW] 7.4
2. Define the accidents and hazards of importance to the stakeholders. Select one or two important ones to analyze.
3. Describe the hierarchical safety control structure that either exists or needs to be created.
4. Perform a Step 1 analysis for at least one human (operator) and one automated (software) part of your control structure. Rewrite the results as requirements.
5. Perform a Step 2 analysis for the unsafe control actions you identified in Step 4. Generate recommendations for human factors design and technical design from the results.
6. What information should be passed to operations that you have created in your analysis? Create a plan for operators to use that information.
7. What recommendations do you have for the overall safety control structure for the organization that will use this system?
8. Is there an existing hazard analysis for this system? If so, compare the results with what you got using STPA. If not, did you find hazard causes that involved non-failure of components?
