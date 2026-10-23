- Source: https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

| SES # | ASSIGNMENTS | SUPPORTING FILES |
| --- | --- | --- |
| 1 | Introduction to C | hello_world.c ( <br> [C](https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/resources/hello_world/) <br> ) |
| 2 | Introduction to C memory management | ( <br> [ZIP](https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/resources/assn02/) <br> ) (This ZIP file contains: 2 .c files and 1 .h file.) |
| 3 | More C memory management | ( <br> [ZIP](https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/resources/assn03/) <br> ) (This ZIP file contains: 1 .c files and 1 .h file.) |
| 4 | Introduction to C++ | ( <br> [ZIP](https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/resources/assn04/) <br> ) (This ZIP file contains: 1 .cc files and 1 .h file.) |
| 5 | Inheritance and polymorphism | ( <br> [ZIP](https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/resources/assn05/) <br> ) (This ZIP file contains: 1 .cc files and 1 .h file.) |

### Assignment 1: Introduction to C

1. Obtain GCC, either from installing (gcc.gnu.org) or from running it on MIT servers.
2. Figure out how to run GDB (gdb) and Valgrind (valgrind).
3. Compile and run the “hello world” program.
4. Extend the “hello world” program to print the current time. **Hint:** look at C’s ctime (time.h) library.
5. Submit your modified hello_world.c program along with a README that describes 1) the command(s) you used to compile your program and 2) the command(s) you used to run your program. Please put the files into a single compressed .zip or .tar.gz file.

### Assignment 2: Introduction to C Memory Management

1. Write insert, find_val, and delete_bst in code we have included.
2. Write tests and make sure your code works.
3. Use valgrind to see if your code leaks memory.
4. Submit all of your files in a compressed .zip or .tar.gz file along with a README describing 1) the command(s) you used to compile your program and 2) the command(s) you used to test your program. If you choose to include tests, you should also describe them. If you used a Makefile, please include that as well.

### Assignment 3: More C Memory Management

1. Re-implement the binary search tree code using an array instead of a node_t struct, using the given .h file.
2. Compare the two implementations. Which is faster? When would you prefer one implementation over the other, and why?
3. Include a README that includes your files, how to run/compile them, and your response to the above question.

### Assignment 4: Introduction to C++

In this assignment, you will re-implement the binary search tree using C++ classes.

1. Download and study the given header file “BST.h”. This defines the interface to the binary search tree class, and includes the functionality that you need to provide to the client of the tree.
2. Implement the methods “insert”, “find”, and “print_inorder”. You can define as many extra classes/fields/methods as you need, but DO NOT modify the declarations for the existing methods (i.e. these three methods, along with the constructor & destructor). You may also reuse code from the previous assignments. Think about access control issues — what should be exposed to or hidden from the client?
3. Write test cases to show that your methods work correctly. You may extend the given test file, test_BST.cc.
4. Answer the following questions, and put your responses in a text file called “answers.txt”: > 4.1. Compare the implementation of the BST in this assignment to those from the previous ones (i.e. struct & array-based implementations). What are some of the differences? How do they affect the client of the BST? > > 4.2. What is the representation invariant for the BST? How would you modify your code to ensure that the invariant holds? > > 4.3. There are an infinite number of BSTs in this universe (theoretically), so it is impossible to test that your code works for all BSTs. What approach did you take to make sure it’s correct? Are your test cases sufficient, and how do you know?
5. Submit all of your files (*.h, *.cc, answers.txt) in a compressed .zip or .tar.gz file, along with a README describing (1) the command(s) you used to compile your program and (2) the command(s) you used to test your program. If you choose to include tests, you should also describe them. If you used a Makefile, please include that as well.

### Assignment 5: Inheritance and Polymorphism

In this assignment, you will use concepts of inheritance and polymorphism in C++ to implement simple arithmetic expression trees.

1. Download and study the given header file “Expression.h”. This defines an abstract base class that represents the interface to all expression trees. In this assignment, you will be defining subclasses that implement this interface. At minimum, these subclasses should provide definition for “eval” and “print” functions (unless they are abstract classes themselves).
2. Design a type hierarchy, with “Expression” at the top, that represents a set of simple arithmetic expressions. The operations in this set include binary operations such as addition, subtraction, multiplication, and division over real numbers (which you may represent using floats in C++), as well as the negation operation. For example, you should be able to represent an expression such as “(3.0 + 4) * -(5.0)”. **Hints:** Think about the following: What are the common characteristics or behaviors among different expressions? What are the differences? Which functions/fields should be inherited, and which should be implemented separately?
3. Implement the methods “eval” and “print”. The “eval” method evaluates the expression and returns the resulting float. For example, the expression “(3.0 + 4) * -(5.0)” should return -35.0. The “print” method should print the raw (i.e. unevaluated) expression in the infix notation.
4. Write test cases to show that your methods work correctly. Include your test cases in “test_expression.cc”.
5. Answer the following questions, and put your responses in a text file called “answers.txt”: > 5.1. Let us suppose that we want to add an extra operation “exponentiation” that takes a base expression and an exponent. How would you modify/extend your type hierarchy to do this? > > 5.2. This time, we want to add an operation “sum” that takes an arbitrary list of reals and add them together. How would modify/extend your type hierarchy? Why? > > 5.3. Does your design allow invalid or undefined mathematical expressions? Why or why not?
6. Submit all of your files (*.h, *.cc, answers.txt) in a compressed .zip or .tar.gz file, along with a README describing (1) the command(s) you used to compile your program and (2) the command(s) you used to test your program. If you choose to include tests, you should also describe them. If you used a Makefile, please include that as well.
