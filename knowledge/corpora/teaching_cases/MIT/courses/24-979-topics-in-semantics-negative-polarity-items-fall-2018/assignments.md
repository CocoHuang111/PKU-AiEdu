> 检索摘要：24.979 Topics in Semantics: Negative Polarity Items（Fall 2018，Graduate）的「Sample Assignment」。页内标题：Sample Assignment；Environments；Maximality, cardinality；DP-internal construal；No maximality；Definite descriptions and operators。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/24-979-topics-in-semantics-negative-polarity-items-fall-2018/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Sample Assignment

Note: All homework assignments given in *24.979 Topics in Semantics: Negative Polarity Items* were optional.

### Environments

(i) Provide the LFs for the sentences in (1). State for each of the constituents in them that dominate *student* and *smiled* whether they are ER (SER), EP (SEP), both, or neither with respect to them.

(1) a. Few people think that no student didn’t smile.
b. Both students who did not smile arrived.
c. Almost no student smiled.

(ii) Consider finally the LFs in (2). Is *a boy* dominated by a constituent that is SER with respect to it in these structures? (Please provide arguments for your answers.)

(2) a. [neg [[a boy] [λx_<sub>(et)t</sub>_ [[exactly 2 books] [λz*e* [x read z]]]]]]
b. [neg [[a boy] [λx_<sub>e</sub>_ [[exactly 2 books] [λz*e* [x read z]]]]]]
c. [[a boy] [λx*e* [neg [[exactly 2 books] [λz*e* [x read z]]]]]]

(iii) Assume that connected exceptive *but John* has the meaning in (3) (cf. von Fintel 1993, Sect. 1.8).

(3) [[but John]](P)(D)(Q) = 1 iff D(P\{John})(Q) ∧ ∀C(D(P\C)(Q) → {John}⊆C)

Provide the LF of the sentence in (4). Compute the meaning of each constituent dominating *student* and *smiled*, and state whether they are ER (SER), EP (SEP), both, or neither with respect to them.

(4) No student but John smiled.

(iv) What is predicted on this analysis of connected exceptives for the acceptability of *any* in (5)?

(5) No student but John read any book.

### Maximality, cardinality

Recall our class discussion of the examples in (6).

(6) a. Fewer than 10 students read War and Peace.
b. Fewer than 10 students surrounded the fort

(i) Adopting the same assumptions we relied on in class otherwise, what happens if we replace Buccola & Spector’s lexical entry for *many* with the one in (7)?

(7) [[many]] = λd. λx. card(x) ≥ d

(ii) What happens if we replace Buccola & Spector’s notion of maximal informativity with the perhaps more standard one in (8) (cf. Fox & Hackl 2006)?

(8) max<sub>*i*</sub>(w)(D)(d) = 1 iff D(w)(d) ∧ ∀d’(D(w)(d’) → (λw.D(w)(d) ⇒ λw.D(w)(d’)))

(Provide the computations of the truth-conditions in support of your answers, and consider in particular what is predicted about the acceptability of any in such sentences.)

### DP-internal construal

Is it possible to interpret *fewer than 10* in the above sentences within the DP? (Consult Heim & Kratzer, Ch. 8, for discussion of the DP-internal interpretations of quantifiers.) If this is the case, do we find a constituent that is SER with respect to *any book* on such a representation?

(9) Fewer than 10 students who read any book surrounded the castle.

### No maximality

The notion of maximality played a crucial role in Buccola & Spector’s accounting for the distribution of *any* with modified numeral quantifiers. However, we can choose different ingredients (theories) in our decomposition. Let us adopt (10) and (11), that is, assume that we decompose *fewer than 10* into comparative *er than 10* and antonymizer *little* (cf. Heim 2006); we keep ∃, *many* as defined in class.

(10) [[little]](d)(D) = 1 iff ¬D(d)

(11) v1. [[er than 10]](D) = 1 iff {10} ⊂ D
v2. [[er than 10]](D) = 1 iff {10, … ∞} ⊂ D

(i) Provide the LFs (incl. DP-internal construals) of the sentences in (12). (In these, the *er than* *10* -phrase should start out as a complement of *little*, and the *little*-phrase should start out as a sister of *many*. See slides #1, p. 13 / Filipe’s question for inspiration.)

(12) a. Fewer than 10 students read War and Peace.
b. Fewer than 10 students surrounded the fort.

(ii) Do the interpretations that we get for these LFs correspond to our intuitions? Do these LFs and their interpretations allow us to capture the distribution of *any* in such sentences? If not, what could be seen as the source of the problem?

### Definite descriptions and operators

Recall the operators-based formulation of the Condition, repeated here:

(13) a. A DP headed by *any* is acceptable only if it is c-commanded by an expression that denotes an SER function.
b. A function f of type (*στ)* is SER iff for all x, y of conjoinable type σ: if x⇒sy, then f(y)⇒sf(x).

(i) What does the Condition predict about the acceptability of the sentences in (14) and (15)?

(ii) If the predictions are incorrect, can you think of a modification of the Condition, or the analysis of definite descriptions, or something else (be reasonable), that would yield the right results?

(14) a. *John talked to the girl who read any book.
b. *John didn’t talk to the girl who read any book.

(15) The mayor with any sense will control the school board.

(iii) What do we need to assume in order for the Condition to predict that (16) is acceptable?

(16) The workers who attended any DSA rallies were fired.
