> 检索摘要：6.189 A Gentle Introduction to Programming Using Python（January IAP 2008，Undergraduate）的「Projects」。页内标题：Projects；Project 1 – Hangman；Project 2 – Guitar Hero Clone；Sample Program 1 – Tic-Tac-Toe；Sample Program 2 – Connect Four。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### Project 1 – Hangman

Project 1 ([PDF](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/project1/)) was the game of Hangman. The handout guides you through the process. This process is called *incremental programming*. It allows you to tackle complex problems, like writing a game of Hangman, by tackling small sub-tasks first. In this case, we can tackle the problems of figuring out whether the user has guessed the word, or creating a string of the word with the letters guessed so far. With the sub-tasks taken care of, it’s easier to take on the bigger task.

Optional project files: word list ([TXT](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/word_list/)) contains many words; hangman_lib.py ([PY](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/hangman_lib/)) contains helper functions to get a random word and to print a Hangman image; hangman.py ([PY](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/hangman/)) contains example usage of hangman_lib.

Example solution: hangman_soln.py ([PY](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/hangman_soln/)) (needs to be in same directory as above files)

### Project 2 – Guitar Hero Clone

Project 2 was a clone of the game of Guitar Hero. This is a decently complex game, and trying to do it all at once is not practical. Instead, we learn the importance of *modularity* and *teamwork* by breaking up the functional parts of the game (input, graphics, sound and logic) and completing these parts in teams. This approach even allowed us to have a working, playable prototype at the end of class, despite being incomplete.

Note: this project could not be included in MIT OpenCourseWare due to copyright restrictions.

### Sample Program 1 – Tic-Tac-Toe

Many of you asked for us to write a tic-tac-toe program as one of our sample programs. In the beginning of class 6, Mihir wrote such a program in front of you all. The goal of that program was to be simple and straightforward, and it was successful.

I’ve written another version, with a different goal: to be polished. My implementation is considerably different, and that’s fine; we all have different styles of programming. Take a look. It’s extensively commented, but feel free to email with questions.

File: tictactoe.py ([PY](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/tictactoe/))

### Sample Program 2 – Connect Four

Here’s another sample program with the goal of being polished. This is a great example where the implementation is not trivial (unlike in Tic-Tac-Toe), so abstraction is vital to prevent bugs and to keep the code readable.

There are some Python things in the code that you may not know yet. The assert statement just throws an error if the following condition isn’t True. Writing a string with the % symbol lets you plug in the variables that follow into that spot in the string (%s means string, %i means integer and %c means one letter).

So take a look. It’s not quite so extensively commented as the Tic-Tac-Toe program, so feel free to email me with questions.

File: connectfour.py ([PY](https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2008/resources/connectfour/))
