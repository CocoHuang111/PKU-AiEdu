> 检索摘要：6.370 Robocraft Programming Competition（January IAP 2005，Undergraduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Requirements for Credits & Engineering Design Points (EDPs)；Tournament Attendance；Contest Rules；Getting Help。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-370-robocraft-programming-competition-january-iap-2005/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

No regular class schedule. Students meet in teams.

### Requirements for Credits & Engineering Design Points (EDPs)

6 General Credits

To receive 6 units of general elective credit, your must successfully submit a Robocraft player of “substantial effort”. The 6.370 chairmen will make judgement calls on what constitutes “substantial”, but basically your player must do something other than sit at its starting location. It does not have to beat the reference player for 6 general credits, although if you do qualify for 6 EDPs (see next section), then you automatically qualify for 6 general credits.

6 EDPs

To receive 6 EDPs, your Robocraft player must defeat the reference player by capturing its flag and uniting it with your own. Your team submission will play against the reference player included with the Robocraft software release, on “seeding.map”. Specifically, to test whether team XXX receives 6 EDPs, we will run:

$ run-robocraft -Drobocraft.teamA=teamXXX.RobotPlayer \
-Drobocraft.teamB=refplayer.RobotPlayer \
-Drobocraft.map=seeding.map \
-Drobocraft.silenceA=true \
-Drobocraft.silenceB=true

If the output of the game engine indicates, “TeamA controls both flags!” (a message that gets printed once a single one of your robots is carrying both team flags), then your team will receive 6 EDPs. The deadline for submitting a player for EDPs is 2 days after the last session at 11:59 pm. Teams may be disqualified from the 6 EDPs if they are found to hard-code map locations of seeding.map to take advantage of this particular map’s terrain features.

### Tournament Attendance

Attendance to the final tournament is mandatory for all students. In addition, if your team qualifies as a “finalist” (i.e. you do well in the preliminary tournament), all team members are required to attend both the Finalists’ Celebration at the Hyatt Grand Ballroom and the final tournament. If any team member does not attend either one of these events, your team will be immediately disqualified and the finalist spot will be awarded to another team.

### Contest Rules

6.370 is open to all currently registered MIT, Harvard and Wellesley students, undergraduate or graduate, excepting 6.370 organizers and contributors to the 6.370 code base.

Entrants may compete individually or form teams of up to 3 students. Registered teams must be mutually exclusive.

Students registered through WebSIS can expect to receive 6 general elective credits if their team produces a working player. Note that attendance at the final tournament is required to receive credit. Harvard and Wellesley students may cross-register for course credit.

Students are eligible for 6 Engineering Design Points if their team produces a player that can beat the “reference player” provided during IAP. EDPs are awarded regardless of performance in the 6.370 tournament.

Past 6.370 entrants may compete with no penalties and are again eligible for 6 credits and 6 EDPs.

Students who wish to compete as finalists in the final tournament must be available for the Finalists Celebration with sponsor company representatives.

All code a team submits must be the original work of members on that team. All submitted code becomes the property of the 6.370 competition.

### Getting Help

6.370 is technically a class, but we are not here to teach you how to program in Java®. Please don’t ask us about Java® programming in general. You are on your own for that. We assume you have a basic knowledge of Java®, or a willingness to learn it, and will consult the appropriate reference materials.

Please keep in mind that 6.370 is completely student run, and we have limited resources with which to address your questions.
