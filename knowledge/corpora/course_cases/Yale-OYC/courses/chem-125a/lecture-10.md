- Source: https://oyc.yale.edu/chemistry/chem-125a/lecture-10
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 10 - Reality and the Orbital Approximation

### Overview

In discussions of the Schrödinger equation thus far, the systems described were either one-dimensional or involved a single electron. After discussing how increased nuclear charge affects the energies of one-electron atoms and then discussing hybridization, this lecture finally addresses the simple fact that multi-electron systems cannot be properly described in terms of one-electron orbitals.

### Lecture Chapters

1. “Atom-in-a-Box” Plots: Assessing Probability Density
2. Scaling the Wave Function for Changing Nuclear Charge
3. Scaling Energy with Respect to Nuclear Charge
4. Superposition, and the Orientation and Shape of Hybrid Orbitals
5. An Inconvenient Truth: Troubles Describing Multi-Electron Systems

1. 0
2. 848
3. 1280
4. 1653
5. 2444

| Transcript | Audio |
| --- | --- |
| html
Freshman Organic Chemistry I
CHEM 125a - Lecture 10 - Reality and the Orbital Approximation
Chapter 1. Atom-in-a-Box Plots: Assessing Probability Density [00:00:00]
Professor Michael McBride:
So back to business. We're in a really great position here because we've gone from one dimension to three dimensions, to get something real, a real atom. And if you take that table from last time, that we got from the old-time mathematicians, and plug in according to what you can use together, you get the exact wave function that's a solution of the Schrödinger equation for the hydrogen atom, or any atom that has only one electron. It can have any nuclear charge you want, right? So it's the real thing. People have shown you pictures, which are some kinds of approximations of this, but you have the equation, the actual formula, for the true wave function, and no one has a better one than you have. That's the real McCoy. Okay?
And you can check these pictures that people have drawn to see if they're realistic graphs, or whether they're just some kind of artist's impression, or somebody who doesn't know anything's impression; maybe he's not even an artist. Right? So you can actually do these. And many of them are very simple functions, like
e-r
, right? You can hardly get easier than that. Okay, but you can also draw pictures that look just like what you could see if the electron had a color to it. They're done by ray tracing where the computer pretends it's your eye and sees how much density it would go through, if it went through this point or that point or that point, along a certain ray from your eye, and puts a color here that's proportional to how much electron density it sees. It's not the wave function; it's the square of the wave function, the electron density, that
Atom-in-a-Box
plots. Okay? So that's what it would really look like, if you could see it and if there weren't problems with wavelength and photons knocking electrons to kingdom come and so on.
That's what it would look like, right? But it'll be colored; it'll be colored according to the sign the wave function has. It's not the wave function; it's the square of the wave function. So it would be positive. But it's colored to say the wave function in this region would be positive or in this region negative. And I'll show it to you in just a second, but first let's — or a few minutes — but first let's describe it. So there's lots of information on the screen that you get with
Atom-in-a-Box
. How many of you have tried it? Okay, all of you should. Okay? Okay, first you have the Schrödinger equation. That always appears and it's sort of silly but if you need the Schrödinger equation for reference, there it is. Then up at the top is the particular function that's being plotted, and it's given as
n
,
l
and
m
, and also the nickname
1s
, for this particular one, which is 1,0,0 for
n
,
l
and
m
. And then there's the formula that that particular wave function has, and you know what it is, it's a bunch of constants, which we can forget, but it's
e-r
. He's not using
ρ
here, notice. He uses actual
r
and puts in explicitly the
Z
and the
ao
, and the two is cancelled. Okay? And then he says what the energy would be, in units of electron volts. An electron volt is 23.06 times as big as a kilocalorie, which is what we usually talk in. Now, you can look at these pictures and ask questions, some fairly simple questions, like where is the electron density highest? The nucleus is in the center of this picture, not surprisingly. So this is not a hard question. Where's the electron density highest?
[Students speak over one another]
Professor Michael McBride:
In the middle, right? No big surprise there. Okay, how do you know? You take the wave function, you square it and find out where it has a maximum, and
e-distance
has a maximum when the distance is zero; the value is one. It falls off from there. Okay, so you just, to find where the density is highest, you just square the wave function and maximize it. Okay, now but here's a slightly different question: What is the most likely distance? Can you see why that's a different question than where — you might think the most likely distance is wherever the density is highest, but that's not quite true. Do you see why?
Student:
[Inaudible]
Professor Michael McBride:
Because what's most — yes?
Student:
It could be moving very quickly in the area.
Professor Michael McBride:
No, it doesn't have to do with motion. Yes Lucas?
Student:
There's almost no volume in the center.
Professor Michael McBride:
There's almost no volume in the center. If you take — say if you talk about a point, then there's no volume at all. Okay? But take a little box and put it in the center, or actually a sphere of a certain radius, a small radius, 0.0001 Å say, and put it in the center, and see how much density is inside. Okay? But then you could look at one angstrom out, and now you're looking at a little spherical shell that's 0.0001 Å thick. Is everybody clear? So there could be different directions in which you have this electron density, which is at that particular distance from the nucleus. And the further out you go, the more volume this shell has. It's always the same thickness, but as you move out there's more stuff in it. You see what I mean? More volume in it. What's it proportional to? As you increase
r
, how does the volume of the shell increase? How does the surface of the sphere increase as you go out?
Student:
r3
.
Professor Michael McBride:
No, volume is
r3
.
Student:
r2
.
Professor Michael McBride:
It goes with
r2
. The surface goes with
r2
. Right? So you have to multiply the probability density by
r2
, to see at what radius you have the most stuff. Is that clear to everyone? Because you want to count everything that's at that radius, not only in that direction but also in that direction, that direction, that direction, and so on, and the sphere gets bigger as you go out. So you'll notice that what's given in this plot here on the bottom right is
r2
times the wave function squared. Okay? So that'll tell you what's the most likely distance. Okay? So you have to do surface weighting by
r2
, and it's not at zero, it's at the unit that we use to measure distance in,
a0
, which turns out to be half an angstrom, 0.53 Å. Okay, now here's a
2s
orbital. Right? Here we'll draw two different shells of the same thickness, right? We'll number them one and two, and we're going to ask the question, which one has higher density? [Technical adjustments of room lighting] Okay, which shell has higher density, one or two?
Student:
One.
Professor Michael McBride:
One, clearly, okay? Now, here's a different question — okay, it shows one — which shell contains more electron density, more stuff? Which one has more probability?
Students:
Two.
Professor Michael McBride:
It's not obvious, because one has higher density but two is much bigger. Okay? And in fact, the two has about three times the radius of one. Right? So how much more volume does that shell have?
Student:
Nine times.
Professor Michael McBride:
About nine times more volume; not of the sphere but of the shell. Okay? So it's about nine times the volume. So it turns out that actually two has more stuff, and you see that in this plot. Right? The red for two is bigger than the green for one. Right? So depending on what question you ask, you have to decide whether you have to weight it by
r2
to get the answer you need. Okay, now here's another way of looking at a wave function. This happens to be the — it's actually a 3D wave function; as you see, not from here, but from here, it's 3D. This is the picture in three dimensions, using that ray tracing, the way we talk about. But you can do it, if you click "Slice" down here, then you get a slice through it. Okay? So that's 2-dimensional, more like the contour plots we've been using. It's just a slice through the 3D thing. So this is a 2D, not a projection, but an actual slice of it, and with this slider here you can control where the slice is. It's in the middle there; so it goes through the nucleus. But if you want, you can slide it down and see what the slice would be if it were in front of the screen that you sliced this picture. Everybody got it? So you can look at different levels that way, if you want to, or you can pretend you're looking at the whole thing. So it can be near or far.
Chapter 2. Scaling the Wave Function for Changing Nuclear Charge [00:14:07]
Okay, now let's look at these two different, the 2D and the 3D pictures, and look at the pattern of nodes, the shape and the energy of the
3d
orbital. You see here that there are diagonal nodes in this
3d
orbital. Okay? So that's
3d
. Let's look at this one. Now we still have those two diagonal nodes. In fact, it turns out that the nodes are actually cones. This is a slice through a cone, on the top, and on the bottom. Okay? So the nodal surface — bear in mind that in one dimension a node is a point; in two dimensions a node is a line; in three dimensions a node is a surface. Right? So we're slicing it and see an intersection of the conical surface here, but the actual node is a cone. Okay, but is that the only node that you see in that picture on the right?
Student:
There's a circular —
Professor Michael McBride:
Ah-ha, Angela says she sees a circle too. Right? So there are two kinds of nodes in this orbital. There's both a conical node, which we had in the previous one; the
3d
orbital had a conical node. That's what makes it a
d
orbital, having a conical node. But this one also has a spherical node, which is a circle when we slice it. Okay? So is this higher energy or lower energy than the one we looked at before?
Students:
Higher.
Professor Michael McBride:
How do you know it's higher?
Student:
Nodes.
Student:
More nodes.
Professor Michael McBride:
It has more nodes. Did you ever see a situation before where you can have two different kinds of nodes? Here you have both, in this section, both a circle and lines. You ever see anything like that before?
Student:
Chladni plates.
Professor Michael McBride:
Right. Anyhow it's higher energy, it's
4d
, not
3d
, as you said, and it's like this, right? You have both circular and diameter nodes, but this is three-dimensional so you have both sphere and cone. So can you guess what a
5d
orbital would look like? We looked at a
3d
orbital. This is a
4d
orbital. How about a
5d
orbital? Lucas?
Student:
It would have a third layer of nodes.
Professor Michael McBride:
Not a third layer of nodes. It would have how many more nodes?
Student:
One.
Professor Michael McBride:
One more node.
Student:
A circle, a sphere.
Professor Michael McBride:
And it would be — in the section it would be another circle; or actually it's another sphere of a different diameter. Okay? So you see how you can combine cones in this case — or it can be planes too; you have planes for
p
orbitals — you can combine spheres with planes, or cones, and you can combine them in different ways to get the same energy. For example, you can have a sphere and a cone that has a certain energy — that's
4d
, the one we're looking at here — or you could have two sets of — forget the sphere but have another cone. Does that remind you of anything? And get the same energy. Or you can have a plane and a cone, or you could have a sphere and a plane, or you can have a sphere and a cone — I said that already — or you could have two spheres, or you could have two planes. [Correction: a conical surface is in fact a double cone and counts as is equivalent to two spheres (
3d
≈
3s
) or a sphere and a plane (
3d
≈
3p
).] All those are two nodes — does everybody see what I'm saying — and they all have the same energy. Does that remind you of anything? It's not exactly the same, but it should remind you of something. That's what Chladni saw; remember, you could get different combinations, in his case, of circles and lines, and get the same frequency. Right? So that's why the
2s
and the
2p
have the same energy, or the
3s
, the
3p
and
3d
have the same energy. Okay, now let's talk about scaling — H-like. What do we mean by H-like?
Student:
One electron.
Professor Michael McBride:
It's one electron; any nuclear charge, but one electron. Why incidentally do we want it to be one electron? Zack?
Student:
Repulsion.
Professor Michael McBride:
That will turn out to be the case, but even if that weren't the case, there's a good reason to start with one electron. Yeah?
Student:
You get a Coulombic interaction between the electrons.
Professor Michael McBride:
Yeah, it's true that we don't want — well we'll get into big trouble when we get Coulomb interaction between electrons. It's absolutely right. But we want to walk before we try to run; work with three variables, not six variables, which you'd have with two electrons, or
3n
if you had
n
electrons. Right? So we want simple functions at the beginning. So that's what an H-like wave function is, just one electron, just three variables;
ρ
,
θ
,
φ
are the convenient ones. Okay, but now we want to see how we scale it as we change the nuclear charge. We already started talking about that last time when we talked about
ρ
, but we're going to talk about size, also about electron density, and also about energy and how the energies of these one-electron atoms change as you change the nuclear charge. Okay, this is what we talked about last time, that if you make the table up, the formulas, in
ρ
, instead of in
r
, then you could use it for any hydrogen-like atom, because the distance scale gets multiplied by the nuclear charge; that is to say, if you have a given
ρ
— that's a given size of the function we're talking about — a given
ρ
, then you have that value at shorter
r
, if you have a higher
Z
; a tradeoff between
Z
and
r
. If you double
Z
, you get the same value at half the
r
. Does that make sense, that as you get
Z
bigger, the distances get smaller? Does that make sense? Why?
[Students speak over one another]
Professor Michael McBride:
Because the nucleus pulls the electron in more. And notice that it's linear, right? If you double the nuclear charge, you shrink by a factor of two, in the distance. Okay? So increasing
Z
shrinks the wave function, makes
r
smaller for the same
ρ
; that is, the same height of the wave function, or the same position in the shape of the wave function, because you have to renormalize if you shrink the wave function. Okay, so let's compare hydrogen, carbon+6, and potassium+19. Right? So the distance scale will go 1, 1/6th, 1/19th. So this is what it looks like. If a hydrogen atom is that big, this is how big the carbon one-electron atom is, and that's how big the potassium one-electron is, 1/19th as the linear distance that's in hydrogen. Now, how much does the electron density change? I think that's the next thing; yeah, scaling electron density with
Z
. You can see that just from what we just talked about. If you shrink the distance by a factor of two, how much do you change the density? Factor of two, does the density get twice as high if you make the distance half as long? Ryan?
Student:
23.
Professor Michael McBride:
It's got to be 23, because you shrink it this way and this way and also this way. So it goes up with
Z
3, the density. That means if you have a hydrogen atom, the electrons are every which-a-way, all over, but if you have even a carbon atom, six times the nuclear charge for the same
1s
orbital, the density is 63 as big. What's 63? Thirty-six — ~forty five — over 200, right? So you have 200 times the electron density for the
1s
electron in carbon, compared to the
1s
electron in hydrogen. Where does that crop up in experiment — that you have so much higher electron density for carbon than you do for hydrogen — and other things are even more so, like potassium — where does it crop up? Yeah?
Student:
The contour plots.
Professor Michael McBride:
Of what?
Student:
Of the molecules, the bond lengths.
Professor Michael McBride:
What experiment?
Student:
I forget.
Professor Michael McBride:
Close. What?
Student:
I forget.
Professor Michael McBride:
You can do it by calculation and you'd see much higher density. That's what we're talking about is theory, but where do you see it experimentally? Lucas?
Student:
Refraction difference diagrams.
Professor Michael McBride:
Not to do — well you can do it in the difference, but if you look at the total electron density you don't see hydrogens, unless you look — work — really hard, because the density of electrons, which is what you're seeing, is so much higher for other atoms. Okay, so the normalization has to be one. So if you shrink it, and that's where that comes in. We talked about that
Z/ao
to the 3/2 that gets squared before, and so that the
Ψ2
is proportional to
Z3
, and the density of the
1s
electron, as you go across these atoms, goes from one to 216 to 7000; potassium is 7000 times higher. Remember where we saw that in X-ray, what a very dark atom that was. Okay, so it helps X-rays find heavier atoms more easily.
Now how about the kinetic energy? Right? So
Ψ
is a function of
r
, some kind of function of
r
, but it includes a
Z
;
Z
times
r
, because
ρ
is
Z
times
r
. So now, how does that influence the derivative, right? If you have a function of
Zr
, the derivative of it is Z times the function of Z, by the derivative of — oh what's it?; blah-blah. I got that wrong, or do I have it right?
Student:
That's right.
Professor Michael McBride:
That's right, yeah I got it right. Okay, now about how about the second derivative?
Student:
Z2
.
Professor Michael McBride:
It's going to have a
Z2
in it, right? So the curvature is going to be
Z2
times what the curvature was before, but the value of the wave function is the same at some — the corresponding ρ. So what's going to happen to the kinetic energy? If you have a bigger nuclear charge, what's going to happen to the kinetic energy at any point, at a corresponding point? Right? It's going to be proportional to
Z2
, the curvature divided by the value of the wave function. Right? So the kinetic energy is going to really zoom up for a hydrogen-like atom, when you get a heavier atom. Right?
Chapter 3. Scaling Energy with Respect to Nuclear Charge [00:21:20]
So let's summarize what we did so far. So distance will shrink according to
Z
, electron density will go up according to
Z3
, and the kinetic energy will go with
Z2
. Okay?
Now how about the potential energy, how will it change as we change the nuclear charge? Well if we change the nuclear charge; Coulomb's law includes the nuclear charge, right? So at the same distance you'll have
Z
times whatever it was for hydrogen, much higher, or indeed lower potential energy, more negative, further from zero. Okay, but at a fixed — that's — so at a fixed distance the potential energy will be proportional to
Z
; but the distance shrinks, right? So if you look at corresponding positions in the wave function, or you look at the average potential energy, it's going to go — it's going to also be, take into account that the distance gets smaller,
r
gets smaller, because the thing got shrunken by a factor of
Z
. So what happens to the average potential energy? How does it scale with
Z
? Maria, you got an idea? At a given distance, the energy, according to Coulomb's law, will be multiplied by
Z
, because you've got a bigger nuclear charge, but every distance gets shrunk by a factor of
Z
. Right? So if you average everything, what are you going to get? There are two factors of
Z
that are increasing (or decreasing, making more favorable) the energy, the potential energy. Got that? Two factors. So what's it going to be?
Student:
Z2
.
Professor Michael McBride:
Z2
, right? So the potential energy — what did the kinetic energy go with? Remember how the kinetic energy scaled?
Student:
Z2
.
Professor Michael McBride:
Z2
. How does the potential energy scale?
Student:
Z2
.
Professor Michael McBride:
How about the average potential energy, if I double the nuclear charge? How much lower is the — obviously if I increase the charge, the average energy of the electrons is going to get lower, but for two reasons, because the nuclear charge is bigger, and because the electron is twice as close. Okay? So how does it scale, the potential energy average?
Z2
. So the kinetic energy scales with
Z2
, the potential energy scales with
Z2
. How about the total energy? This is a hard one.
Student:
Z2.
Professor Michael McBride:
Z2
, right? Okay, so the potential energy goes as
Z2
, and the total energy, here's a big surprise, it goes with
Z2
too. It also happens to be
1/(n2)
. Right? So the energy gets — yeah, so as you go up in
n
, you get less stable, right? Now
R
turns out to be about 300 kilocalories/mole, if you want to really get what the energies are. And here is a plot of the energies. Here's the
1s
,
2s
or
2p
,
3s
or
3p
or
3d
,
4s
,
p
,
d
,
f
and so on, right? But the distance from zero, the amount of stabilization, is proportional to
1/(n2)
; and we saw the same thing if we did — in the one-dimensional Coulomb case, the energy was also
1/(n2)
. Okay. Notice it's independent of
l
and
m
;
3s
is the same as
3p
is the same as
3d
. Does that square with what you have learned before?
Student:
No.
Professor Michael McBride:
What did you learn before? Lexy, did you learn anything about that before, about the energies of
3s
,
3p
,
3d
? No. Anybody? Shai?
Student:
s
,
p
,
d
.
Professor Michael McBride:
Yes,
s
is lower than
p
is lower than
d
. Now how can both these things be true, that you heard something that was true, and I'm telling you they're all the same?
Student:
There are more electrons.
Professor Michael McBride:
Ah-ha! What you heard about was real atoms, things that have many electrons. I'm telling you about if the atom has only one electron, then
s
and
p
and
d
are the same. Okay? But it'll be different when you have many electrons, and we'll see why shortly. Okay, because this is one-electron atoms. Okay, so we've — this just summarizes — the size goes with
1/Z
, the electron density is proportional to
Z3
, and the energy goes with
Z2
, whether you're talking potential, kinetic or total energy. Okay, and it's also
1/n2
. And the size happens to be
n/Z
as well. Okay, now here's a really pretty one, and to do this, to see this right, you want to see the real thing. So notice that this is a
2p
orbital;
n
,
l
,
m
are 2,1,1. Everybody see that? I want to show you the real program that does that. [Technical adjustments to show
3d
orbital in
Atom-in-a-Box
program]
Chapter 4. Superposition, and the Orientation and Shape of Hybrid Orbitals [00:27:33]
Okay, now what I want for the display — this display is just as if electrons were all white, okay? But we want to color them according to the color of the — [Technical Adjustments of
Atom-in-a-Box
format] — we want to color them with the phase, plus, minus. That's
3d
. The phase keeps changing. That has to do with time dependence, which we're not talking about. Okay? Now, that's a
3d
orbital. We want to have — what did we have before? We had
2p
, right? So I'll make this instead of a three, a two. So there's a
2p
orbital, a particular
2p
orbital, 2,1,0. Which one is that? Notice you have a coordinate system next door there, and I can rotate this thing, I can grab it and rotate it; the coordinate system rotates. See that?
Student:
Cool!
Professor Michael McBride:
So I can look at it end-on if I want to, or look at it from the side. Which
p
orbital is that?
Students:
2pz
.
Professor Michael McBride:
How do you know?
[Students speak over one another]
Professor Michael McBride:
Points along the
z
axis. Okay? Now, let's look at another
2p
orbital, because we can make
m
one instead of zero. So the 2,1,0 is
2pz
. Now what's 2,1,1? Let me look at it this way. That's time-dependence, right, and that's weird. And physicists love this sort of thing, because they deal with atoms in isolation, and atoms in isolation have angular momentum, things going around. But atoms, when they're in molecules, when they're with other atoms, or in other things that distort it, like in an electric field, they don't behave that way. So chemists use a different way of doing it, right? It's not that physicists are right and chemists are wrong, or that chemists are right and physicists are wrong, it's if you're dealing with isolated atoms, you use one thing; if you're dealing with atoms interacting with other atoms you should use something else. And the way you do this, dealing with something else — I'll show you here. You do what's called superposition; that is, you add two functions in order to get a new function, and the two functions I'm going to add, when I click "Superposition" here, are 2,1,1, and the other one I'm going to use is 2,1,-1. And now what's that?
Students:
2py
.
Professor Michael McBride:
That's the
2py
orbital. Okay, does everybody see what I did? So I can combine two of the physicist's orbitals to get the chemist's
2py
orbital. Dean Dauger, who wrote this, is a physicist, so he writes physicist programs, right? But we can trick it to be chemistry by adding two of his together, or by subtracting them; and when you subtract them you have to put an
i
in — imaginary. So I'm not going to do it right now. You can do it yourself. You can see down here, you can do the phase and so on; the phase of
p
makes it imaginary. I won't do that now. We'll go back to the PowerPoint. [Technical Adjustment to change program] So superposition of that kind, when you add two functions together to get a new function, for whatever purpose, is a kind of what's called hybridization. Now there are other kinds of — have you heard about hybrid orbitals? Right. What that is is adding two orbitals together to get a new orbital. And let's look about when that would be. As we said, this is the physicist's
2p
,
m=1
, with orbital angular momentum, and it has complex numbers involved. And the chemist's
2p
is that sum. Okay.
Now multiplying and adding wave functions. We've already seen a case where you multiply functions. Do you remember where we've seen things be multiplied?
[Students speak over one another]
Professor Michael McBride:
Alison, do you remember? No.
Student:
You multiplied the wave functions.
Professor Michael McBride:
Multiplied which wave functions? Let me tell you one place we already multiplied was squaring a wave function is a kind of multiplication to get probability. But I want a different one.
Student:
When we, for different variables —
Professor Michael McBride:
Ah, for separating the variables,
r
,
θ
and
φ
; we had an
R
function, a
Θ
function, a
Φ
function, and we multiplied these pieces together to get the total wave function for the electron, the three-dimensional wave function. So that's one place you multiply, to get a one-electron wave function, which is — we call an orbital.
An orbital is a one-electron wave function
; that's what an orbital is. Now, you can add orbitals to create a hybrid orbital; that's what we just did, we took two physicist's orbitals, added them together, and got a new orbital. Okay?
2py
+
2pz
is a hybrid orbital. An orbital is a one-electron wave function. What's it a function of? What variables do you put in, in order to get a value out? How many variables? Sophie?
Student:
Three.
Professor Michael McBride:
Three. What are they?
Student:
Those.
Professor Michael McBride:
The position of that electron, the one electron. If it's a one-electron orbital, you can write the orbital as many pieces — here are two pieces, right? But it still is a function of just the position of one electron; it's not a function of six, or eighteen, or whatever number of variables, it's just a function of — it's an orbital, a one-electron function, so it's a position of one electron that you plug in. Now, you can change orientation of orbitals by hybridization. Let's look at that. So here's the
2pz
orbital. I've rotated the coordinate system so
z
is horizontal. Okay? And here's the
2py
orbital, which we already made by adding two physicist's orbitals together. Okay? Now what happens — and notice the
2py
, surprise, is pointed along the
y
axis,
2pz
was pointed along the
z
axis. What if I add the two together? What if I add
2pz
and
2py
? Now let's go back and look at
2pz
a second. Notice it's red on the left, blue on the right; say positive numbers on the left, negative numbers on the right — everybody with me? — because it assigns numbers to different points in space, positive numbers on the left, negative on the right, let's say. Now this one assigns positive numbers on the top, negative numbers on the bottom. Suppose I add together, what am I going to get? Andrew?
Student:
You get diagonal.
Professor Michael McBride:
Ah, they should reinforce in the top left where they're both positive, and in the bottom right where they're both negative, but in the bottom left and the top right they should cancel. Okay? So if we add them together to make a weighted sum — we don't have to add them 50:50, but we'll start by adding 50:50. Okay? So if we add them, a 50:50 mixture will give that, just what you said. Okay, so we changed the orientation of the
p
orbital by adding two. Okay, now suppose we didn't use 50%, suppose we used another mixture, suppose we used 75%, right? Or there's 50%, or 25%. Okay? So you can get any orientation you want by mixing — within that plane, within the
yz
plane, by adjusting the ratio. Okay, there's
2py
.
Now, what would happen with a
2s
orbital if you put it in an electric field? You're changing the rules, you're changing the potential, because now the electron has — doesn't just — its energy doesn't depend just on its distance from the nucleus, it also depends on where it is in the field. So we're changing the definition of the potential energy. So it's a different quantum mechanical problem. But I don't want you to think about quantum mechanics, I just want you to think about what would happen if you put an electric field on. What do you think?
Student:
It shouldn't —
Professor Michael McBride:
Would it move the atom?
Student:
Yes.
Professor Michael McBride:
No, because the atom is neutral, overall. We'll do a hydrogen atom here. The atom's neutral, so it won't move. But what will happen?
[Students speak over one another]
Professor Michael McBride:
The electrons will move one way and the nucleus will move the other, and if you've preserved the center of mass, then the nucleus will hardly move at all, and the electrons will do most of the moving. Okay. So you can change the shape by hybridization. We can get something that will work in an electric field, describe an atom in an electric field, by mixing the ones without electric field. Now let's look how we do that. We make an
spn
hybrid orbital. Have you ever seen that?;
n
is a number. Can you give me an example? two,
sp2
or?
Student:
sp3
.
Professor Michael McBride:
sp3
or
sp
, where
n
is one, right? Or
sp0
. Have you ever seen that?
Student:
No.
Professor Michael McBride:
sp0
is just
s
. This is how much
p
there is in it, after you square it. That is, it's a weighted sum, this thing you're using. You have different values of
a
and
b
, and it's weighted such that — so when you square it, you get
a2
, a fraction of
2s squared
; that's the distribution
2s
would have;
b2
of the way
py
would be when squared. But you also get a cross-term,
2ab
times
2s
times
2p
. Okay, now so
n
, the number you put in to talk about
sp2
,
sp3
and so on, is the square of
b2/a2
. So if you have an
sp
hybrid, it means equal parts of
s
and
p
, and if you have
sp3
, it means three times as much
p
as
s
, after squaring. Okay, so it's what fraction you have of something that looks like
2s
squared and
2p
squared;and then there's also that part. Okay, so now let's just look at some examples here. Suppose
n
is zero; then you have just pure
s
. Okay? Now suppose you put an electric field that wants to shift the electrons. It would push a positive charge to the right but it will push electrons to the left. Okay, so let's — here we went to 0.02, just a tiny amount of
p
. But see how it — here's back to
s
, and there's
sp0.02
. It shifted the electrons to the left. What if I go to a higher value? 0.04, 0.06, 0.09, 0.11, 0.18, 0.25, 0.33. So what I'm doing is turning up a dial to make the electron — electric field stronger — and the electron is shifting, by changing the hybridization. Okay, 0.5, 1. There's an
sp
hybrid. Now what'll happen if I keep on going, make it
sp2
, for example. What do you think will happen? Guess.
Student:
It'll get more and more to the right.
Professor Michael McBride:
It'll keep going to the right. Wrong! Watch this. That's the maximum extension is
sp
. That's the most you can extend. Now watch what happens if I make it bigger;
sp2
,
sp3
,
sp4
,
sp9
,
sp24
, pure
p
. Right? Because both pure
s
and pure
p
are symmetrical. The 50:50 mixture is the one that shifts the most to the left.
Chapter 5. An Inconvenient Truth: Troubles Describing Multi-Electron Systems [00:40:44]
Okay, now we're going to close here with trying to go beyond what we've already seen. What we've seen is one-electron atoms, hydrogen-like atoms. So we find that we can multiply pieces,
R
,
Θ
,
Φ
, to create this one-electron wave function, the orbital, and we can furthermore add these things to make hybrids that shift things around in useful ways. We can add orbitals to make an
sp
hybrid, for example, as what would happen in an electric field. But it's still an orbital, so it allows adjusting to new situations — for example, an electric field — while preserving the virtues of real solutions of the nuclear potential, because you never put on a field as strong as the field felt by the electron near a nucleus. Adding the external field by turning up your dial is just a small change. So you want things to look pretty much like what they looked originally, with the nucleus, just a little change, and you can do that by hybridization. Okay, the big deal is the nuclear potential at small distances.
Now, let's try to go to a two-electron wave function. Okay? So what's it a function of? What's a two-electron wave function going to be a function of, how many variables?
Students:
Six.
Professor Michael McBride:
Right, six, right?
x
,
y
,
z
for one electron, and
x
,
y
,
z
for the other electron, or
r
,
θ
,
φ
of electron one, and
r
,
θ
,
φ
of electron two, and they're on the same nucleus, so you measure the distances from the same point, but they're two different distances, one to electron one, another to electron two. They could be the same, but they don't need to be, they could be different. Okay? Now wouldn't it be neat — that's the question mark — if we could get that by multiplying two one-electron wave functions? Because we have one-electron wave functions cold; we look in the table and we've got the exact thing. If we could take two of those and multiply them together, so orbital A for electron one times orbital B for electron two — remember, what these things are is just numbers. If you put in some value of position of electron one and some value of position of electron two, this first thing will give you a number, the second thing will give you a number. If you could multiply those two numbers together and get the number for the total wave function, that would be really great, because then you'd know how to do it. The question is, can you do that? Remember, an orbital is a one-electron wave function. So can we multiply orbitals in order to get a many-electron wave function? If we could — and then, of course, we would square it to get probability density. Now it would be a different probability. In the first case it was probability of electron one being here. Now it's the joint probability of electron one is here, and electron two at the same time is here; that's the probability when you have six variables. Okay? Wouldn't that be great? It's just paradise, right?
Because if we had many electrons we could just multiply all those orbitals together, a certain orbital for electron one, another orbital for electron two, another one for electron three. We know how to write those; multiply them together, we get the thing. We find the total energy is whatever energy electron one had, plus whatever energy electron two had. That's great. We find the total electron density. We know how to find the electron density of each individual electron. So the total electron density should be just the sum of those. So if we were interested in the total electron density at this particular point, we'd see what the electron density of electron one is at that point, and what the electron density of electron two is at that point, and we'd add them together and that would give the total electron density, at that point. So the total electron density is a function of
x, y, z
. It's whatever this is, evaluated at
x
,
y
,
z
, plus whatever this, plus all the others. Absolutely wonderful. Right? And then you could write things. So the whole is the sum of the parts. Right? And you could write things like this at the top, that Neon has the configuration: two electrons in
1s
, two electrons in
2s
, two electrons in
2px
,
2py
. Right? Things like that. You've seen things like that. So those are the orbitals in which electrons are, to describe the neon atom. Right? Now, this is a problem in joint probability. So it's like tossing two coins to try to get to two heads. So I don't know if I can do these at the same time, but I have two quarters here. Need your back of your hand. Okay, so I got tails. What did you get?
Student:
Heads.
Professor Michael McBride:
How often?
Student:
Half the time.
Professor Michael McBride:
Half the time. Actually if I get tails and you get heads, that's a quarter of the time.
Student:
Yes, that's a quarter of the time.
Professor Michael McBride:
But a quarter of the time you'll get tails and I'll get heads. So heads/tails is half the time. How about heads/heads, how often?
Student:
Heads/heads. Still a quarter.
Professor Michael McBride:
A quarter of the time. Now I'll bet you, I'll bet you that I can get head/head half the time, actually doing the experiment.
Student:
Yes.
Professor Michael McBride:
You want to take the bet? I would advise against it.
[Laughter]
Student:
I won't take it then.
Professor Michael McBride:
Okay, here's what I'm going to do. Okay?
[Professor McBride tapes the quarters together]
Professor Michael McBride:
Two tails, I lose.
[Laughter]
Professor Michael McBride:
Whoops.
[Laughter]
Professor Michael McBride:
Two tails, I lost again. But I think you can see that if I do it a lot of times I'm going to win half the time. Why? Why was the rule wrong?
Student:
They're not independent.
Professor Michael McBride:
Because they weren't independent, right? If they're independent, the probability of both A and B, that is, the probability that A will be here and at the same time B will be here, is the product of the probabilities; but if you do this, that's not true anymore. Right? So if you have a two-electron wave function, you square it to get the joint probability, that electron one will be here and electron two will be here at the same time. So is that valid, to multiply — here I'm multiplying the individual probabilities that electron A is at a certain position, electron B is at another position. Do I get the joint probability that way? Well under what conditions do I get the joint probability that way?
Students:
If they're independent.
Professor Michael McBride:
If they're independent. Now, here's the big question. Are they independent?
Students:
No.
Professor Michael McBride:
Why not?
[Students speak over one another]
Professor Michael McBride:
Because of Coulomb's law, they repel one another. There's no way they can be independent, they repel one another. So orbitals, one-electron wave functions, to express many-electron wave functions, cannot be right. Orbitals are a fiction, except for one-electron problems. Right? hydrogen-like atoms fine; we've got hydrogen atoms cold. But if you got more than one electron, orbitals won't work. But still we're going to use them.
[Laughter]
Professor Michael McBride:
Right? And that's what you're going to find out after the exam. Okay, good luck on — so that doesn't work — good luck on the exam.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall08/chem125/mp3/chem125_10_092408.mp3) |
