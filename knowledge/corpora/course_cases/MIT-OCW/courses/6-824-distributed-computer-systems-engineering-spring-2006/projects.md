- Source: https://ocw.mit.edu/courses/6-824-distributed-computer-systems-engineering-spring-2006/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

Due date for team list: Lec #6
Due date for project proposal: Lec #8
First project conferences: Lec #10
Due date for first draft report: Lec #16
Second project conferences: Lec #17
Due date for second draft report: Lec #19
Project demonstration day: Lec #22
Due date for completed project and report: Lec #24

### Introduction

For the final project in 6.824, you’ll form groups of three or four students, pick a system you want to build, design it, implement it, and write a report about it. The project has six deadlines:

- Team list. Send us the names of the people in your project group. Your group should have three or four people.
- Project proposal. The proposal is a one-page description of what your project will be. It should state what problem you are solving, why it’s a useful or interesting problem, what software you will write, and what the expected results will be. You won’t be judged on your proposal; it is there to help you to get started. We’ll give you written feedback about your proposal and then meet with you to discuss it.
- First draft report. This should include a draft of your report’s abstract, introduction, related work, and design sections. These sections should be in good shape, close to what they would look like in the final report. Be sure that the draft clearly states what your project’s goals are, why those goals are worthwhile, and how you’re going to achieve those goals. We’d like your draft report in Postscript or PDF format; you can e-mail us either the draft or a link to it. We won’t grade these drafts; we’ll just e-mail you comments intended to help you write a good final report. We will hold a second set of project conferences to discuss your first draft with you.
- Second draft report. This report should include a detailed design and implementation section. By this time your implementation should be well on its way to completion.
- Demonstration Day. During class you’ll have five minutes to impress your colleagues with how cool your system implementation is. We will supply two projectors and screens; you should bring a laptop that’s running your demonstration. You’ll set up on one screen while the previous group is presenting on the other screen. You should plan out the demo in detail in advance.
- Project report. Your report should be patterned after the research papers we have read in class. See the next section (Grades) for a description of what we expect. The report must be ten or fewer pages in length (see below for formatting details).
- The project is to be executed in teams of 3 or 4 students. We will not make exceptions: we will not allow smaller or larger teams. Find team-mates and send their names by e-mail to the TA. The email is due soon (see the list of deadlines at the top of this page).

### Grades

Your project grade will be based on the quality of your report, on the usefulness of the system you’ve built, on the extent to which your design is a good fit for the problem you’re solving, and on how useful your new ideas and techniques might be to other people building distributed systems.

When evaluating your report, we will look at both content and writing.

We expect your report to answer the following questions:

- What problem are you solving?
- What is the motivation for solving that problem? Why is the problem interesting and challenging? Why would a solution be useful?
- How have you solved the problem – how is your system designed?
- Why is your design good? What key decisions and trade-offs have you made? Is your design the simplest reasonable design?
- Does your solution fit well with the rest of the system? If your solution requires modifying every piece of hardware, software, and data in sight, it won’t be credible, unless you can come up with a very good story why everything needs to be changed.
- What new ideas or techniques have you developed as part of your design? What can others learn from your work?
- How does your implemented system work?
- Can you demonstrate that your system does indeed solve the original problem? Typically you’ll do this with an experimental evaluation, and present quantitative results.
- What is the relationship between your work and previous solutions to similar problems? Your report should include a Related Work section outlining the existing work that’s closest to your project, and explaining how your design is different or better.

A good report will also be well written:

- Is the report easy to understand?
- Is it well organized and coherent?
- Does it use diagrams where appropriate?

### Suggestions for projects

You should feel free to propose any project you like, as long as it is related to operating systems or distributed systems and has a substantial system-building and evaluation component.

Doing a good project is a daunting task. The most successful projects tend to be very well defined and modest in scope. We (the 6.824 staff) are very happy to be involved in all stages of your project. Please, come talk to us about your project ideas, how you should execute the project, what you should write about in your final report, etc.

Feel free to base your implementation on the code that we supply you for the labs, or on your lab solutions.

