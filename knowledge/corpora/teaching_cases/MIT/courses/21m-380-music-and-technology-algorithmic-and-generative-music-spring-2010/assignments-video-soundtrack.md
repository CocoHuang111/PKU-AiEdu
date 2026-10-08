> 检索摘要：21M.380 Music and Technology: Algorithmic and Generative Music（Spring 2010，Undergraduate）的「Assignments and Projects Project Sample: Video Soundtrack Generation with PD」。页内标题：Assignments and Projects Project Sample: Video Soundtrack Generation with PD。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/21m-380-music-and-technology-algorithmic-and-generative-music-spring-2010/pages/assignments-and-projects/video-soundtrack/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments and Projects Project Sample: Video Soundtrack Generation with PD

*Courtesy of MIT student, used with permission.*

My sonic system was an attempt at soundtrack generation to a given piece of film. For my video test material, I used an old 1950s PSA about surviving a nuclear attack. The footage is part of the [Prelinger Archive](http://www.archive.org/details/prelinger). It is in black and white deliberately to limit the amount of visual information I have to deal with and to make the project simpler.

I used PD as my platform for producing sound. I also used tools from GEM to both play the footage and to draw color values from frames of the video. To start, I used a 3x3 grid of pixel “sensors” to pick up color information from the frames of the video. While the GEM object “pix_data” can also produce RGB values, I only needed the greyscale values. This gave me 9 streams of values ranging between 0-1 where 1 = white and 0 = black to use in sound generation.

The most difficult part of the process was the mappings from data to sound. I recognized that frames that were lighter in contrast had higher tension in the narrative of the film so I decided to make them softer than the other frames. I used each vertical section of data sensors to control three polyphonic granular synthesizers to generate the low base of the sound. They are fed various sound files: two explosions and one sample of bass. Then each data sensor controlled an oscillator and a noise generator. I tried to manipulate the data more by generating more information: how the current data value compares to a local average, how it compares to a local minimum and maximum, how it compares to values of closely adjacent frames. These other data streams controlled values such as the pitch of the oscillator (within a specified band), band pass values for the pink noise generator, volume of the noise, and LFO on the oscillator.

Additionally I tried to build in some “recognition” into the system. I noticed that the bombs in the film were always in the center of the frame and almost white when exploding. I calibrated a counter to trigger the sound of an explosion when a bomb was shown on the screen but not at another time.

The project is a medium success. The sound produced is mostly without large-scale contour or interest. Admittedly, most of the time was spent on making sound on a micro-scale— the amount of LFO, the frequency range, the band pass values—and not as much on overall contours (except for basic considerations such as overall contrast values controlling the master volume). There could have been more effort but into trigger-based sounds instead of continuous sounds whose control values were constantly being changed. This would introduce both more space and interest into the sound. Also using more pre-composed segments that could be triggered would be useful. There may have also been too many “sound units” going on—when listening to one voice, the oscillations and sound over time are sort of interesting but this type of concentration is lost when hearing all 9 voices together with the granular synthesizers.

I also think the project would have sounded better if the three channels were separated out in space, in an installation set-up instead through headphones or speakers. This would help to “spatialize” all of the sounds being made and allow the listener to focus more closely on individual movements in each of the channels. I hope to keep working with this patch in order to produce something that sounds much better and improve my skills in PD.

Project Sample: Video soundtrack generation with PD 1.

Project Sample: Video soundtrack generation with PD 2.

Project Sample: Video soundtrack generation with PD 3.

Source video: 1951 US Civil Defense film [Survival Under Atomic Attack](http://www.archive.org/details/Survival1951)

Code and input audio samples ([ZIP](https://ocw.mit.edu/courses/21m-380-music-and-technology-algorithmic-and-generative-music-spring-2010/resources/assn_ss_a_files/)) (This ZIP file contains 1 .pd and 3 .wav files)
