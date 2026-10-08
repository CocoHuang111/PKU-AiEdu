> 检索摘要：2.12 Introduction to Robotics（Fall 2005，Undergraduate）的「Projects」。页内标题：Projects；First Project: De-Mining Robot；Second Project: Rescue Robot。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

Lab sessions are devoted to two projects. The first project, spanning Labs 1 through 4, is to build a de-mining robot. The second project, covering Labs 5 through 10, is to build a robot that finds and rescues disaster victims.

### First Project: De-Mining Robot

The goal of this project to produce a robot capable of searching for hidden metal disks (“mines”) in a open space. Students design and implement a search algorithm that lets the robot hunt autonomously, and when a mine is found to pause on top of it.

| LABS | TOPICS | SUPPORTING FILES |
| --- | --- | --- |
| Lab 1 ( <br> [PDF](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/resources/lab1/) <br> ) | Embedded Robot Controller, I/O Interface, and PWM Amplifiers | Lab Report Form ( <br> [PDF](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/resources/lab1_response/) <br> ) |
| Lab 2 ( <br> [PDF](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/resources/lab2/) <br> ) | Controller Software and Sensor Inputs |  |
| Lab 3 ( <br> [PDF](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/resources/lab3/) <br> ) | Implement Basic Sensor-Based Controls; Plan Strategy for De-mining Task |  |
| Lab 4 | Refine and Test De-mining Operations |  |

*From the Fall 2004 Class - Videos of Final Demonstrations*

These short video clips of the De-mining Robot demonstrations illustrate variations in search patterns and in the ability to accurately detect a mine that’s within range of the search.

The robot has a set of “whiskers” at its corners to detect walls and obstructions. The mine sensor itself has a fairly small radius of detection, about 2 inches, so the sensor must pass nearly over the top of the mine for it to be detected.

The robot has a failsafe control link that causes the robot to shut down if it loses contact with the student controller. While this was supposed to be a wireless connection, mysterious interference during the demonstration led most students to fall back on a wired control link.

- Robot loses RF control link and stops ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_037-220k.mp4))
- Robot gets stuck in a control loop ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_038-220k.mp4))
- Working RF control link; robot finds a mine ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_039-220k.mp4))
- Robot searches without success ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_040-220k.mp4))
- Robot finds a mine ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_041-220k.mp4))
- Robot finds two mines ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_042-220k.mp4))
- Students try to keep the robot’s RF link alive ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_043-220k.mp4))
- Robot with a novel search pattern ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_044-220k.mp4))
- Robot misses a mine, then finds one ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_045-220k.mp4))
- Robot searches without success ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_046-220k.mp4))
- One of the “better functioning” designs, in terms of speed and search technique ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_047-220k.mp4))
- Robot searches in a spiral out from center ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_048-220k.mp4))
- Robot finds a mine; very quick reverse after pause ([MP4](http://www.archive.org/download/MIT2.12F04/2.12_049-220k.mp4))

### Second Project: Rescue Robot

This past year will be remembered for its many severe natural disasters, both overseas and here in the United States. One of the most compelling applications for robotics technology is to develop rescue robots that might be able to save lives after such catastrophic events. Students will be given the challenge of developing autonomous mobile robots that can perform navigation and manipulation for a disaster response rescue mission. Each robot has a manipulator arm mounted on a moving platform guided by an on-board Linux computer and various sensors, including a laser range scanner for detecting obstacles and “houses” where victims (dolls) may be located. Once located, the robot should retrieve the victim and take it a hospital treatment center.

Description of the Rescue Robot Project ([PDF](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/resources/final_project/))

[Video of Final Demonstrations (MOV - 13.3 MB)](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/resources/rescue_robot_mov/) (Courtesy of Phil Shaltis. Used with permission.)
