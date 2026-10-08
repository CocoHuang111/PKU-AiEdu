> 检索摘要：15.879 Advanced Research Seminar in System Dynamics:（Spring 2014，Graduate）的「Assignments」。页内标题：Assignments；Homework；Homework 1；Homework 2；Replicate & Understand Sterman 85 Model；Projects；Tutorials；Tutorial Topics；Method of Simulated Moments (MSM)；Kalman Filtering and Estimation；Eigenvalue Analysis；Maximum Likelihood Estimation and Confidence Intervals。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/15-879-research-seminar-in-system-dynamics-spring-2014/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

### Homework

There are two early homework assignments. There is no need for submission or grading on these assignments.

### Homework 1

Do Challenge on Sterman, John D. Parts 1–3 in *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill Higher Education, 2000, p. 624. ISBN: 9780072311358.

### Homework 2

#### Replicate & Understand Sterman 85 Model

This homework includes replication and analysis of the model in:
Sterman, John. “[A Behavioral Model of the Economic Long Wave](http://dx.doi.org/10.1016/0167-2681%2885%2990023-X).” *Journal of Economic Behavior and Organization* 6, no. 1 (1985): 17-53.

The equations for the model are listed at the end of the paper. Your goal is to build that model in Vensim, replicate its behavior, specifically, try to replicate the behavior in Figure 8 with self-ordering mechanism active, and understand where that behavior comes from in terms of different contributing loops and structures.

This is a relatively simple model with pretty interesting behavior modes. Replicating it is a great exercise to learn good model structures and formulations, and the analysis will be instructive.If you can’t get the Sterman ‘85 model to equilibrium, that is fine, just replicate the behavior mode in figure 8 and explain that without starting from equilibrium.

### Projects

The course is organized around your team projects, which are expected to be at a quality sufficient to generate journal publications. You select your team and your project by the first session. Teams of 2–4 students will work on the projects. Teams will follow a structured process for enhancing the project. Adherence to this process is critical to enable timely management of the project. You will have presentations of your project progress every other week, providing an opportunity to receive feedback from the instructor and your classmates.

The final report from the project is a (preferably journal-submission-ready) manuscript that discusses the problem, the literature, the modeling and analysis work, and your results and insights. Use the [System Dynamics Review’s guidelines for authors](http://onlinelibrary.wiley.com/journal/10.1002/%28ISSN%291099-1727/homepage/ForAuthors.html) for formatting, length, and other style issues. Final reports are due by the last day of classes.

Projects are evaluated based on the final report, their progress throughout the semester, the openness to learning shown by the team, quality of modeling and analysis, and the insights the project has generated for all the parties involved. Each individual will anonymously evaluate and provide reviews for the other projects, and so will the instructor. Final project grade is an evenly-weighted average of instructor and student evaluations of each project.

Your team, or a subset of individuals in the team, is encouraged to submit a conference or journal article based on the project. We will discuss the potential target outlets, the co-authorship expectations, and other publication related issues as part of the course; here are a few guidelines for starting the conversation within your team about important issues:

- The distribution of tasks should be discussed and agreed upon early on by all team members. While specialization for different types of tasks (e.g. modeling, data collection) by different team members may be efficient for task completion, it is not for learning. It is highly recommended that all team members are aware of all of the steps that are being taken as part of the team’s work, and can replicate those if need be. Regular weekly team meetings are necessary, and often more frequent meetings are called for.
- If a project is part of the thesis for one of the team members, that team member is expected to contribute most significantly to the project, and have sole responsibility for some aspects of the work so that the results can be justified as part of the student’s thesis.
- Discuss your publication goals for the project early on and agree on a set of expectations and target outlets and dates.
- It helps if one individual takes the lead by the end of semester to push the publication forward and coordinate the process. That individual is usually (but not necessarily) the first author.
- To be part of coauthors for a submission each team member should have contributed significantly to some aspects of the project, from conceptualization and data collection, to modeling, analysis, and writing.
- If the team receives significant support and contribution from some other class participants or instructor, it is encouraged that co-authorship is discussed early and those individuals are invited as coauthors after agreement on the significance of their contributions.

### Tutorials

Your team is expected to develop a video tutorial that either (1) introduces one of the methods we cover in the course (e.g. optimization, calibration, differential games) using a simple example, or (2) clearly shows how to use a specific capability within Vensim to solve a common modeling problem. The pool of potential tutorial topics will be provided by the instructor. This exercise has multiple benefits for all involved. You will learn about the topic in your tutorial, as well as the tutorials developed by others in the class. Moreover, the repository of these tutorials will be a resource for yourself as well as future students; in fact you will benefit from some of such previous tutorials during this semester.

Please confirm your tutorial topic with instructor by the third class session. You will then develop a clear but brief (under 40 min) video tutorial and go through the motivation, problem definitions as well as step-by-step instructions of solving the problem. You can record the video using the trial version ofa video capture software such as [Camtasia](http://www.techsmith.com/camtasia.html)™. If you go this route, make sure you plan your recording within the trial period of the software, or any other method of your choice. The video tutorial should be detailed enough to allow anybody with access to Vensim DSS (or your implementation software of choice) to replicate your solution to the defined problem. Make sure your tutorial includes credits for your team and any other parties involved.

The tutorial topics are assigned to the tutorials on a first-come-first-served basis. The instructor will let you know about the first available topic, which will be your designated topic, and you can start working on your tutorial from then on.

Your tutorial video and any accompanying documents are due by the end of Spring Break. You will review the tutorials developed by other teams and provide your evaluation on the usefulness of the tutorial for a novice user of the technique through an anonymous online survey. These evaluations are used for specifying the tutorial portion of the grade.

### Tutorial Topics

Please select your team’s top three choices for tutorials from the list below and share the rank order with the instructor. The topics are assigned on a first-come first-served basis. You are expected to figure out how to do each problem under your topic of choice, and then implement that clearly and video-document the implementation process along with relevant explanations that allow a novice to the technique to learn this topic and apply it to problems of her choice.

#### Method of Simulated Moments (MSM)

The chapter by Jalali et al. (2014) in the [Readings](https://ocw.mit.edu/courses/15-879-research-seminar-in-system-dynamics-spring-2014/pages/readings/) section provides an easy overview of the method of simulated moments, and offers a simple exercise at the end of the chapter for model estimation and confidence interval approximation. The exercise’s solution in Matlab is available. Your goal is to implement and solve that exercise in Vensim, using Vensim’s optimization to solve the estimation problem. Note that you may need to make some changes to the Vensim models to correctly implement the method. In your video tutorial review the key formulations that leverage subscripts to implement MSM matrices and calculate different steps of the process. Go through the steps one by one, rather than using command scripts, so that viewers can follow all of the steps of the process.

#### Kalman Filtering and Estimation

Your task in this exercise is to apply the Kalman filtering and estimation technique to estimating a simple population drug use model. The estimation is conducted using synthetic data from the same model and many of the files for conducting the analysis are available, so your main task is to figure out the steps, explain them clearly, and implement the video tutorial. Read the chapter by Eberleinand Vensim help for background information.

#### Eigenvalue Analysis

In this tutorial you will use the Loop Eigenvalue Elasticity Analysis (LEEA) on the Industrial Structures model reported in Kampmann&Oliva 2006; see the introduction and tools in the chapter by Oliva and references therein. This is essentially replicating the analysis by Kampmann & Oliva using the currently available tools, and providing a tutorial that explains all the relevant steps for a novice user of LEEA.

#### Maximum Likelihood Estimation and Confidence Intervals

The chapter by Struben et al (2014; in course readings) provides an overview of maximum likelihood estimation and bootstrapping for estimation and confidence intervals. Your goal for this tutorial is to solve the challenge at the end of the chapter, only focusing on estimation of the model using MLE and determining the univariate likelihood intervals using likelihood ratio method in Vensim. The implementation provided with the chapter is in R, so you need to develop the estimation steps and confidence interval determination in Vensim.

Tutorial project examples can be found in the [Student Projects section](https://ocw.mit.edu/courses/15-879-research-seminar-in-system-dynamics-spring-2014/pages/student-projects/).
