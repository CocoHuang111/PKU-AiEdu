> 检索摘要：21M.380 Music and Technology: Algorithmic and Generative Music（Spring 2010，Undergraduate）的「Assignments and Projects Design Report 3 sample」。页内标题：Assignments and Projects Design Report 3 sample；Cat sounds source, PD generated。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/21m-380-music-and-technology-algorithmic-and-generative-music-spring-2010/pages/assignments-and-projects/design-report-3/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments and Projects Design Report 3 sample

### Cat sounds source, PD generated

*Courtesy of MIT student, used with permission.*

This assignment was generated completely in PD. I based the patch on one I used to play sounds at an event in early April. That piece was a series of cat purrs and I used the same source material for this piece (purrs, meows, and field sound). Most of the material sampled I found online in free sound databases (notably freesound.org) but I also spent a significant amount of time capturing sounds from my own cat, Eegloo. None of those sounds are used except for the “bird” sound that contains some birds outside my window that start talking at about 4:00 a.m.

The piece mainly uses array-controlled multiple granular synthesizers to cut up material. Both the phasor and pitch shift aspects are controlled by arrays. Each one moves at a different speed to create some interesting aspects when the values are at a maximum together, for example. A base of purrs is used to give some bottom to the sound where the granular synthesis is the top. The purrs have a low-pass filter on them to isolate them. The piece sounds the best on headphones or on a floor populated with transducers. Two different purrs begin (one in each channel) and then a faster, more frantic purr provides a setting for the other sounds. The granulated sounds are allowed to mingle for the main section of the piece before being removed and only the bird sound and a purr is left. The bird sound is then slowed to almost its recorded speed and pitch before exiting and allowing the purrs to finish the piece. The PD file does contain some objects to allow me to “punch” in meow sounds via MIDI input but I decided not to use them.

I am pleased with the sounds in the piece, though they do move slowly. More sculpting of the granular synthesis parameters could always strengthen their use, including developing more precise graphs in athenaCL to use in PD. I also think using a variable metro rate would be interesting too (using the reading of one graph to control the reading speed of another graph). Maybe another granular synthesizer would add more texture and could be used in the middle of the piece to have something super dense that is just a knot of sound and then it untangles back to discernible noises.

Design Report 3 sample: Cat sounds source, PD generated

Code file ([PD](https://ocw.mit.edu/courses/21m-380-music-and-technology-algorithmic-and-generative-music-spring-2010/resources/assn3_a/))
