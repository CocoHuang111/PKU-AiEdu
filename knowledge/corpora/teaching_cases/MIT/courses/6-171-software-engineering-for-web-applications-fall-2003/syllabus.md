> 检索摘要：6.171 Software Engineering for Web Applications（Fall 2003，Undergraduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Prerequisites；Description；Practical Stuff；Grading and Required Work；Participation in Design Reviews (30%)；Term Project (60%)；Mid-term Exam (10%)；Textbooks；Adoption by Universities and Companies；Course History。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-171-software-engineering-for-web-applications-fall-2003/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Prerequisites

This is a senior-level class at MIT where we expect the average student to be working on a bachelor’s or master’s degree in computer science, to have taken our introduction to computer science ([6.001](https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/)), to have taken our core software engineering class ([6.170](https://ocw.mit.edu/courses/6-170-laboratory-in-software-engineering-fall-2005/)), and to have done at least some programming during summer jobs.

That said, the class does not require any knowledge of particular computer languages or systems. I.e., the students will learn enough about the required tools as the course progresses.

Admission to 6.171 is by permission of instructor. If you’d like to take the class, please fill out the survey ([PDF](https://ocw.mit.edu/courses/6-171-software-engineering-for-web-applications-fall-2003/resources/survey/)) and return it via email. If you are unsure about whether your preparation is adequate, a good way to find out is by simply doing the work in the [first chapter/problem set](http://philip.greenspun.com/seia/basics) and including the URL of your running system in your survey. This will reassure us of your ability to install and maintain the multiple subsystems that are, unfortunately, required to support a modern Web application.

### Description

This is a course for students who already have some programming and software engineering experience, e.g., at MIT the prerequisite is 6.170, Laboratory in Software Engineering. In 6.171 we try to give students some experience in dealing with those challenges that are unique to Internet applications:

- Concurrency — 1000 people might be using the system at the same time
- Unpredictable load — 100,000 users might show up tomorrow even if only 100 are using the system today
- Security risks — an Internet application is forced to expose itself to attacks
- Opportunity for wide-area distributed computing, i.e., using “Web services” provided by other machines on the Internet
- Creating a reliable and stateful user experience on top of unreliable connections and stateless protocols
- Extreme requirements and absurd development schedules
- Requirements that change mid-way through a project, sometimes because of experience gained from testing with users
- User demands for a multi-modal interface: Web, mobile (WAP), and voice

The bottom line: we want one someone who has finished this course to be able to build [amazon.com](http://www.amazon.com/), [eBay](http://www.ebay.com/), or [photo.net](http://photo.net/gallery/) by him or herself.

This is a laboratory course where most of the learning occurs during the completion of problem sets. Students organize into groups of 2-4 for the purpose of building an online learning community. Each problem set is devoted to adding features and capabilities to the online community. We encourage students to work with a real customer or client. Good sources of clients for online communities include organizations that want knowledge sharing systems (intranets) and non-profit organizations that wish to operate a public online learning community within their area of expertise. Students who themselves have a passion for a particular topic sometimes build an online community in that area.

### Practical Stuff

One of the good things about 6.171 is that students are free to use tools of their choosing in completing the coursework. The upside of this is that if you’ve had a summer job in which you used Postgres and PHP (for example), you won’t be distracted during the semester by having to learn new syntax. The downside is that we, the teaching staff, can’t help you very much with setup and administration of tools. Each student is expected to set up and maintain his or her environment, on his or her own computer, ideally a couple of weeks before the start of the semester.

If you have not done any Web development already and therefore aren’t familiar with any of the standard tools, we can suggest some ways to configure your development server based on our past experience. The [Basics chapter](http://philip.greenspun.com/seia/basics) of the course text discusses tool options. In choosing tools, please note that 6.171 requires the use of an ACID-compliant relational database management system. You’ll learn the definition of “ACID” during the semester. But for now suffice it to say that MySQL is out; Microsoft® SQL Server, Postgres, and Oracle are in.

Here are some helpful links for things that are either popular or non-obvious:

- Microsoft .NET, SQL Server, Windows® 2003: these tools are available at no charge to MIT students doing coursework
- The Oracle database server: all the Oracle database server tools can be [downloaded](http://www.oracle.com/); these are available at no charge to developers worldwide; the versions that you download do not expire and are not crippled in any way
- [PostgreSQL](http://www.postgresql.org/)
- [AOLserver](http://www.aolserver.com/); if you need help plugging it together with Oracle or Postgres, look at [these forums](http://www.openacs.org/bboard/)
- Apache™: [Apache HTTP Server Project](http://httpd.apache.org/) and [Apache Modules](http://httpd.apache.org/modules/)
- Microsoft® Internet Information Server (IIS): [microsoft.public.inetserver.* newsgroups](http://groups.google.com/groups?hl=en&lr=&ie=UTF-8&oe=UTF-8&group=microsoft.public.inetserver)

### Grading and Required Work

#### Participation in Design Reviews (30%)

A central activity in 6.171 is presentation of designs and critique of those designs. This happens mostly in class but also via written critiques. When you’re presenting, points are given for clear presentations of design decisions and open questions. When you’re in the audience or writing, points are given for constructive criticism.

#### Term Project (60%)

You and your partner(s) will share a grade for the quality of the work that you do during the semester in building an online learning community. Quality is defined as a combination of user experience, the maintainability of the system, and the helpfulness of the documentation.

#### Mid-term Exam (10%)

The mid-term is a one-week take-home exam, intended to require about 6 hours of work. Your ability to think about data model, user experience, and overall system engineering will be tested.

### Textbooks

See the [readings](https://ocw.mit.edu/courses/6-171-software-engineering-for-web-applications-fall-2003/pages/readings/) section for more information on the required textbooks.

### Adoption by Universities and Companies

This course is designed for easy adoption by other universities. We provide the following materials online for free:

- Textbooks
- Problem Sets (incorporated in main text)
- Lecture Notes
- Sample Exams (on request)

You may wish to provide a computing environment for your students. Students have been most successful using either Microsoft .NET (Windows® 2000 only; one machine per student) or AOLserver/Oracle (a single pizza box Unix® machine can support 10 students).

### Course History

This course was developed by Hal Abelson, the late Michael Dertouzos, and Philip Greenspun.

- Fall 2003: offered as MIT course 6.171
- Spring 2002: offered as MIT course 6.171
- Spring 1999: offered as MIT course 6.916: Software Engineering of Innovative Web Services (3-0-9)
- Summer 1999: offered as an intensive summer course at University of Hamburg and New York University, as a 5-week boot camp (three problem sets plus Unix® sysadmin and Oracle dbadmin), and as a 2-week boot camp (problem sets 1 and 2)
- Fall 1999: adopted by California Institute of Technology; offered again as MIT course 6.916
- Winter 2000: offered as an intensive 9-unit course during MIT’s IAP;
- Spring 2000: repeated as MIT course 6.916, offered to remote students at UC Berkeley (thanks to Doug Tygar) and Stanford University (thanks to Jeff Ullman)
- Spring/Summer 2000: offered as CS190 at UCLA, taught by Robert Dennis
- Summer 2000: adopted by University of Michigan, taught by Nandit Soparkar
- June-December 2000: adopted by UFM (Guatemala City, Guatemala), taught by Oscar Bonilla
- Spring 2001: offered at Carnegie-Mellon, University of New South Wales (Sydney, Australia; led by John Shepherd)
- May 2001: “Teaching Software Engineering” paper presented at the Web conference in Hong Kong, describing our experience with the course and the rationale behind the new curriculum and textbook
- Spring 2002: the revamped version offered at MIT as 6.171

Bottom line: about 1000 CS majors have gone through this curriculum and all but about 30 have become competent database-backed Web service developers. A more detailed history and explanation of this course is [available](http://philip.greenspun.com/teaching/teaching-software-engineering).

### Ongoing Glory

Here are some examples of good things have happened in or because of 6.916/6.171:

- From Spring 1999 The image sharing service at [photo.net](http://www.photo.net/gallery/) was developed in Spring 1999 by a student team. The system continues to run on the public Internet and permits nearly 300,000 to share and comment on uploaded photographs.
- From Fall 1999 Camfield Estates continues to serve the residents of a public housing project in inner-city Boston (see the [background](https://link.springer.com/chapter/10.1007%2F3-540-45636-8_9) on this project by Randal D. Pinkett, a Media Lab graduate student)
- From Fall 2000 MIT UPV is online and providing an international cultural exchange for hundreds of students at MIT and Valencia, as described in this [WIRED magazine article](http://www.wired.com/category/magazine/).

A reasonably complete list of old projects is [available](https://philip.greenspun.com/seia/writeup). In addition to continuing public sites, 6.916/6.171 has also produced a few startup companies as students who took the course together continued their collaboration in industry. (Of course, that was in the go-go years of the Internet; now most of the students graduate and take jobs at IBM, Microsoft, and Oracle.)
