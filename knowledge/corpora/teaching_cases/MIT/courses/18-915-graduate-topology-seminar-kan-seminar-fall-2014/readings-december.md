> 检索摘要：18.915 Graduate Topology Seminar: Kan Seminar（Fall 2014，Graduate）的「Reading Responses December」。页内标题：Reading Responses December；3 Dec；3 Dec；5 Dec；5 Dec。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-915-graduate-topology-seminar-kan-seminar-fall-2014/pages/reading-responses/december/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Reading Responses December

#### 3 Dec

*Response to*: Tillmann, U. “Mumford’s Conjecture—A Topological Outlook.” In *Handbook of Moduli: Volume III (Advanced Lectures in Mathematics).* Vol. 26. International Press of Boston, 2013, pp. 399–429. ISBN: 9781571462596.

Dear Professor Miller,

Here is my response to the Tillmann Paper:

1. Is the idea that M_g^top is easier to work with since its a classifying space, but for proving Mumford;s conjecture, the fact that it is rationally equivalent to M_g is enough? It seems that M_g^top is interesting in its own right, especially given the homotopy theory in the rest of the paper.
2. Is there any geometric intuition for Mumford’s conjecture? It seems that in the way it is phrased it is very geometric, but the proof relies on topological techniques.
3. What is the main take-away from this? How does knowing this result that the stable rational cohomology of M_g is a polynomial algebra on some explicit generators prove useful? Or what is the take-away from the broader topological framework?

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 3 Dec

Isabel

1. I agree. Coarse moduli spaces are just weird.
2. Well, the classes \kappa_i are very natural, and nobody could think of any other way to generate characteristic classes for surface bundles. That’s when conjectures bubble up. What Mumford did not conjecture, because it requires topological techniques, is that the scanning map is an integral equivalence, not just rational. The question of the relations among those classes in H^*(BDiff_g) is very interesting. I think the image is actually finite dimensional.
3. This was a big step forward in understanding characteristic classes for surface bundles. Perhaps it’s unfair to ask why one would be interested in such things in the first place. The techniques have proven very important too, and have led to a whole range of analogous theorems about diffeomorphism groups in higher and lower dimensions. In lower dim’s, you are looking at homotopy automorphisms of graphs, or what is the same the automorphism group of a free group. These can again be stabilized, and Soren Galatius worked out what the analogous infinite loop space is. In higher dimensions we don’t have such a clean way to stabilize, but there are still results around (by Galatius and others).

Also the spectrum MTSO(d) has been seen before. An alias is Th(-can | BSO(d)) where can is the canonical d-plane bundle and by Th I mean the Thom spectrum of the virtual vector bundle associated to -can.

Haynes

________________________________________________________________________________________________________________

#### 5 Dec

*Response to*: Adams, J. F. “Quillen’s Work on Formal Groups and Complex Cobordism.” In *Stable Homotopy and Generalised Homology* *(Chicago Lectures in Mathematics)*. University of Chicago Press, 1995. ISBN: 9780226005249. [reprint of the 1974 original]

Hi Professor Miller,

My response is below:

First of all, reading this paper was really satisfying! I’ve really only seen the usefulness of formal groups from the angle of number theory, so I enjoyed this a lot, and I’m glad I finally read it.

More particular things:

1. The Lazard ring really measures the constraints put on a formal group to be associative and commutative, right? But then this intuitive definition (which obviously satisfies the desired universal property) doesn’t give a satisfactory tool because of the relations. So Lazard’s theorem can be thought of as giving something more of a practical handle on this?
2. You’re right, given Milnor’s result on pi_*(MU) being a polynomial algebra in generators of the right degree, Quillen’s theorem just feels like it has to be true for algebraic reasons! Is there any intuition? Also, I understand what the Lazard ring means… is there some reason why I should understand pi_*(MU) to satisfy the same universal properties? Is this isomorphism canonical (I think no? Was there choice involved in the formal group law?)?
3. Cor 9.2 of section 9 makes me think immediately of multiplicative genera….

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 5 Dec

Isabel

Lazard’s theorem is equivalent to the statement that any (1d, commutative) formal group can be lifted across any surjection of rings. The annoying thing about Lazard’s theorem is that it doesn’t provide you with generators. This defect is one of the reasons for liking the condition of p-typicality.

Quillen’s approach is to try to show that the generators of the MU formal group law generate MU_*. He does this using a version of Steenrod operations on MU_*.

Suppose you have a commutative monoid R in the stable homotopy category (a “ring spectrum”) whose homotopy groups are zero in odd dimensions (eg K-theory). Then you can compute that R^*(CP^\infty) is a power series ring over R^*, and you get a formal group over R^*. The set of coordinates for this formal group are in bijection with the set of ring spectrum maps from MU.

Formal groups provide an interpretation genera for U-manfolds. All the parts of the theory of genera have interpretations in terms of formal groups. The characteristic series is x/exp(x), for example. I think Miscenko’s theorem is exceptionally beautiful!

Haynes
