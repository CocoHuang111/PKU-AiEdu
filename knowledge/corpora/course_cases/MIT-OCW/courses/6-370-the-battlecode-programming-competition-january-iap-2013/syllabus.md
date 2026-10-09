- Source: https://ocw.mit.edu/courses/6-370-the-battlecode-programming-competition-january-iap-2013/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Optional Lectures: 1 session / day, 1 hour / session for the first half of IAP ![image](https://ocw.mit.edu/images/educator/icon-question-iap.png)

Optional Lab Hours: 1 session / day, 1 hour / session for the first half of IAP

### What is Battlecode?

The Battlecode Programming Competition is a unique challenge that combines battle strategy, software engineering, and artificial intelligence. In short, the objective is to write the best player program for the computer game Battlecode.

Battlecode, developed for this course, is a real-time strategy game. Two teams of robots roam the screen managing resources and attacking each other with different kinds of weapons. However, in Battlecode each robot functions autonomously; under the hood it runs a Java virtual machine loaded up with its team’s player program. Robots in the game communicate by radio and must work together to accomplish their goals.

Teams are given the Battlecode software and a specification of the game rules in early January. Each team develops a player program, which will be run by each of their robots during Battlecode matches. Contestants often use artificial intelligence, pathfinding, distributed algorithms, and/or network communications to write their player. At the final tournament that takes place at the end of January, the autonomous players are pitted against each other in a dramatic head-to-head tournament in front of a live audience.

This course is a great opportunity to learn to program or hone your skills further. We provide lectures on relevant topics to the Battlecode competition. The optional lecture series is intended for beginners and mid-level competitors to learn how to get started writing a bot and to learn about some techniques employed by more advanced players. While we do not provide extensive resources on basic programming skills, we may be able to point you in the right direction as you supplement your learning with hands on experience in the competition.

### Course Requirements

To compete, individuals must sign up through the [Battlecode website](https://www.battlecode.org/), be on a team (even if it consists of only one person), and upload his/her resume. Non-MIT students are welcome to participate, but you must be a current MIT student to be eligible for prizes and competing in the final tournament.

Teams must have one to four people, but can be a mix of MIT and non-MIT students.

Experience in programming definitely helps in the competition, but everyone has to start somewhere. The supported programming languages are [Java](http://www.oracle.com/technetwork/java/index.html) and [Scala](http://www.scala-lang.org/).

### Grading

MIT students are able to receive six units of credit for this course if the following requirements are met:

- Defeat the reference bot in a set of matches. You must defeat Teh Devs (the team name for the developers of this year’s code base) in an unranked scrimmage on a certain set of maps. These maps will be announced approximately two weeks into the course. If your player beats the reference player, everyone on your team receives 6 credits.
- Submit a well-written strategy report if you do not defeat the reference bot. The two-page report on your player should cover its code design, how it works, an explanation of any AI paradigms you used, etc. You will receive credit if your source code and your report both show a significant amount of effort, thought, and good design techniques.

### Scrimmages

Any team can challenge another team to a scrimmage. A scrimmage is a friendly game between two teams. This allows a team to test their strategies against those of other teams. Teams may also challenge each other to ranked matches to improve their Battlecode scrimmage ranking.

### Tournaments

During the actual competition, top teams from the newbie tournament and final tournament are awarded cash prizes. Smaller prizes are also awarded to top teams in other tournaments. There are five tournaments: the sprint, seeding, qualifying, final, and newbie tournaments.

#### Sprint Tournament

The sprint tournament is a single-elimination tournament. One week after spec release, teams are given a chance to win small prizes in this tournament. The goal is to get an idea of the meta-game, and a chance to test bot prototypes. Contestants are seeded based on scrimmage ranking, and play continues until there is only one undefeated team.

#### Seeding Tournament

The seeding tournament is a double-elimination tournament that takes place one week after the sprint tournament. Contestants are seeded based on scrimmage ranking, and play continues until there is only one undefeated team. The results of this tournament are used to determine seeds for the qualifying and newbie tournaments. Teams are ranked by the following criteria, in order:

- Furthest round achieved.
- [Bayesian Elo rating](http://remi.coulom.free.fr/Bayesian-Elo/) for the tournament (computed on a per-game basis, not a per-match basis).

#### Qualifying Tournament

The qualifying tournament is a double-elimination tournament that takes place one week after the seeding tournament. This tournament determines the teams going into the final tournament, and showcases the final strategies of all the competitors. Final submissions must be in by this tournament. Play continues until there are eight teams remaining. These teams move on to the final tournament. Teams are seeded for the final tournament as follows:

- The four teams that did not lose a match receive the top four seeds.
- Teams that did not lose a single game are ranked by their qualifying seeds.
- The remaining teams are ranked by Bayesian Elo rating for the tournament (computed on a per-game basis).

#### Final Tournament

The final tournament is another double-elimination tournament. The final tournament starts with a blank slate (i.e., any losses in the qualifying tournament are erased). The top teams compete for glory and fame!

#### Newbie Tournament

The newbie tournament will run concurrently with the qualifying tournament. All teams consisting entirely of MIT students who have not participated in Battlecode before will automatically be entered into the newbie tournament in addition to the other tournaments.
