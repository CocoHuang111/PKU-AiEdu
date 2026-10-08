> 检索摘要：6.826 Principles of Computer Systems（Spring 2002，Graduate）的「Calendar」。页内标题：Calendar。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-826-principles-of-computer-systems-spring-2002/pages/calendar/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Calendar

This calendar provides the lecture topics, along with assignment due dates. Lectures given by Professors Lampson and Rinard are shown as “L” and “R,” respectively, in the Lecturer column. The Handouts column indicates materials distributed in class.

| LEC # | LECTURER | HANDOUTS # | TOPICS | PROBLEM SET # OUT | PROBLEM SET # DUE |
| --- | --- | --- | --- | --- | --- |
| 1 | L |  | Overview <br> . The Spec language, state machine semantics, examples of specifications and code | 1 |  |
|  |  | 1 <br> 2 <br> 3 <br> 4 <br> 5 | Course information <br> Background <br> Introduction to Spec <br> Spec reference manual <br> Examples of specs and code |  |  |
| 2 | L |  | Spec <br> and code for sequential programs. Correctness notions and proofs. Proof methods: abstraction functions and invariants |  |  |
|  |  | 6 | Abstraction functions |  |  |
| 3 | L |  | File systems 1 <br> : Disks, simple sequential file system, caching, logs for crash recovery | 2 | 1 |
|  |  | 7 | Disks and file systems |  |  |
| 4 | L |  | File systems 2 <br> : Copying file system |  |  |
| 5 | R |  | Proof methods <br> : History and prophecy variables; abstraction relations | 3 | 2 |
|  |  | 8 | History variables |  |  |
| 6 | R |  | Semantics and proofs <br> : Formal sequential semantics of Spec |  |  |
|  |  | 9 | Atomic semantics of Spec |  |  |
| 7 | L |  | Performance <br> : How to get it, how to analyze it | 4 | 3 |
|  |  | 10 | Performance |  |  |
|  |  | 11 | Paper: Michael Schroeder and Michael Burrows. “Performance of Firefly RPC,” <br> ACM Transactions on Computer Systems <br> 8 <br> , 1, February 1990, pp 1-17. |  |  |
| 8 | L |  | Naming <br> : Specs, variations, and examples of hierarchical naming | Form groups |  |
|  |  | 12 | Naming |  |  |
|  |  | 13 | Paper: David Gifford, et al. “Semantic file systems,” <br> Proc.13th ACM Symposium on Operating System Principles <br> , October 1991, pp 16-25. |  |  |
| 9 | R |  | Concurrency 1 <br> : Practical concurrency, easy and hard. Easy concurrency using locks and condition variables. Problems with it: scheduling, deadlock | 5 | 4 |
|  |  | 14 | Practical concurrency |  |  |
|  |  | 15 | Concurrent disks |  |  |
|  |  | 16 | Paper: Andrew Birrell, “An Introduction to Programming with Threads_,” Digital Systems Research Center Report 35_, January 1989. |  |  |
| 10 | R |  | Concurrency 2 <br> : Concurrency in Spec: threads and non-atomic semantics. Big atomic actions. Safety and liveness. Examples of concurrency |  |  |
|  |  | 17 | Formal concurrency |  |  |
| 11 | R |  | Concurrency 3 <br> : Proving correctness of concurrent programs: assertional proofs, model checking |  | 5 |
| 12 | R |  | Distributed consensus 1 <br> . Paxos algorithm for asynchronous consensus in the presence of faults |  |  |
| 13 | L |  | Distributed consensus 2 | Early proposals |  |
|  |  | 18 | Consensus |  |  |
| 14 | R |  | Sequential transactions <br> with caching |  |  |
|  |  | 19 | Sequential transactions |  |  |
| 15 | R |  | Concurrent transactions <br> : Specs for serializability. Ways to code the specs | Late proposals |  |
|  |  | 20 | Concurrent transactions |  |  |
| 16 | R |  | Distributed transactions <br> : Commit as a consensus problem. Two-phase commit. Optimizations | Late interim reports |  |
|  |  | 27 | Distributed transactions |  |  |
| 17 | R |  | Introduction to distributed systems <br> : Characteristics of distributed systems. Physical, data link, and network layers, design principles <br> Networks 1 <br> : Links. Point-to-point and broadcast networks |  |  |
|  |  | 21 | Distributed systems |  |  |
|  |  | 22 | Paper: Michael Schroeder, et al. “Autonet: A high-speed, self-configuring local area network,” <br> IEEE Journal on Selected Areas in Communications <br> 9 <br> , 8, Oct 1991, pp. 1318-1335. |  |  |
|  |  | 23 | Networks: Links and switches |  |  |
| 18 | L |  | Networks 2 <br> : Links cont’d: Ethernet. Token Rings. Switches. Coding switches. Routing. Learning topologies and establishing routes |  |  |
| 19 | L |  | Networks 3 <br> : Network objects and remote procedure call (RPC) | Early interim reports |  |
|  |  | 24 | Network objects |  |  |
|  |  | 25 | Paper: Andrew Birrell, et al. “Network objects,” <br> Proc.14th ACM Symposium on Operating Systems Principles <br> , Asheville, NC, December 1993. |  |  |
| 20 | L |  | Networks 4 <br> : Reliable messages. 3-way handshake and clock code. TCP as a form of reliable messages | Late interim <br> reports |  |
|  |  | 26 | Paper: Butler Lampson. “Reliable messages and connection establishment,” in S. Mullender, ed. <br> Distributed Systems <br> , Addison-Wesley, 1993, pp. 251-281. |  |  |
| 21 | L |  | Replication and availability <br> : Coding replicated state machines using consensus. Applications to replicated storage |  |  |
|  |  | 28 | Replication |  |  |
|  |  | 29 | Paper: Jim Gray and Andreas Reuter. “Fault tolerance,” in <br> Transaction Processing: Concepts and Techniques <br> , Morgan Kaufmann, 1993, pp. 93-156. |  |  |
| 22 | R |  | Caching <br> : Maintaining coherent memory. Broadcast (snoopy) and directory protocols Examples: multiprocessors, distributed shared memory, distributed file systems |  |  |
|  |  | 30 | Concurrent caching |  |  |
| 23 |  |  | Early project presentations |  |  |
| 24 |  |  | Early project presentations |  |  |
| 25 |  |  | Late project presentations |  |  |
| 26 |  |  | Late project presentations |  |  |
|  |  |  | Final reports due |  |  |
