> 检索摘要：18.915 Graduate Topology Seminar: Kan Seminar（Fall 2014，Graduate）的「Reading Responses October」。页内标题：Reading Responses October；1 Oct；1 Oct；3 Oct；3 Oct；8 Oct；8 Oct；20 Oct；20 Oct；24 Oct；24 Oct；29 Oct。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/18-915-graduate-topology-seminar-kan-seminar-fall-2014/pages/reading-responses/october/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Reading Responses October

#### 1 Oct

*Response to*: Milnor, J. W. “[On Manifolds Homeomorphic to the 7–sphere](http://www.jstor.org/stable/1969983).” *Annals of Mathematics* 64, no. 2 (1956): 399–405.

Dear Professor Miller,

Here is my response to the Milnor paper:

1. A very key point to the argument is that any closed and oriented 7 manifold can be realized as the boundary of an eight manifold—e.g. the degree 7 piece of the cobordism ring is trivial (not just 2-torsions!)… After reading this I looked back at pg 203 of Milnor-Stasheff and sure enough he cites this result (as well as that the degrees 1, 2, 3, and 6 pieces vanish as well). But by taking appropriate products you can show that above 7 all cobordism groups are nonzero. So this method of generating an invariant of 7-manifolds is quite unique to this case. Presumably people have found other examples where homeomorphic manifolds of dimension higher than 7 aren’t diffeomorphic…. Do you know what extra ingredients had to go into this? Also, before this paper, did people think that homeomorphic smooth manifolds with a differentiable structure were diffeomorphic?
2. I found the Morse theory argument used to show the 7-manifolds constructed are ``exotic 7-spheres" very interesting if a little out of my comfort zone of things I understand (I know very little about this). Is this a standard way of proving the types of results that Milnor is after? (e.g. that if you have such a map with such critical points then you can cook up a homeomorphism onto some topological space). In his practice talk [Student Name] mentioned you might use homotopy theory to prove that these topological spaces constructed are exotic 7-spheres. A nice thing that comes out of this Morse theory approach is that the obstruction to being diffeomorphic to S^7 (with its standard differentiable structure) is a single point (I’m not sure if this is obvious otherwise?)

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 1 Oct

Isabel,

It helped a lot when Kervaire and Milnor showed that any smooth manifold homotopy equivalent to a sphere embeds in a Euclidean space with *trivial* normal bundle. That guarantees that it will bound, since all its SW classes are zero. It also gives an invariant in the group of framed bordism classes modulo reframings, the “cokernel of J.” K&M go on to almost completely analyze this; In dim 4k it’s an iso. In dim 4k-1 (eg 7) it is surjective with kernel determined essentially by the signature theorem (so cyclic of order given in terms of Bernoulli numbers). In the other dimensions they nail things down up to a factor of two, which is the famous Kervaire invariant, subject of this semester’s Juvitop.

People worked very hard to prove that there were no exotic smooth structures in dimension 2. They understood the possibilities, and spoke of the “smooth Poincare conjecture.” But I don’t think there were fixed beliefs. Certainly Milnor’s paper was celebrated!

[Student Name] wanted to apply the “h-cobordism theorem,” which I think came after this paper. It gives a systematic way to try to prove that two homotopy-equivalent manifolds are diffeomorphic, and comes with an obstruction (the “surgery invariant”) if it fails. But this is out of my comfort zone too!

Haynes

________________________________________________________________________________________________________________

#### 3 Oct

*Response to:* Atiyah, M. F. *K–theory* *(Advanced Book Classics)*. 2nd ed. Notes by D. W. Anderson. Addison Wesley Longman Publishing Company, 1989. ISBN: 9780201093940.

Dear Professor Miller,

Here is my response:

There seem to be several ways to define K-theory of X (say complex K-theory)…. you could do it as maps from X to BU(\infty). Well, this gives you K^0(X) reduced. To get higher homotopy groups you’d have to map into a space whose loops is the classifying space for n-1st K-theory. Then you apply Bott periodicity to see that the homotopy classes of iterated loops on BU(\infty) are 2-periodic, and so K-theory is periodic, and we really care about K^0 and K^1… Or you could take the route of defining higher K-groups to be the derived functor of K^0… Or you could do what the paper does and say that (Def 2.4.1 on pg 68) that reduced -nth K theory is the reduced K-theory of S^nX. Its clear that some of these definitions agree, like the third implies the second because Atiyah proves the LES in K-theory. And maybe the second implies the first by general theory. Its also pretty easy to see that reduced K^0 agrees with this Maps(X, BU), once you have the results that Atiyah covers in section 1 about any k-plane vector bundle as the subbundle of a trivial bundle, you naturally get the map to the Grassmanian of k-planes. I guess I’m wondering about the relation between these definitions and what is most useful to think about in practice?

A related question is what tools are there to compute K-theory… I know there is the spectral sequence relating the K-theory of a space to its cohomology and the K-theory of a point… which is easy. You could also use the fact that the chern classes give maps from K-theory to cohomology. Atiyah manages to use the LES in K-theory as well around pg 80. What other tools are there?

Thanks,
Isabel

________________________________________________________________________________________________________________

#### 3 Oct

[Student Name] did a nice job of linking up the various definitions.

Actually a ‘reduced’ cohomology theory is best thought of as K(X,*). So it’s *pointed* homotopy classes of pointed maps X –> Z x BU. If X is connected (as [Student Name] kept assuming) then a pointed map has to land in the 0-component of Z x BU (which is where the basepoint is). But if X is not connected, then reduced K-theory is not quite [X,BU].

And it’s not quite true that \Omega^(BU) = BU: rather, it’s Z x BU.

Hey, how can I think of higher K-groups as derived functors of K^0? Seriously, if you have a way of thinking about that please tell me.

Atiyah basically doesn’t mention cohomology; this is the axe that he is grinding. But a major tool in understanding K-theory is the AHSS, which you mention. Another is the Chern character,

ch: K –> HQ. It’s a multiplicative transformation, sending K^0(X) to the direct sum of the even rational cohomology groups of X (for X a finite complex) and K^1(X) to the sum of the odd groups.
It’s a rational isomorphism….

Haynes

________________________________________________________________________________________________________________

#### 8 Oct

*Response to:* Adams, J. F., and M. F. Atiyah. [“K–theory and the Hopf Invariant](http://qjmath.oxfordjournals.org/content/17/1/31.full.pdf+html).” *The Quarterly Journal of Mathematics* 17, no. 1 (1966): 31–38.

Dear Professor Miller,

Here is my response to Hopf Invariant 1:

The main thing one has to note from this paper is how simple and beautiful the argument is! (But I think that’s most apparent, from my perspective, since Adams and Atiyah didn’t have to do any difficult computations of K theory – the reduced K-theory is easily seen to be free on the generators coming from the cells in dimensions n and 2n in cohomology… Then if you compare the arguments in the vector fields on spheres paper and this one (modulo the computation of K-theory) they are both very simply and boil down to very similar obstructions.) Something I was wondering was, when you have an isomorphism between the K-theory and cohomology rings, what do the Adams operations correspond to on the level of cohomology? Is this even a reasonable question to ask?

Could we plan on meeting this afternoon? You can let me know when you’re free after 4:30 (alternatively I can meet right after class until 11:30 am or before class).

Thank you,
Isabel

________________________________________________________________________________________________________________

#### 8 Oct

Isabel

You are only guaranteed a ring isomorphism modulo filtration, or rationally. The rational bit comes from the Chern character, a ring homomorphism ch : K(X) –> H^{even}(X;Q) that extends to an isomorphism after tensoring with Q. Under ch, \psi^k corresponds to multiplying by k^n on H^{2n}: so it picks out the grading as eigenspaces.

Somehow the proof works for K-theory because you are entitled to work modulo a higher power of 2. K-theory has some surprising torsion properties; for example, the K-theory of RP^\infty is torsion-free.

See you this afternoon.

Haynes

________________________________________________________________________________________________________________

#### 20 Oct

*Response to:* Quillen, D. G. “[The Spectrum of an Equivariant Cohomology Ring: I](http://www.jstor.org/stable/1970770).” *Annals of Mathematics* 94, no. 3 (1971): 549–72.

Dear Professor Miller,

Here is my response:

The results about equivariant cohomology of G-spaces seemed very natural, when you think that for X with a free G-action, the G-equivariant cohomology should just be H^*(X/G). But then the problem is that if the action isn’t free, this isn’t a homotopy invariant (e.g. S^\infty and a point with a Z/2Z action, which is free on S^\infty, but the quotient RP^\infty is not contractible). So if you want to define equivariant cohomology of X to be the cohomology of Y/G for some Y in the homotopy class of your space with a free G action, then EG \times X would give such a space Y. And this is exactly the definition Quillen gives (except to call it PG).

I found the results about the cohomology of BG (e.g. G-equivariant cohomology of a point) very interesting. In particular theorem 7.1, which says (approximately) that to calculate H^*(BG, Z/pZ) up to nilpotents, it is enough to know H^*(BA, Z/pZ) for A an elementary p-group. In the case that G is a finitely generated abelian group, BG is a K(G,1). And Serre’s paper (which [Student Name] also presented!) gives techniques to compute the cohomology of this Eilenberg-MacLane space. So can you prove these results easily using this machinery in this special case? Or even in the special case when p=2 and you can just apply Serre’s results? In any case, this Theorem seems interesting, as well as the corollary that the dimension of H^*(BG, Z/pZ) is the maximum rank of an elementary p-group. What’s the intuition behind why this theorem (7.1 or more generally for G-spaces) should be true?

Thanks,
Isabel

________________________________________________________________________________________________________________

#### 20 Oct

Isabel

BG is always a K(G,1) … you can define H^1(X;G) for non nec abelian G (as isomorphism classes of principal G-bundles over X).

But we’re speaking here about K(Z/p,1) (or a power of this space). That’s easy; its skelata are called “lens spaces.” One way to get at it is to think about the fibration derived from the group extension Z/p –> S^1 –> S^1: S^1 –> BZ/p –> CP^\infty. With integral coefficients, p times the generator of H^2(CP^\infty) pulls back to zero, so you must have d_2(generator of S^1) = px. From this you can conclude that H^*(BZ/p;F_p)=E[e]\tensor F_p[x] with |e| = 1, |x| = 2, and the two connected by the Bockstein. (When p=2 there’s an extension, e^2=x.)

So Spec H^*(BE) is an affine space, if E is elementary abelian. Quillen shows that Spec H^*(BG) is a colimit of these affine spaces; it’s a bunch of affine spaces, corresponding to conjugacy classes of maximal elementary abelian subgroups, glued together according to certain conjugacies. In particular the Krull dimension of H^*(BG) is the largest of the ranks of the elementary abelian subgroups.

Maybe the intuition comes from the corresponding result where you replace F_p by Q. Then it goes back to Elie Cartan, maybe, that H^*(BG;Q) = H^*(BT;Q)^W . Here G is a connected compact Lie group T a maximal torus, and W the Weil group (ie the group of isomorphisms of T induced by conjugation by elements in G). The mod p picture is more complicated in general because there may be difference conjugacy classes of maximal elementary abelian p-subgroups. (They can even have different ranks.)

Haynes

________________________________________________________________________________________________________________

#### 24 Oct

*Response to:* Wall, C. T. C. “[Finiteness Conditions for CW–complexes](http://www.jstor.org/stable/1970382).” *Annals of Mathematics* 81, no. 1 (1965): 56-69.

Hi Prof. Miller,

Here is a response to Wall’s paper:

If I understand correctly, a key insight of this paper is in the algebraic conditions placed on a complex to be equivalent to one of finite type (or finite dimension). That is, these conditions Fn for finite type, and Dn for finite dimension. At least in the case of finite type, the proofs seem to be rather straightforward and builds on Milnor’s construction in the simply-connected case.

Section 3 seems more interesting, in particular Theorem F (and the Lemmas 3.1 and 3.2 leading up to Theorem F), that gives that the class of \pi_n(\phi) in the projective class group for \phi an (n-1)map from a finite complex K^(n-1) to X depends only on X if X satisfies the algebraic conditions Fn and Dn. This really uses the fundamental group in a very nontrivial way, since if X were simply connected, then \Lambda = Z and as Z is a PID, projective Z-modules are free so this projective class group is trivial, and all classes are trivial [In fact as observed latter the same is true if \pi is free abelian]. Is it clear immediately that \pi is the obstruction to this problem being obvious? (I guess this comes up in section 1 as well, with the algebraic conditions Fn, and his key insight is extending Milnor’s work to the non-simply connected case).

Another question is whether the other questions he poses in the introduction have been answered? Is the best way to think about these finite conditions still in terms of the algebraic constraints put on classes in a projective class group?

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 24 Oct

Milnor’s theorem (in the appendix) is one of my favorite results! I agree, this paper is really working out what you can say in analogy with that result in the non simply connected case.

My impression of the utility of this result today is this. One receives a homotopy type, which you know in advance is finitely dominated. Often your ultimate goal will be to show that it contains a compact manifold. A first step is to show that it contains a finite complex. So those obscure conditions are not used to verify finite domination, but rather to use finite domination to construct the invariant in the projective class group.

One of the surprises of the construction of this invariant is that it depends only on the top dimension. I suspect that there is a different way to produce the invariant which is more intrinsic - not depending on the construction of a map \phi - but in exchange uses more dimensions. For example you have the chain complex of the universal cover …

Haynes

________________________________________________________________________________________________________________

#### 29 Oct

*Response to:* Adams, J. F. *Stable Homotopy and Generalised Homology (Part III) (Chicago Lectures in Mathematics)*. University of Chicago Press, 1995. ISBN: 9780226005249. [Preview with [Google Books](http://books.google.com/books?id=6vG13YQcPnYC&pg=PAfrontcover)] [reprint of the 1974 original]

Dear Professor Miller,

Here is my response:

A disclaimer is that I know very little stable homotopy theory already, so I am mostly searching for some motivation. I see how the category of spectra is a natural definition if you want to study stable phenomena, and how the definition of maps in this category are the natural choice again if you care primarily about stable phenomena. I’m not sure exactly why we care about this (other than maybe its more computable?), and Adams hints that you can also use this to study unstable problems? And the stable category of spectra is sufficiently “nice”… Maybe you could also give me some context for this, since I don’t have much of a background in which to fit this. A couple of things that came up in the paper:

1. It’s a very nice argument that the spectrum associated to any cohomology theory (where you have excision) is an \Omega-spectrum. I think that Adams says that any (CW?) spectrum is equivalent to an \Omega-spectrum, so you can think of any spectrum as being iterated loop spaces. Is there an easy way to see this? Then, we can defined a (co)homology theory using an \Omega-spectrum E with, like E^r(X) = [X, E]_r degree r maps… So maybe I should think about spectra as really ways to getting cohomology theories.
2. How do you explicitly define a degree 1 “map” (not function) of S \to S (the sphere spectra) that extends the Hopf map S^3 \to S^2? This isn’t going to be a fibration with sphere fibres, and the homotopy groups \pi_{n+1}(S^n) don’t stabilize until after the Hopf fibration at n=2. But Adams seems to hint at this ideas as a goal when motivating the discussion of maps not functions.

Thanks! I think some motivation will probably be provided in the talk tomorrow and in the future.

Best,
Isabel

________________________________________________________________________________________________________________

#### 30 Oct

Isabel

Stable homotopy theory is a certain kind of localization of ordinary homotopy theory: you formally invert the suspension functor. It takes a certain amount of care to make this work right. So in a certain sense everything you do in the stable category is some sort of complicated limit of unstable constructions. But keeping track of the range of dimensions in which certain constructions work is a big hassle, and it’s taken care of automatically by the stable category. You saw an example in the construction of the Atiyah-Hirzebruch spectral sequence.

But then it turns out that this particular localization has extraordinarily beautiful properties, and makes a compelling object of study on its own merit.

It also forms a universal example. Any kind of derived category is enriched over spectra, for example.

Does this help? Here’s another motiviation: You are right, of course, spectra “are” cohomology theories. What the category of spectra (and maps) does for you is that it lets you form things like cofibers. So any natural transformation of cohomology theories embeds into a long exact sequence in which the third term is also a cohomology theory …. Coefficient sequences are one example of this.

Omega spectra … well, I can form \Omega^n E_{n+r} ; and by adjointness it maps into \Omega^{n+1} E_{n+r+1} ; so I can take the direct limit space … this wants to be the r-th space in the \Omega spectrum for E. There are probably some point-set topology problems there, which were probably dealt with by Peter May somewhere.

Hopf map … Can’t I just use \Sigma^{r-2} \eta : S^{r+1} –> S^r ?

Haynes

________________________________________________________________________________________________________________

#### 31 Oct

*Response to:* May, J. P. *The Geometry of Iterated Loop Spaces* *(Lectures Notes in Mathematics).* Vol. 271. Springer-Verlag, 1972.

Dear Prof. Miller,

Here is my response:

1. So the motivation for replacing operads by monads is that the notion of monads is simpler to work with, and we have the Bar construction to get a simplicial space out of a monad…? Could this have all be phrased working with operads? (I guess, an operad determines a monad by construction given in Construction 2.4 of May’s paper,. But a monad is more general, right? So you can’t necessarily go in the other direction?) Lemma 2.10 saying that monads encode the information of an adjunction is a nice way to think about this. And its useful because it gives that \Omega^nS^n is a monad.
2. In the discussion on the bottom of the first page of chapter 5 (pg 39), when he says that the data of L^n (the sequence of n iterated loop spaces of Y) “serves to record the fact that Omega^nY does not determine Y and we must remember Y…” he means that we’ve lost information about the first n-1 homotopy groups of Y by taking n-fold loops, so we can’t uniquely go back to Y from \Omega^nY, right? But the whole idea is we can product some Y via delooping to show that \Omega^n Y is an n-fold loop space.
3. I don’t really see the difference between his definition of L^\infty and bounded \Omega-spectra? (First I’m not really sure what bounded means, and a quick check on the internet didn’t help). Is this something having to do with that he writes Y_i = \Omega Y_{i+1} in J for spaces in the sequence L^\infty, where as for an \Omega-spectrum we have only homotopy equivalences f_i : Y_i \to \OmegaY_{i+1}?

Thanks!
Isabel

________________________________________________________________________________________________________________

#### 31 Oct

Isabel

1. Yes. The monads (or in an older language the triples) you get from an operad are special. For one thing, you need a symmetric monoidal structure just to make sense of the definition of an operad. Also the construction makes them behave smoothly - commute with filtered colimits, for example. I’ve wondered whether there’s an obstruction theory somewhere here actually. By the way [Student Name] didn’t point this out but the use of operads in other symmetric monoidal categories is extremely important; I think Peter’s failure to set them up in that generality in this paper somehow hid them from the algebraists for many years. Going to the monad determined by an adjunction does forget information. You get one of the categories by design. For the other, one choice would be the category of algebras over the monad. An adjoint pair is “tripleable” if that category of algebras is actually equivalent to what you had to start with. Sometimes yes, sometimes no. There is more than one adjoint pair giving a monad. The category of algebras is one extreme. The other extreme is the “Kleisli construction,” which you can google.
2. I think it’s best to say that an “n-fold loop space” IS an expression of the space as the n-fold loops on a specific other space.
3. Sorry, I don’t know the reference here. In other work (maybe here too) Peter May proposes to study (X_i, e) where e: X_i –> \Omega X_{i+1} is a Homemrphism. He calls these “spectra,” and the things with just maps X_i –> \Omega X_{i+1} he calls prespectra.

If you point out the specific reference I can try to respond.

Happy Halloween
Haynes
