> 检索摘要：18.915 Graduate Topology Seminar: Kan Seminar（Fall 2014，Graduate）的「Reading Responses November」。页内标题：Reading Responses November；5 Nov；5 Nov；7 Nov；7 Nov；14 Nov；16 Nov；19 Nov；19 Nov；20 Nov；21 Nov；24 Nov。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-915-graduate-topology-seminar-kan-seminar-fall-2014/pages/reading-responses/november/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Reading Responses November

#### 5 Nov

*Response to*: Quillen, D. G. “Algebraic K–theory I.” In **Higher K-Theories (*Lecture Notes in Mathematics)*.** Vol. 341. Proceedings of the Conference Held at the Seattle Research Center of Battelle Memorial Institute. Springer, 1973, pp. 85–147. ISBN: 9783540064343.

Dear Professor Miller,

Here is my response:

1. In the construction of BC in section 1, its required that C be a small category. This is only up to equivalence, right? I should have in my mind that we want to apply this to the category of vector bundles on a space, right? But vector bundles over a point gives you the category of vector spaces, which isn’t small… But its equivalent to a small category where you just record the dimension of the vector space (which is obviously gives the isomorphism class). Is this what he means when he says “the proceeding definition extends to categories having a set of isomorphism classes of objects” on page 95/19/103 (depending on which page numbering system you’re looking at)?
2. I already have in my mind a notion of BG for G a group… But I can also define a group to be a category with one object and the morphisms indexed by elements of G with composition given by the group law. Do I get an equivalent classifying space under this construction?
3. We have a notion of K_i already, which is the K-homology (we can define using the theory of spectra in Lyubo’s paper). If we take the category of vector bundles on a topological space, do these “topological” and “algebraic” notions coincide at all?
4. These higher K-groups don’t seem to be easily computable (at least from what I can see in the first section of this paper). Have people come up with good techniques for computing higher algebraic K-theory? How useful are these K-theory groups?

(To be fair, I know that there is a seminar going on at Harvard at the moment on higher dimensional class field theory that uses algebraic K-theory, so I guess number theorists have found this useful!)

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 5 Nov

1. Sure - the category of finitely generated projectives isn’t small. But any two choices of small equivalent subcategories will give you canonically homotopy equivalent Q constructions.
2. Yes, of course. You could see it in the specific description of the nerve that [Student Name] gave. However, there are some differences. BC might not be connected! And any space is weakly equivalent to the classifying space of some category. (The category of simplices in the singular simplicial set, for example.)
3. The algebraic K-theory of the discrete ring of complex numbers is not quite right. For one thing, topological K-theory is periodic, while algebraic K-theory is the homotopy of a space… This can be modified; the space BQ is actually an infinite loop space, so K_*(M) is the homotopy of a spectrum, but it still is zero for negative dimensions. And even in positive dimensions it’s not quite right. There is a way to put the topology of C back into play, and then you get BQ = BU.
4. Not easily computed is putting it mildly. Quillen (in a paper we discussed) computed it for finite fields. Borel computed it rationally for number rings. Quillen’s theorems in this paper describe relationships between K-theories of different rings. But some of the deepest work in topology in the past thirty years has been concerned with this question: The Quillen-Lichtenbaum conjectures, Voevodsky’s work on the Milnor conjecture, the entire development of the cyclotomic trace by Madsen, Hesselholt, and many others … all this is addressed at these computations. Clark Barwick represents the contemporary forefront of that effort.

Algebraic K-theory has a lot to do with algebraic cycles. Spencer Bloch is the relevant name. To be fair, I think it’s fair to say that the payoff in arithmetic has not been as great as had been hoped at first. But maybe it’s just a matter of time. I had not heard of this seminar on higher dimensional class field theory.

Haynes

________________________________________________________________________________________________________________

#### 7 Nov