You could look for inspiration about hot topics in the on-line proceedings of recent [SOSP](http://www.cs.rochester.edu/meetings/sosp2003/), [OSDI](http://www.usenix.org/events/osdi04/), [Usenix](http://www.usenix.org/events/usenix04/), and [NSDI](http://www.usenix.org/events/nsdi04/) conferences. You might also want to look at 6.824 projects from previous years. ([PDF](https://ocw.mit.edu/courses/6-824-distributed-computer-systems-engineering-spring-2006/resources/prev_projects/))

If you’re having trouble thinking of a project idea, some of the topics below might help get you started.

- Build a more full-featured version of your distributed NFS server lab, perhaps patterned on Frangipani and Petal.
- Figure out how BitTorrent works and build something better.
- Rumor has it that BitTorrent has a hard time keeping its directory server working, because parties who find BitTorrent offensive cause the directories to be shut down. Build a more survivable BitTorrent directory.
- Build a distributed game for large number of users.
- Build a scalable Gnutella.
- Perhaps all computers will soon have built-in secure computing hardware such as [XOM](http://www.xom.nu/)™. Such hardware can certainly be used to restrict what computers can do, for example by enforcing copy protection. It’s also possible that secure execution hardware could be used to make computers more useful; for example, it might allow secure execution of Java™ applets or Web browser plug-ins or SETI@Home software, or store your passwords or RSA private keys or credit card numbers securely, or help players of multi-user network games convince each other they are not cheating, or let you walk up to anyone’s computer and use it (and trust it) as if it were your own. Design an application in this space and implement it as realistically as you can. Depending on your ambition you may have to simulate the required hardware and operating system support.
- ISPs and users alike benefit if all of a network’s links are driven at high utilization – that is, if network capacity doesn’t lie idle. Right now high total utilization is achieved with a combination of TCP’s congestion control and ISP traffic engineering (re-routing flows from overloaded links to idle links). Another approach might be to spread out the data people want to fetch over many servers, so that each file fetch requests small parts of the file from many different servers; this might spread the total network load, decrease the variation in load among links, and thus allow higher total utilization. Your task is to design and implement such a system and evaluate whether it does any good.
- Build a mechanism to automatically detect and prevent network break-ins or other unwanted traffic such as distributed denial of service attacks. It might help to correlate network traffic observed at many different points.
- Build a service on top of the [PlanetLab](http://www.planet-lab.org/) research test-bed.
- Make a distributed shared memory (DSM) system, so that processes running on different machines can share an address space. You would need a plan to allow caching but maintain consistency. You would also want to find at least one program that could take good advantage of DSM, to help you evaluate your system.
- Design and implement a disk scheduler that enforces priority. The point would be to give high priority to disk reads that interactive processes are waiting for. Lower priority would be given to reads by non-interactive programs, background page-outs, read-ahead, delayed writes, etc. This might make your Emacs and X Windows® faster at the expense of background compilation. You would need to demonstrate that the scheduler actually improved some aspect of system performance. The danger is that there is probably a tradeoff between enforcing priority and scheduling the disk efficiently.
- Build a service that maintains consistent replicated data. You could build a general-purpose service (like DDS) or an application that replicates in a way tailored to that application’s needs (like the Porcupine mailbox service ([PS](http://www.cs.washington.edu/homes/bershad/Papers/sosp.ps)).)
- Build a file synchronizer.
- Implement a system like Network Objects in C++.
- Design and build a proxy that provides a file-system interface to something other than files on the server’s disk. For example, build a front end to a database. This would be a useful tool for making MIT server resources such as Hesiod and Moira accessible with a file-system interface. The challenge is figure out how to provide a sensible interface to objects that don’t act like standard UNIX® files.
- Improve NFS performance by adding support for batched commit of arbitrary operations. This might let the client cache a sequence of operations (such as creates, renames, and writes), and them commit them to the server all at once. The server could then write the whole batch to disk at once. This arrangement would be particularly attractive if the server’s file system used a log, like SGI XFS or Hagmann’s Cedar file system, or performed checkpointing like Netapp’s WAFL. You might need to provide a way for applications to indicate the start and end of a batch of operations. The challenge here is to achieve higher performance while retaining reasonable behavior after failures.

### What to Hand In

Check the top of this page for due dates.

Team list: e-mail your team list (three or four members) to 6.824 staff.

Proposal: e-mail your proposal to 6.824 staff. The proposal should be no more than two pages. It should be ordinary ASCII text, not an attachment or word processor file.

Draft reports: E-mail your drafts, in PDF format to 6.824 staff.

Final report: E-mail your final report, in PDF format to 6.824 staff. Put a tar file containing your project source code in ~/handin/final/source.tar.

**Your report must not exceed ten single-spaced pages in length. This is a limit on the total length, including references and appendices. Please use 11-point fonts and 1-inch margins.**

Make sure you save enough time to write a good report, since that’s what will determine most of your project grade.
