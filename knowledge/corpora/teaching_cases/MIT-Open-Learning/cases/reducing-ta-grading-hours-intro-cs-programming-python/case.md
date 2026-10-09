> 检索摘要：该材料匹配教学问题为助教（TA）在编程入门课中人工评阅负担过重且响应滞后，影响复杂问题的深度反馈，适用于MIT 6.0001 Introduction to Computer Science and Programming Using Python（Electrical Engineering & Computer Science, Course 6）。实施策略为分层自动化：对30%结构明确、答案唯一的问题启用自动评分（auto-grader）；针对常见编码错误（如循环未重置、变量未初始化）开发实验性自适应提示（Adaptive Hinting）系统，向学生推送定制化纠错建议。工具为MOOC基础设施、CAT-SOOP自动评分平台及自研适应性反馈机制。评价方式体现为自动反馈即时性与TA转向高阶问题的手动评阅。已陈述效果包括：TA评阅工时减少超100%；学生获即时纠错提示；TA得以集中精力处理答案多元、需深度理解的复杂编程题；该模式正扩展至6.0002课程。

- Source: https://openlearning.mit.edu/mit-faculty/residential-digital-innovations/reducing-ta-grading-hours-intro-cs-programming-python
- source_format: html
- capture_date: 2026-10-09

---

# Reducing TA Grading Hours: Intro to CS Programming in Python

6.0001 Electrical Engineering & Computer Science (Course 6)     ![Ana Bell](https://openlearning.mit.edu/sites/default/files/styles/event_news_detail/public/residential-innovations/anabell_web.jpg?h=4e4bb880&itok=k2D5DWiw)       Faculty/Instructor  Ana Bell    Digital Innovations & Tools  Adaptive Hinting

In MIT courses 6.0001 and 6.0002, Digital Learning Fellow Ana Bell implemented MOOC-based interventions in order to facilitate quicker student comprehension and reduce the TA grading burden.

### **Educational Challenges**

**Problem:** How to reduce the hours TAs spent grading without sacrificing grading accuracy or responsiveness to coding complexities?

**Solution:** Bell used the auto-grader for problems with structured, one-dimensional answers. If the student got the answer correctly, chances were strong that his or her code was correct. 30% of the problems fit this profile and by using the auto-grader on them, Bell was able to reduce TA grading hours by over 100% and thereby leave more time for manual grading of complicated questions for which there was a range of possible correct answers.

**Problem:**How to provide personalized feedback on common student pitfalls and misunderstandings?

**Solution:**With the help of a graduate student, Bell designed an automated feedback system that identified common pitfalls in student code and responded with suggestions and prompts customized to an individual student’s error. Such suggestions could be, for example, a reminder to re-initialize a loop, or pointing out that the student was incrementing over and over again without re-setting. This automated feedback system is in its experimental phase but it shows promise for future iterations of the course.

### **Key Take-Aways**

Through identifying common pitfalls and providing immediate feedback, auto-grading and adaptive hinting are tailored to common student errors. This, in turn, frees up TA time to give personalized attention to more complicated problems.

*If you are interested in using the concepts from this case study in your teaching, please contact**MITx Residential**to speak with a consultant.*
