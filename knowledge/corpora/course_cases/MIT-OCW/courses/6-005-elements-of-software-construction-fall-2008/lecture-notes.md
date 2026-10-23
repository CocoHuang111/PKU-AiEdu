- Source: https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/pages/lecture-notes/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Lecture Notes

### Review Handouts

State machine syntax and semantics ([PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec_state_machine/))

Graphical object model notation ([PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec_object_model/))

### Topics by Session

Notes for lecture 21 are not available.

#### Abbreviations

JSP = Jackson Structured Programming

DPLL = Davis-Putnam-Logemann-Loveland (algorithm)

SQL = Structured Query Language

| SES # | TOPICS | LECTURE NOTES |
| --- | --- | --- |
| 1 | Introduction <br> Basic Java syntax and semantics; overview of objectives and structure of the course | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec01/) <br> ) |
| 2 | Classes <br> More Java: exceptions, input/output, classes, access control, static | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec02/) <br> ) |
| 3 | Subclassing and interfaces <br> Subclassing, inheritance, overriding, interfaces, packages; distinction between declared type and actual type; downcasting; anonymous classes | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec03/) <br> ) |
| 4 | Designing state machines <br> State machine design; graphical and textual notation; state machine semantics; parallel combinations of machines | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec04/) <br> ) |
| 5 | Implementing state machines <br> State machine implementation patterns; concurrency and queues; modularity and interfaces | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec05/) <br> ) |
| 6 | State machine invariants <br> Safety and liveness properties; state properties and invariants; inductive reasoning; computing the product machine of a parallel combination; state explosion; fault tolerance; interlocks and the idea of a trusted base | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec06/) <br> ) |
| 7 | Designing stream processors <br> Stream processing programs; grammars vs. machines; JSP method of program derivation; regular grammars and expressions | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec07/) <br> ) |
| 8 | Decoupling and interfaces <br> Modularity, decoupling, information hiding; module dependence diagrams; using interfaces for decoupling | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec08/) <br> ) |
| 9 | Testing and coverage <br> Why software testing is hard; input space partitioning, boundary testing, state machine coverage, code coverage; test-first development and regression testing | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec09/) <br> ) |
| 10 | Designing a SAT solver, part 1 <br> The SAT problem and SAT solvers; a new paradigm of functions over immutable types; use datatype productions to model structured values; patterns for implementing datatypes (Variant as Class, Interpreter) | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec10/) <br> ) |
| 11 | Designing a SAT solver, part 2 <br> Review of basic datatype patterns; a naive solver with backtracking search; design improvements with Facade, Option types, and a 3-valued logic | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec11/) <br> ) |
| 12 | Debugging <br> Techniques for avoiding debugging: assertions, modular development with unit testing, code reviews; strategies for debugging: reducing test cases, hypothesis-driven debugging, binary search; Heisenbugs | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec12/) <br> ) |
| 13 | Designing a SAT solver, part 3 <br> Abstract data types; representation independence; characterizing types by operations; encapsulation; examples of types used by DPLL solver; Factory Method pattern | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec13/) <br> ) |
| 14 | Rep invariants, equality, visitors <br> Advice on implementing types; rep invariants and abstraction functions; equality for immutable types; Iterator and Visitor patterns | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec14/) <br> ) |
| 15 | Little languages <br> Representing behavior using data structures; language datatypes, visitors, functional objects, higher-order functions; solving a problem by creating a domain-specific language | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec15/) <br> ) |
| 16 | Basics of mutable types <br> Heap semantics (aliasing, assignment, field setting); reachability and conceptual storage leaks; the Object Contract and equality properties; hash maps and their representation invariant; problems caused by mutation of keys | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec16/) <br> ) |
| 17 | Event-based programming <br> Fundamentals of programming graphical user interfaces; view hierarchy, Composite pattern, Publish-Subscribe pattern, Model-View-Controller (MVC); pitfalls of event-based programming | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec17/) <br> ) |
| 18 | Designing a photo organizer <br> The relational paradigm; conceptual modeling; object model syntax and semantics; Mitchell and Webb on “unity of purpose” | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec18/) <br> ) |
| 19 | Implementing a photo organizer <br> Implementation as object model transformation; key issue of where state resides; standard patterns; navigation, immutability and encapsulation; MVC considerations | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec19/) <br> ) |
| 20 | Concurrency <br> Shared-memory and message-passing paradigms; race conditions and deadlock; using threads and blocking queues in Java; concurrency issues in graphical user interfaces | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec20/) <br> ) |
| 21 | Usability <br> User interface design principles: learnability, visibility, efficiency, errors, simplicity; iterative design; sketching and paper prototyping; user testing |  |
| 22 | Relational databases <br> Using a database to represent an object model; relational algebra and SQL; transactions | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec22/) <br> ) |
| 23 | Conclusion <br> Final words; courses and internships that might follow 6.005; winners of Project 3 awards; 6.005 quiz game | ( <br> [PDF](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/resources/mit6_005f08_lec23/) <br> ) |