*Response to:* Nishida, G. “[The Nilpotency of Elements of the Stable Homotopy Groups of Spheres](http://dx.doi.org/10.2969/jmsj/02540707).” *Journal of the Mathematical Society of Japan* 25, no. 4 (1973): 707–32.

Dear Professor Miller,

I’m sorry this is going to be a terrible response, since I spent most of my time over the past few days preparing my talk. But anyhow, some thoughts:

I think this paper is pretty cool, I like seeing that this “D_nX” construction we saw on the first day to construct the Steenrod operations comes up to prove this theorem about nilpotency of order p elements in \pi_t^s(S^0). I also like papers with concrete computations!

The proof of proposition 1.6 using the fact that D_n^(r)(S^k) is a Thom complex of a vector bundle which is a of finite order in the real K-theory of BS_n^(r)… I am a little confused about how the conclusion follows?

Also, a key theorem for him is the homology of the “infinite loop space” Q(X) =lim \Omega^\infty S^\infty X given in Theorem 2.3 due to Dyer-Lashof. The result clearly reminds one of the cohomology of Eigenberg-Maclane spaces that we already saw. What was the original motivation for proving such a result on the mod p homology of Q(X) in terms of the homology of X? (Obviously its very useful here.)

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 7 Nov

Isabel

Do you get the identification of D_n S^k with a Thom space? Remember the exercise I didn’t carry out? (It’s sketched, but poorly, by Hatcher.) You want to know that Sq^0 is nonzero in some example; why not S^1. So look at D_2(S^1) . The claim is that it’s the Thom space of the bundle over RP^\infty associated to the canonical representation of C_2. This representation is 1 + sign, so the Thom space is the suspension of RP^\infty. Now you have to think about what the diagonal map looks like in this presentation. It’s going to be the map induced by the inclusion of sign into 1+sign. This induces the map \Sigma RP^\infty_+ –> \Sigma RP^\infty sending the + to the basepoint. This is nonzero enough!

I guess you have to pick the skelata carefully: you want them to have torsion homology. Then the AHSS tells you that the K-theory will be torsion as well.

I guess the motivation for computing H_*(QX) is that it’s there! But the result is amazing: it’s a functor of H_*(X) (field coefficients). It’s worth thinking about what the answer is with Q coefficients; it’s simpler than the finite characteristic case Nishida needs. The key to the calculation is the approximation theorem; this relates QX to the n-adic constructions. So then the surprise is that H_*(D_nX) is a functor of H_*(X). This fact is almost a consequence of the construction of the universal power operation.

Haynes

________________________________________________________________________________________________________________

#### 14 Nov

*Response to*: Quillen, D. G. *Homotopical Algebra (Lecture Notes in Mathematics)*. Vol. 43. Springer, 1967. ISBN: 9783540039143.

Dear Professor Miller,

Here is my response to Quillen’s paper:

I think I have some trouble with these papers that introduce a new construction or concept with seeing how this is useful to solve problems/fits into a larger goal of understanding something. So I asked [Student Name] what the “main point” of this paper was and she said she thought it was the construction of the homotopy category (in terms of inverting weak equivalences) and Theorem 1 (or 1’) which gives a means of more concretely understanding and working in the homotopy category (something I see paying off for Quillen in the latter sections of the paper). She said another key result was the adjunction Theorem 2 at the end of Section 2 giving loops and suspension functors in the homotopy category (and more generally Theorem 3 on left and right derived functors of adjoint functors between model categories).

Would you agree with this? Maybe you could give me some references for how this formalism has paid off more recently (you don’t need to convince me that derived categories are useful, but this seems more general, and I this is my first encounter with model categories). Some things that I found enlightening were examples and remarks at the end of section 4 following the proof of Theorem 3 mentioned above. I should also probably look at the second half of the paper that [Student Name] isn’t planning on covering, because it might provide more motivation by way of examples.

Thanks,
Isabel

________________________________________________________________________________________________________________

#### 16 Nov

Isabel

Just wait! [Student Name] will describe a wonderful example of the practical application of this theory.

But in general, you may want to be sure that some construction has homotopy theoretic content, or want to know how to modify it so that it does. This is how Tor is derived from tensor, or Ext from Hom. But what if you’re working in a non-additive situation, where chain complexes don’t make much sense (and where the proof of the fundamental theorem of homological algebra fails)? A good example is provided by commutative rings, but almost any category of universal algebras well work the same way. In the second part of HA, Quillen sets up a model category structure on simplicial obects in such a category. This lets him say what a “projective resolution” is: it’s a cofibrant replacement of a constant object. In another landmark paper, he explains what the universal meaning of “homology” is: you fix an object X and look at the category of abelian objects over it. There’s usually an abelianization functor Ab from objects over X to Abelian ones. Apply Ab to a cofibrant replacement for X as an object over itself; this gives you a simplicial object in a category of abelian objects, which is usually abelian. So now you can form the associated chain complex and its homology. That’s the “Quillen homology” of X.

In brief, Quillen homology is derived functors of abelianization.

Haynes

________________________________________________________________________________________________________________

#### 19 Nov

*Response to*: Bousfield, A. K. “[The Localization of Spaces with Respect to Homology](http://dx.doi.org/10.1016/0040-9383%2875%2990023-3).” *Topology* 14, no. 2 (1975): 133–50.

Hi Professor Miller,

Here is my response to the Bousfield paper:

1. Yes! This was a very nice application of Quillen’s model category framework! Especially since the main theorem is so easy to prove once you have that the h_*-equivalences can be used as weak equivalences instead of weak homotopy equivalences in the model structure on the category of simplicial sets. It definitely makes it seem like the right framework.
2. But I want to make sure I understand the proof that localizations exist with respect to any homology theory h_*. So he wants to prove that there is a localization functor E on the pointed homotopy category of CW complexes, along with a natural transformation \eta : 1 \to E satisfying a universal property. But to prove this, he uses the alternate model structure defined above on simplicial sets. This reminds me of one of the other theorems Quillen proved in the paper we read that there is an equivalence of model categories between the pointed homotopy category of simplicial sets and the pointed homotopy category of topological spaces via the adjoint functors of geometric realization and singular set. Does he not have to deal with any of the details of this because he can define this model structure on the pointed homotopy category of CW complexes by the structure on simplicial sets and geometric realization? Is this what he means when he says “This abuse [of notation in letting Ho denote the category of Kan complexes or CW complexes] is harmless because the geometric realization provides an equivalence between the Kan and CW pointed homotopy categories.”? He cites a paper of May on “Simplicial Objects in Algebraic Topology” here.
3. Do people care about homology theories that aren’t ordinary singular homology with coefficients? (I would assume so… such as K-theory?) And homology theories that aren’t connective, which he says means that the acyclic spaces are the same as ordinary homology with coefficients? I couldn’t find much about this by some short googling…
4. Why are the “algebraic” conditions given in sections 5-9 useful? Is it just for intuition or completeness, not that they are actually computable?
5. Also googling around about this subject I found: [http://mathoverflow.net/questions/173546/why-localize-spaces-with-respect-to-homology](http://mathoverflow.net/questions/173546/why-localize-spaces-with-respect-to-homology), which seems to say that localization can not only simplify a problem but make more phenomena appear… I also like the observation that the only reason Adams lacked a proof of localization with respect to any homology-theory was set-theoretic concerns.

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 19 Nov

Isabel

1. Glad you liked it!
2. Well, I think that all the model category work in this paper takes place in simplicial sets. He uses spaces only to say what he means by ‘generalized homology theory.’ I think he refers to may rather than Quillen at this point because he doesn’t even care that the homotopy *theories* of simplicial sets and spaces coincide; only that the homotopy categories do.
3. You bet! Yes, K-theory is a good example; we defined a cohomology theory, represented by a spectrum, and in turn the spectrum determines a homology theory, by taking the homotopy of a space smashed with the spectrum. In fact there’s a whole swarm of analogues of K-theory, also nonconnective, including so-called elliptic homology theory. And there are many interesting connective theories. Bordism is one, determined by a Thom spectrum, and represented by bordism classes of singular manifolds. I think [Student Name] will talk about complex bordism, for example. Any spectrum admits a “connective cover,” in which the negative dimensional homotopy groups have been killed. So there’s “connective K-theory,” for example.
4. Well, localization can’t exactly create something from nothing. But things become so much clearer and easier to talk about that new things appear. Stable homotopy theory itself is a kind of localization; you are inverting the suspension functor. And there are are a lot of ’new’ things there!

Yes, Adams proposed this topological enrichment of Serre’s mod C theory, but neglected the set theory. I think he was also mainly interested in the stable picture. Bousfield has another paper called “Localizing spectra with respect to homology.”

Haynes

________________________________________________________________________________________________________________

#### 20 Nov

*Response to*: Griffiths, P. A., and J. W. Morgan. *Rational Homotopy Theory and Differential Forms*. Birkh ̈auser, 1981. ISBN: 9783764330415.

Hi Professor Miller,

Here is my response to Griffiths and Morgan ([Student Name] told us to skim chapters 8–12):

1. I really enjoyed this paper!
2. I am glad that Prop 8.7 and Cor 8.8 hold! I was starting to type out a question to you about how C^\infty manifolds can be triangulated, so if I viewed this manifold as a simplicial complex by this triangulation, would I get the same homology theory taking piece-wise linear forms and C^\infty forms… but then I got to this proposition and I see that you do, in fact (up to tensoring with R). But you don’t get the same DGA of the cochain complex.
3. I really like section IX about commuting cochains and that the obstruction for Z-coefficients is really in the existence of cohomology operations (well, the Steenrod ops can be defined using failure of commutativity on the cochain level – this was a nice tie-up with things we’ve seen before)! But I am a little confused about why rational cohomology for a simplicial complex doesn’t give commutative cochains…? I don’t see why (v) isn’t satisfied —this is saying that the map on cochains isn’t surjective, right? But why can’t you extend your function from Y to X by 0 on the complement? I’m probably missing something really silly here…
4. I don’t really appreciate this sentence “So now we have come full circle. The problem of commutative cochains is equivalent to finding not only the cohomology, but also the Q-homotopy type of a space from a chain complex.” – probably from not reading the first 7 chapters of the book. But the idea is that we want to extract from Q-cochain data the maximum information, and it turns out that you can tell the Q-homotopy type if you have commuting cochains (but once you pass to homology you loose this). Is this the most important take-away of the paper – coupled with the piece-wise linear forms which realize commuting rational cochains? Because sections IX, X, XI, and XII seem to be devoted to understanding this.
5. Building on (3), is it hard to compute commuting cochains? (Or we could just say piecewise linear differential forms for concreteness.) Rational homotopy doesn’t include the information of torsion in the fundamental groups, so perhaps it’s more computable anyways?

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 21 Nov

Isabel

1. There are many DGA models (but up to noncanonical iso the minimal model is unique).
2. The “complement” isn’t a simplicial complex. Or: if you think of a 0-cochain as a continuous function to Q, you won’t be able to extend it continuously.
3. In other developments (Quillen, Bousfield-Guggenheim), you construct a model category structure on commutative rational coalgebras and show that it’s Quillen equivalent to the HQ-local model category on simply connected spaces. So DGAs give you a complete picture of rational homotopy theory.
4. Let’s try to find the minimal model of S^{2n}. [Student Name] didn’t quite say this explicitly, but part of his dictionary is that \Lambda(x_k) is the minimal model for K(Z,k). (You can check this by inductively computing the rational cohomology of K(Z,k).) Map S^{2n} –> K(Z,2n). It’s not a rational equivalence; there’s a 4-dimensional class in the EM space that pulls back to 0. So kill it by a map to K(Z,4n). The homotopy fiber sits in a fiber sequence K(Z,4n-1) –> E –> K(Z,4n), and now S^{2n} –> E is a rational equivalence. The corresponding Hirsch extension is \Lambda(x,y) with |x| = 2n, |y| = 4n-1 , and dy=x^2. That’s it!

The most amazing thing, from my perspective, is this: the rational homotopy of X is the vector space dual to the indecomposables in minimal model for X. Check: the rational homotopy of S^{2n} is nontrivial only in dimensions 2n and 4n-1.

There are general classes of spaces which are known to be “formal,” that is, the cohomology ring itself serves as a DGA model. Polynomial cohomology is one way to guarantee this. Also the famous theorem of Deligne, Griffiths, Morgan, Sullivan, says that any compact Kaehler manifold is formal.

Haynes

________________________________________________________________________________________________________________

#### 24 Nov

*Response to*: Segal, G. “[Categories and Cohomology Theories](http://dx.doi.org/10.1016/0040-9383%2874%2990022-6).” *Topology* 13, no. 3 (1974): 293–312.

Hi Professor Miller:

Here is my response to the Segal paper:

So the (rough) basic idea of this paper is that to a category we associate an infinite loop space (well, a spectrum which is often an infinite loop space). And this is a generalization of a topological abelian group because composition only commutes up to homotopy. The spectrum we get then defines a generalized cohomology theory, which again generalizes what we would get from a topological abelian group in which this is just the direct sum of ordinary cohomology with coefficients. Is that right? The obstruction to the cohomology theory being direct sum of ordinary cohomology is the fact that composition doesn’t commute on the nose so an infinite loop space doesn’t have the homotopy type of a topological abelian group? (This might be a really silly question, but is there some way to measure difference in cohomology theories that illustrates this obstruction to your theory being ordinary cohomology?)

Something else:

I was trying to think if his definition of classifying space of a Gamma space is natural in that it generalizes classifying spaces of topological abelian groups – I mean, it must, right? So I tried to work this out with my hands, if you took the Gamma-space corresponding to a topological abelian group (well, just finite abelian group to make it easier). I got a little stuck —but I’m going to try to work this out after seeing [Student Name’s] talk today. One potentially tricky thing is that he uses a different definition of realization..? Is it easier to work this out in the language of Gamma spaces or Gamma categories?

(By the way, I figured out an answer to the kernels and cokernels of locally free coherent sheaves… I’ll tell you today in our meeting.)

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 24 Nov

Isabel

Well, let’s see. A category has a classifying space. In fact any space is weakly equivalent to the classifying space of the category singular simplices in it. So you need extra structure to get an infinite loop space. One such structure is a symmetric monoidal structure. This still doesn’t quite give an infinite loop space, generally; you only get one after “group completing,” which is, in this topological context, formation of the loop space on the next space in the spectrum.

Mere homotopy commutativity isn’t enough, right? You need something to produce extensions of the n-fold product through the extended n-th symmetric power, and they have to be compatible. Or, in Segal’s framework, you need an entire \Gamma-space, not just the first couple of terms of one.

What you say about topological abelian groups and ordinary cohomology is right! The best answer to the question of how to distinguish spectra that are not products of EM spectra from those that are is that the K-invariants are nontrivial in the former case and trivial in the second. But you can also just inspect: Z\times BU for example is the 0-space of the omega spectrum for K-theory, and it’s visibly not a product of EM spaces.

Remember, the “classifying space” construction takes a \Gamma space to another \Gamma space. As [Student Name] pointed out, (BA)(1) is the geometric realization of A regarded as a simplicial set via the inclusion \Delta^op –> Fin_*. The \Gamma space A associated to an abelian group G has A(n)=G^n, and you can check that the structure of simplicial space is exactly the bar-construction simplicial space whose realization is BG.

I agree with your resolution of my confusion, but I still feel confused.

Haynes
