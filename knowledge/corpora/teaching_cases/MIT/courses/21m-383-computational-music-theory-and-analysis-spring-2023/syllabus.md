> 检索摘要：21M.383 Computational Music Theory and Analysis（Spring 2023，Undergraduate、Graduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Prerequisites；Description；Requirements and Grading；Required Text and Materials；Recommended texts；Topics。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/21m-383-computational-music-theory-and-analysis-spring-2023/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session + 1 hour asynchronous lecture content

### Prerequisites

A background in music theory, e.g., [*21M.301 Harmony and Counterpoint I*](https://ocw.mit.edu/courses/21m-301-harmony-and-counterpoint-i-spring-2005/), [*21M.302 Harmony and Counterpoint II*,](https://ocw.mit.edu/courses/21m-302-harmony-and-counterpoint-ii-spring-2005/) or [*21M.303 Writing in Tonal Forms I*](https://ocw.mit.edu/courses/21m-303-writing-in-tonal-forms-i-spring-2009/)*,* and prior experience in computer programming, e.g., *6.1010 Fundamentals of Programming,* is required or by permission from the instructor.

### Description

This class presents major approaches to computational music theory and musicology in the symbolic (score-based) domain. It covers algorithms for music theory, encoding, corpus studies, musical search and similarity, feature extraction and machine learning, music generation, and computational music perception. Other topics include repertory access and computational bias. Programming assignments are given in Python using the MIT-created music21 toolkit. The class culminates in a two-person-group research project in computational music theory, computational musicology, or creative music theory that will be presented to the class.

This class meets the MIT [HASS-A course](https://registrar.mit.edu/registration-academics/academic-requirements/hass-requirement) requirement.

### Requirements and Grading

As this is a small class, we want to and should be able to hear each other’s thoughts and ideas in nearly every class meeting. Thus, participation, preparation, and presentations will form a graded subject component.

The approximate grade breakdown will be as follows:

|  |  |
| --- | --- |
| Midterm exam | 10% |
| Problem sets and other assignments | 50% |
| Final project: recorded presentation | 20% |
| Attendance, <br> preparation <br> , and participation | 20% |

A failing grade may be assigned for failure of any of the components of the class.

Please note the **preparation** in bold under the attendance/participation grade.

Problem sets (PSets) and the midterm will be assigned a numeric grade and a letter grade. Other components will be given letter grades only. The lowest PSet grade will be dropped if it is turned in with at least one-third of the problems attempted. Late assignments will be lowered by 5% if they are turned in before any solutions have been distributed and 20% afterward.

The final project is an original research or creative project using materials from this class. It will consist of a pre-recorded presentation. The final project will generally be done in groups of two. No groups larger than three will be approved. Algorithmic composition using AI / ML / deep learning techniques will also not be approved because they have received consistently poor results. Students receiving graduate credit must also write the presentation up as a paper.

### Required Text and Materials

- [music21 User’s Guide, Chapters 1–30](https://www.music21.org/music21docs/usersGuide/)
- Laptop computer with Windows or MacOS installed. *If you choose to use Unix, etc., any problems with any assignments will fall entirely on you and I cannot provide technical support. Set up a dual-boot environment for win/ac.*
- music21 v.8.1 (to be upgraded to v.9 soon) and Python 3.10 or higher installed

#### Recommended texts

- David Huron. [*Sweet Anticipation: Music and the Psychology of Expectation*](https://mitpress.mit.edu/9780262582780). MIT Press, 2006. ISBN: 9780262582780. [Preview with [Google Books](http://books.google.com/books?id=uyI_Cb8olkMC&pg=PAfrontcover)]
- Dmitri Tymoczko. *A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice*. Oxford University Press, 2011. ISBN: 9780199887507. [Preview with [Google Books](http://books.google.com/books?id=ODSt58Yk2YYC&pg=PAfrontcover)]
- Carol Krumhansl, [*Cognitive Foundations of Musical Pitch*](https://global.oup.com/academic/product/cognitive-foundations-of-musical-pitch-9780195148367?cc=us&lang=en&) (Oxford, 1990). ISBN: 978-0195148367. [Preview with [Google Books](https://www.google.com/books/edition/Cognitive_Foundations_of_Musical_Pitch/aJDEVqyArr4C?hl=en&gbpv=0)]
- David Temperley. “Probabilistic Foundations and Background.” Chapter 2 in [*Music and Probability*](https://mitpress.mit.edu/9780262515191). MIT Press, 2006. ISBN: 9780262201667. [Preview at [MIT Press](https://direct.mit.edu/books/monograph/2326/chapter/60959/Probabilistic-Foundations-and-Background)]

#### Topics

|  |  |
| --- | --- |
| Introduction | How Do Computers Hear Music? |
| Topic 1: | Representations of Durations and Pitches |
| Topic 2: | Musical Score Encoding |
| Topic 3: | Musical Hierarchies + music21 Streams as Containers |
| Topic 4: | Symmetry, Equivalence, and Intervals |
| Topic 5 part 1: | Corpus Analysis. Representing the World in Computation |
| Topic 5 part 2: | Quantitative Musicology/Theory: Research Beyond the Score |
| Topic 6: | Chords, Counterpoint, and Voice Leading |
|  | Mid-Term Examination (in class) |
| Topic 7: | Scales, Keys, and Roman Numerals |
| Topic 8: | Algorithmic Composition and Performance |
| Topic 9: | Vocabulary Reduction |
| (Interlude 1) | Similarity, Difference, and Alignment |
| Topic 10: | Feature Extraction and Machine Learning |
| (Interlude 2) | Computational Analysis Beyond Classical/Rock/Pop Music |
| Topic 11: | Music Cognition and Psychology with the Computer |
|  | Final Presentations (no final exam) |

Classes will proceed according to individual topics, generally taking 2–4 class meetings including the asynchronous lecture/materials. There are four parts to most topics:

|  |  |
| --- | --- |
| a) | Introduction to the topic (e.g., what is Roman numeral analysis?)—this might be done very quickly if the topic is well known to all of us. |
| b) | In-class/written discussion of the topic, including readings (e.g., tricky issues with Roman numerals in general and on a computer) |
| c) | Work on a PSet on the topic (generally 5–7 days between assigning and due). (e.g., write your own Roman numeral analyzer). |
| d) | Follow-up discussion, including “unlocking” the equivalent tool in music21 or elsewhere. (e.g., here’s how to use music21’s “Roman” module). |

At first, topics will be kept separate, so we’ll finish topic 1 before moving on to topic 2. But after a while topics will overlap, so that while working on the PSet for topic 4 we start introducing topic 5. I will try to make this as *non-confusing* as possible. There are 11 topics but only 9 PSets this semester.
