> 检索摘要：6.S096 Introduction to C and C++（January IAP 2013，Undergraduate）的「Final Project Starter Kit」。页内标题：Final Project Starter Kit；Source Code；Compiling；Running；Understand It；What Next?；Plot a Graph；Draw Shapes；Draw Text；Invert an Image；Game of Life。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/pages/final-project/starter-kit/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Final Project Starter Kit

Starting a C or C++ project from scratch can be a daunting task. If you’re having trouble picking a software library, installing it on your system, and testing that it works, maybe you should try this Starter Kit!

This Starter Kit uses the [libpng](http://www.libpng.org/pub/png/libpng.html) library to render a series of random lines as a PNG image. The images look like this:

![Vertical red lines of different heights.](https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/16c065ed11ff220360ba6190d4a8bc4d_Line.jpg)

The example code was written by skimming the section of the [libpng manual (PDF)](http://www.libpng.org/pub/png/libpng-1.4.0-manual.pdf) on how to write PNG files. That manual also has a section on *reading* PNG files that you might find useful.

Use this kit to bootstrap your project and your imagination! The deadline looms, but there’s still plenty of time to have fun making silly little PNG files!

#### Source Code

[lines (C)](https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/resources/lines/)

#### Compiling

`$ gcc -Wall -std=c99 lines.c -lpng -o lines`

The `-lpng` flag is short for `-l png`, which links the `png` library with your project to create the program.

#### Running

`$ ./lines`

`./lines` creates a file called `out.png` in the current directory with some crazy graphics inside.

To view your image, you can use the `scp` command to copy it to your computer.

### Understand It

In the spirit of lab exercises, here are a few tasks to direct your focus to the parts of the program that matter:

1. Make the program take the filename as a command-line argument instead of hard-coding “`out.png`”.
2. Tweak the values that are assigned to `r`, `g`, `b`, and `a` in the loop labeled “`draw a bunch of vertical lines`”. The values range from 0 to 255. You should do this if you don’t understand how pixels work. [Wikipedia has a nice section on pixel colors](http://en.wikipedia.org/wiki/RGB).
3. Memory is allocated for storing the image data, but it’s never freed. You should free it. You’ll definitely need to do this if you use this code as a base for your project!
4. Tweak the program to draw horizontal lines instead of vertical ones.

### What Next?

Here are some concrete project ideas that you can implement and submit, roughly in order of increasing difficulty.

Whatever you do, **start (very) small** and add features as time allows. The secret to success here is to be unambitious at first.

#### Plot a Graph

Instead of drawing lines of random height, allow users to plot a bar graph by providing numbers as program arguments or using `stdin`.

#### Draw Shapes

Draw shapes of various colors. Start with squares, then move on to lines and circles if you have more time or people.

Optionally, convert the program to C++ and create a `Shape` parent class with sub-classes for each type of shape.

#### Draw Text

Read text from `stdin` and draw it on the image by changing pixel colors in the patterns of (very simple) letters. Here’s an example of how you might render ‘hi’:

![image](https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/62024122c82cd8dddade4ceb1b4e1f83_Draw_Text.jpg)

Instead of hard-coding how to draw each letter shape, I recommend storing them as strings or in a separate file, but this is not necessary.

#### Invert an Image

Read a PNG image (with libpng), flip it upside-down, and save it as a new image.

#### Game of Life

Implement the [Game of Life](http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) and render each time step as a separate PNG file.
