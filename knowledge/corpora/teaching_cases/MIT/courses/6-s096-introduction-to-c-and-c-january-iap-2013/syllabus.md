> 检索摘要：6.S096 Introduction to C and C++（January IAP 2013，Undergraduate）的「Syllabus and Software」。页内标题：Syllabus and Software；Course Meeting Times；Course Description；Software；Standard Environment；IDEs。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus and Software

### Course Meeting Times

Lectures: 2 sessions / week for 4 weeks, 1 hour / session

Labs: 2 sessions / week for 4 weeks, 1 hour / session

### Course Description

This course provides a fast-paced introduction to the C and C++ programming languages. You will learn the required background knowledge, including memory management, pointers, preprocessor macros, object-oriented programming, and how to find bugs when you inevitably use any of those incorrectly. There will be daily assignments and a small-scale individual project.

### Software

#### Standard Environment

It’s most efficient for the staff if everyone uses the same environment:

- Athena command-line
- Compiling: gcc, g++
- Debugging: gdb, valgrind
- Editing: nano, pico, vim, or emacs

You can mimic that environment on your own computer:

- **Windows:** All the necessary packages (except valgrind) are available in [cygwin](http://www.cygwin.com/) (gcc-core, gcc-g++, gdb).
- **OS X:** [Install Xcode from the App Store](https://itunes.apple.com/us/app/xcode/id497799835), open it, go to Preferences > Downloads > Components and download “Command Line Tools”.
- **Linux:** `sudo apt-get install build-essential` or equivalent.

#### IDEs

If you’d like to use a GUI instead (and there are many good reasons to do so), we’ll try to help you out, but:

- Your programs still need to work in the standard environment, so you should test them there.
- One of our primary debugging tools (valgrind) may not be available in your IDE.

Nevertheless, these IDEs seem to work well:

- [Code::Blocks](http://www.codeblocks.org/) (Windows, Linux, OS X)
- [Eclipse](http://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/junosr1) (Windows, Linux, OS X)
- Visual Studio (Windows)
- [Xcode](https://itunes.apple.com/us/app/xcode/id497799835) (OS X)
