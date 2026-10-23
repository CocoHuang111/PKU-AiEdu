- Source: https://oyc.yale.edu/physics/phys-201/lecture-14
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 14 - Maxwell's Equations and Electromagnetic Waves I

### Overview

Waves on a string are reviewed and the general solution to the wave equation is described. Maxwell's equations in their final form are written down and then considered in free space, away from charges and currents. It is shown how to verify that a given set of fields obeys Maxwell's equations by considering them on infinitesimal cubes and loops. A simple form of the solutions is assumed and the parameters therein fitted using Maxwell's equations. The wave equation follows, along with the wave speed equal to that of light (3 x 10^8), suggesting (correctly) that light is an electromagnetic wave. The vector relationship between the electric field, the magnetic field and the direction of wave propagation is described.

### Lecture Chapters

1. Background
2. Review of Wave Equation
3. Maxwell's Equations
4. Light as an Electromagnetic Wave

1. 0
2. 283
3. 1203
4. 3408

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics II
PHYS 201 - Lecture 14 - Maxwell's Equations and Electromagnetic Waves I
Chapter 1: Background [00:00:00]
Professor Ramamurti Shankar:
Before we start today's lecture, I just wanted to explain to you that at the end of the class, I have to run out and catch a plane. So if you have to discuss any other administrative matters, you should do it now, because you won't find me after class. I couldn't take this weather. You know where I'm going? Seattle. That's the story of my life. So nothing else? Yes?
Student:
Is there going to be an equation sheet for the midterm and if so, is it possible to get it?
Professor Ramamurti Shankar:
You will get the equation sheet. Do you want it now? No. With the exam? Yeah. I don't give it out before, but you will have all the reasonable equations on that sheet. You know the reason for that, right? The reason is that some of you may be going into medicine and you control the anesthesia on me, one of these days in the future. If I held back the equation sheet, I know you will hold back the painkillers. It's just making a deal, the way things are done nowadays. I made a deal with you guys. I couldn't sleep last night, because today is when we're going to solve Maxwell's equations and get the waves. I just couldn't wait to get to work. It's great. No matter how many times I talk about it, I just find it so amazing.
So here are these great Maxwell equations. I'm going to write them down. Those are the equations. The first one tells you that if you draw any surface and integrate
B
over that surface, namely, you're counting the net number of lines coming out, you're going to get 0. That's because lines begin and end with charges and there are no magnetic charges. If you look at any magnetic field problem, the lines don't have a beginning or an end. They end on themselves. So if you put any surface there, whatever goes in has to come out. That's the statement of no magnetic charges. This one says, yes, there are things that manufacture electric field lines called charges. They make them and they eat them. Depending on how many got in the volume, the net will decide the flux out of that volume. This one, without that, used to say electric field is a conservative field. It defines a potential and so on. But then we found in the time dependent problem,
E⋅dl
, we said rate of change of the magnetic field. So changing magnetic field sustains an electric field. And this one says a changing electric field can produce a magnetic field. In addition, a current can also produce a magnetic field.
This is what we have to begin with. Now I'm going to eventually focus on free space. Free space means we're nowhere near charges and currents. And the equations become more symmetric. This has got no surface integral, that has got no surface integral. The line integral of this guy is essentially the rate of change of flux of that. And the line integral of that guy is - the rate of change of flux of this. If I'm going to get a wave equation, the triumphant moment is when I do this and do that and out comes the wave equation. But if at that moment you have not seen the wave equation, you're not going to get the thrill. So I have to know, how many people remember the wave equation from the first part of the course? Okay, so I think I have to remind you of what that is. It's a bit like explaining a joke, but still, I have to do that, because otherwise we won't have that climactic moment.
Chapter 2: Review of Wave Equation [00:04:43]
So let me tell you one example of a wave equation. People have seen them before. Here is the simplest example. You take a string, you tie it between two fixed points and it has a tension
T
. Tension is the force with which the two ends are being pulled. Then you distort it in some form and you release it, and you see what happens. Now let's measure
x
as the distance from the left end and
y
as the height at that time
t
. The wave equation tells you an equation governing the behavior of
y
. It tells you how
y
varies. Now if you want to do that, you may think you have to invent new stuff, but you don't. Everything comes from Newton's laws. That's to me the amazing part, that you have these equations, then of course the Lorentz force equations. Then you've got Newton's laws and that's all we have up to this point in the course. So there should be no need to invoke anything beyond Newton's laws to find out the fate of this string. And namely, we are going to apply
F = ma
, but not to the whole string at one time, because
a
is the acceleration and whose acceleration are we talking about? Piece of string here, piece of string there? It can all be moving at different rates.
So you pick a tiny portion, which I'm going to blow up for your benefit. That's a piece of string. Its interval, it lies under region of length
dx
. In other words, you take a
dx
here and look at that string. It is being pulled like that with a tension
T
and it's being pulled like this with a tension
T
here. That's the meaning of tension, pulled at both ends. If this was a perfectly straight segment, there'll be no net force on it, because these forces will cancel. But if it's slightly curved, then this line and that line are not quite in the same direction and the forces don't have to cancel. So let's take that force and write its vertical part. If this angle is
θ
,
T
times sin
θ
is the force here. -
T
times (because
T
is pointing the opposite way) — let me call this
θ1
and
θ2
is the angle you have here. Do you understand? The vertical force is restoring the strength to where it was is what I'm focused on. So you resolve that force into a vertical part, up and this one has the vertical part down. Now if
θ1 = θ2
they cancel and that's what I just said. But
θ1
and
θ2
are generally not equal, because if I go to the top of the string, for example, this end is pulling this way, that end is pulling that way. There's a net force down. So you have a net force because this angle or the tangent to the string is changing with position.
That's why they don't cancel. Now the approximation I'm going to make is that theta is small, measured in radians, and I remind you that sin
θ
is essentially
θ
- very small corrections. And cosine
θ
is 1 −
θ2
/2 + corrections. And tan
θ
, which is the ratio of these guys, is
θ
+ other corrections. For a very small
θ
, you forget that, you forget that. You keep things of order theta in every equation. So for small angles, cosine is just 1, and sin
θ
is
θ
. If you do that, and sin
θ
and tan
θ
being equal, I can write it as tan
θ1
- tan
θ2
. But that's in the approximation, where tan and sine are all roughly equal. That is really
T
times
dy/dx
at the point
x + dx
−
dy/dx
at the point
x
. Are you with me?
dy/dx
from calculus, you remember, is the slope. It's a partial derivative. Why is it a partial derivative now? Can you tell me? Yes?
Student:
It's all dependent on time.
Professor Ramamurti Shankar:
It can depend on time and I'm doing
F = ma
at one instant in time. So I don't want to take this guy's slope now and that guy's slope an hour later. I want them at the same time, at a fixed time. Now what do I do with this? Have I taught you guys how to handle a difference like this? There's one legacy I want to leave behind is what to do when confronted with a difference like this. You have any idea what to do? Pardon me?
Student:
Multiply by one.
Professor Ramamurti Shankar:
Multiply by one. Then what do you do with that? I'm asking you to evaluate the difference between this guy at
x + dx
- the same thing at
x
. What is it equal to approximately for small
dx
? Let me ask you another question. Suppose I have
f
of
x + dx
and I subtract from it
f
of
x
, what is it equal to?
Student:
[inaudible]
Professor Ramamurti Shankar:
If I divide by
Δx
and take the limit, it becomes a derivative. If I don't divide by
Δx
, this is then
df/dx
times
Δx
. There may be other corrections, but when
Δx
goes to 0, you may make that approximation. That is the meaning of the rate of change. If I tell you, here's a function and that's the same function somewhere to the right, what's the difference? That's what the role of the derivative is, to tell you how much it changes. This slope changes from here to there, therefore it's a derivative of something which is already a derivative, so it's
d2y/dx2
times
Δx
. In other words, the f I'm using here is itself
dy/dx
and the
df/dx
is then the second derivative. So that's the force. Now that force we must equate to ma. That's the easy part.
What is the mass of this section, this portion of string? If the mass per unit length is μ, that's the mass of that section. Then what's the acceleration. Acceleration is the rate at which y is going up and down. That is
d2y/dt2
. Canceling the Δx, we get this wave equation which says
d2y/dx2
μ
over T
d2y/dt2
is 0, and that's the origin of the wave equation. Any time you get something like this, you call it the wave equation. I'm going to write this as
d2y/dx2
- 1 over v2
d2y/dt2
= 0 where v is √(
T/μ
). I use the symbol
v
, because this will turn out to be the velocity of waves on that string. Namely, if you pluck the string and make a little bump here, let it go, the bump will move and v is going to be the speed at which it moves. The speed of waves is determined by the tension and the mass per unit length.
Now I want to show you that this really is the velocity of the wave. How do we know that's the velocity? It's got dimensions of velocity, but maybe it's not the velocity of this wave. Maybe it's something else. I want to show you that
v
stands for the velocity of the waves in this medium. The way you do that is you ask yourself, what is the nature of the solutions to this equation? If
y(x,t)
satisfied the equation, what can you say about its functional form? What functions do you think will play a role? Does anybody have any idea what kind of functions may play a role?
Student:
Sine function?
Professor Ramamurti Shankar:
Sines maybe. With single oscillators, when you have something something is
d/dt
squared, you had cosine
ωt
. Whatever you can do for
t
you can do for
x
. You can have a cosine in
x
. So you might think it is all sines and cosines and exponentials. All that is true, but it turns out the range of solutions is much bigger than that. I'm going to write down for you the most generation solution to the wave equation, namely what's the constraint it imposes on the function? The answer is this:
y
can be any function you want of
x - vt
. I don't care what function it is. So if I call
z
as a single variable
x - vt
,
y
can be a function of this single combination,
x - vt
. In other words,
y
can depend on
x
and
y
can depend on
t.
If it depends on
x
and
t
in an arbitrary way, of course it won't satisfy this equation. But I'm telling you that if it depends on
x
and
t
only through this combination,
x - vt
, it will satisfy the wave equation. In other words, here's the function. You don't even have to think,
x - vt
squared over some number
x02
.
That's a completely good solution to the wave equation. I guarantee if you took this, it would satisfy the wave equation, because it's a function only of x - vt. A function that's not a good function is
y = e −x2 − v2t2
. That's not a function of
x - vt
. That won't satisfy the wave equation. So why is that true is what I want to show you. Let us take
dy/dx
. Remember,
y
depends only on this combination
z
, therefore it equals
df/dz
times
dz/dx
. But
z
is
x - vt
,
dz/dx
is 1, so it's just
df/dz
. Now let me rush through this and do it one more time. Everything will go the same way. You will get this. But how about
dy/dt
? If you want
dy/dt
, again you take
df/dz
times
dz/dt
. But that gives you — this should be written as a partial–
dz/dt
is
df/dz
times -
v
. Can you see that? By the chain rule, you take any function you have, first differentiate with respect to
z
. Then differentiate
z
with respect to
x
and with respect to
t
. If you do an
x
derivative, you get 1. If you do a
t
derivative, you get -
v
.
Now if I do it twice — again, I don't want to spend too much time — if I do it twice, I'm going to skip the intermediate step. I'll get a -
v
and a −
v2
. It follows then that if I took 1/
v2
times that, can you see that now? 1/
v2 d2y/dt2
is the same as
v2y dx2
. Therefore to satisfy the wave equation, it can be any function at all, as long as it depends on
x
and
t
in the combination
x - vt
. That is just a mathematical fact. You just have to do the chain rule, you will find that it's true. But more importantly, I want you to understand what it tells you about the wave propagation. Let me pick
x0
= 1 for convenience. Let me plot this guy at time
t
= 0. This solution looks like
e
to the -
x
squared, which is a function like that, at
t
= 0. What does it look like at
t
= 1 second?
Think about it.
t
= 1 second looks like
e
to the -
x - v
whole squared. That means it's the same bump, shifted by an amount
v
. See this function
x - v
squared behaves with respect to
x = v
the same as the original function around
x
= 0. Whatever happens to this guy here happens to that guy at distance
v
to the right. You can see that if you wait
t
seconds, it would have moved a distance
vt
. That's why you understand that
vt
,
v
is the velocity of propagation, because what this is telling you is that if you start the system out with some configuration at time
t
,
t
= 0, later on the function looks like the same function translated to the right at a velocity
v
. That means its profile, whatever profile you have, is just moved to the right. Now can you think of another family of solutions besides this one? Why should the wave move to the right? Yes?
Student:
It's
x + vt
.
Professor Ramamurti Shankar:
Do you understand that if it was
x + vt
, you go through this derivation, you'd get a +
v2
instead of a −
v2
and that doesn't matter. So the answer is, the most general solution to the wave equation is any function you like of
x - vt
+ any function you like of
x + vt
. This will describe waves going to the right; that will describe waves going to the left, and you can superpose them. Because it's a linear equation, you can add solutions. This is what I want you to know about the wave equation. This is one example of how the wave equation comes and what the meaning of the symbol v is.
Chapter 3: Maxwell's Equations [00:20:03]
Now let me go to the old Maxwell equations. Now I want to do them and ask myself. I'm going to write down a solution and I'm going to see if it obeys these four Maxwell equations. If I write down a solution for the electric field and the magnetic field, they have to obey all those conditions, those four equations. That means, let's take first the case of working in a vacuum, when there is no current, when there is no charge. So you want a surface integral of
E
on any surface to be 0 and the surface integral of
B
on any surface to be 0. Look at the surface integral first. Do you understand?
This was never going to be non-zero. This will be non-zero near matter but we are far from any charges, so there is nothing to enclose in the volume. There are no charges there. Look at those equations. I give you a function and I say, "Tell me if it satisfies Maxwell's equations," what do you have to do? Operationally, what is it that you have to do? Any ideas on what you must do at this point to test? Any ideas? What do you have to see of a potential solution? Come on, this is not the New York subway. You can make eye contact. What is this? You have no idea what you may have to do? What if I give you a function and say, "See if it satisfies the wave equation," what will you do then? Take the function and then what? Yes?
Student:
Differentiate it and see —
Professor Ramamurti Shankar:
Yes! Take
x
derivative,
y
derivative and all that, second derivative. If it vanishes, you'll say it satisfies it, right? That's what it means to satisfy it. If I give you fields
E
and
B
that depends on space and time and I want you to verify if it satisfies this, what do you have to do, is what I'm asking?
Student:
Come up with a situation?
Professor Ramamurti Shankar:
No, it must be true in every situation. In other words, what's the surface on which this integral is done? On what surface do we do the integral? Pardon me?
Student:
Closed.
Professor Ramamurti Shankar:
Closed. But beyond closed, anything else? Where is it located? How big is it? Pardon me?
Student:
[inaudible]
Professor Ramamurti Shankar:
I didn't hear that.
Student:
It's everywhere.
Professor Ramamurti Shankar:
It could be anywhere and it could have any size. It could have any shape. And it must be true for all those surfaces. So if I just give you a field,
E
(
x,y,z
and
t
), it's a lot of work, right? Draw all possible surfaces. On them, you can take the surface, divide it into patches, do the surface integral patch by patch, and you better keep getting 0. When you're done with that, then you take the magnetic field. Then the other two Maxwells tell you, take a loop, any loop, go round that and do the line integral of
B
. That should be the flux crossing it, the electric flux or magnetic flux. And it should be done for every loop and for every surface. You realize that looks impossible. But there is a quicker way to verify all of these equations, and the quick way is the following: if these equations are true for a tiny loop, in this case, true for a tiny volume or a tiny surface enclosing a tiny volume, then it's true for big ones. And likewise, if true for a tiny loop, it is true for any arbitrary loop. In other words, if I can show that at any arbitrary point, if I pick an infinitesimal loop or infinitesimal surface, and these guys satisfy these equations on an infinitesimal thing, it's going to satisfy it on a macroscopic thing.
That's what we want to understand. How does that come about? It comes about due to a very beautiful way in which we define the sum of two surfaces. So here is a surface. I'm going to take everything to be a cube, but it's not important. Here's a surface. Let's call it
S1
. And it's got its outward normal. That's the definition of surface integral is you draw the normals pointing outwards and you take
E⋅dA
on every face of the cube and add it. The area vector is defined to be outward pointing normal to every face. So you take the little cube.
E
may be pointing this way there or that way there, but you take the dot product of the area and you add them. Then I take a second cube here. Let's see. It's got its own outward normal. This is surface 2. Now imagine gluing this guy to this guy, so it looks like this. You glue this common face. Bring that surface over and glue them with that face common to both. Then I claim that the surface integral on this one + the surface integral on that one is the surface integral on the union of the two. In other words, let's see, take one cube, take another cube, and that surface integral will be the same as on a longer object. I don't know what this is called, something over that. The two cubes used to be sharing this. Do you understand why?
Let's understand why the integral on this guy, which is, if you want, two cubes joined to form a rectangular solid. That surface integral is the sum of these two surface integrals. Think for a minute about why that is true. If you compare them, piece by piece, this face matches that face. This face matches that half. This one matches that half. But something is missing in this that's present here, do you agree? What is it we don't have? What's missing in the equal union? Yes?
Student:
Two sides equal _________.
Professor Ramamurti Shankar:
The two common faces are missing in the big surface, but it does not matter. The two common faces do not matter because when you do the surface on the first one, the outward normal will point out of that, whereas if you do it on the second one, the outward normal will point into the other one. When you glue them together, the common face is opposite orientations. Consequently, the surface integral on the big solid is equal to the sum of the surface in integrals in the two small solids. Do you follow that? That's the way it works. Then you can go on adding more and more pieces to this, right, and you can build like Legos and arbitrarily complicated blob. Remember, these are all very, very tiny volumes, so you can build them up to look like a big thing. It may look like a pyramid. If you look very closely, you'll have the steps like in a real pyramid, but the steps here can be made arbitrarily small. Therefore if the surface integral was 0 on every little piece that made up the big object, then it's going to be 0 on the big object, because the integral on the big object is the integral of the tiny pieces that make up the big object.
This is a very profound idea, because the big object has fewer surfaces than the small ones, because when you cut it, you create two new surfaces, but they don't contribute between the two of them, because they cancel. And in particular, if the surface integral had not been 0, but because of matter it was equal to charge inside volume 1, and this right hand side of this one was the charge inside volume 2, you can see that the surface integral on the bigger surface will be the sum of the two charges. So anything you're trying to prove about surface integrals, even if the right hand side is not 0, if it is true in a tiny cube, true in a union of two cubes and then in a union of any number of these tiny guys, therefore on any surface. That's the thing to remember. What we will do then is not to take arbitrary surfaces, but infinitesimal surfaces and we'll prove for them that the Maxwell equations are satisfied for the solution that I come up with. Then you're guaranteed that it will work for an arbitrary surface.
When you do line integrals — this is for surface integral — line integral is even easier. Suppose I'm taking the line integral of some function around this loop. This is loop
L1
. I take a line integral of some field on L1. Then somebody wants to do a line integral on
L2
that looks like this,
E⋅dl
on line 2.
You agree that this + that really is the same as the line integral on the union of the two loops where you delete the common edge. You have to understand this. I will not leave any child behind. You have to know why this is true. I'm taking a lot of time so you know where it's coming from. If you compare an integral of any field on the big rectangle compared to the two squares, the only difference is that the two squares had these two sides, but they were doing them in opposite directions, so it does not matter. So if the line integral of this, for example, was some flux coming out of this one, and the line integral of that was the rate of change of flux coming out of that one, if it was true, then it's guaranteed that the line integral on the big rectangle will be the sum of the fluxes or the rate of the change of fluxes coming out of both. So any Maxwell equation, if it's true for a tiny square, infinitesimal square, will be also true for anything bigger. There's only one subtlety when you do loops and that's the following: if you're living in a plane, you can prove the result for the plane in the plane of the blackboard, because there no loop I cannot form by joining these guys.
But we live in three dimensions so that we may have a loop like this, floating in three dimensions. Then what you have to do is, you've got to find any surface with a loop as a boundary, maybe this dome. Then the integral on — let me hide this for you. This is the part behind; this is the part you can see. That's the same as tiling it into little squares and doing an integral on each one of them like this. You have a dome of some big building, you take little tiles and you tile the building. Then all the interior edges cancel, and all that remains is the edge that is the edge of the original surface. So even in 3D it's going to work, but now you should be ready for loops that are not lying in the
xy
plane. So you will have to prove it for the three independent loops. You will have to prove it for an infinitesimal loop in that plane, infinitesimal in that plane, infinitesimal in that plane. If it's true for three independent directions, then by combining those little pieces, you can make yourself any surface you want.
In other words, I'm saying, given a rim, you can build any surface with the rim as the boundary. If you can take the little flat pieces in any orientation, and it's enough to have them in the
xy, yz
, and
zx
planes. So the strategy that I'm going to follow, this is something one can skip, but I wanted you to know the details, if you really want to know where everything comes from. I'm going to write down or search for a solution to Maxwell equations. I'm going to make it have a certain form. You remember how we do this with equations. We assume a certain form, stick it into the equation, play with some parameters till it works. I'm going to make it work on infinitesimal loops and infinitesimal cubes and that's going to be enough, because if it works on this tiny loop, it works in a big loop, works in a tiny cube, works on a big cube or arbitrary surface.
So let us write down the functional form that I'm going to use. The functional form that I'm going to use looks like this. I'm going to take an electric field that is entirely in the
z
direction and the
z
field will depend on
y
and
t
. And I'm going to take a magnetic field which is going to be in the
x
direction and the
B
field is going to depend on the
y
and
t.
So let me tell you how my axes are defined here. This is
x,
this is
y
, this is
z
. The electric and magnetic fields, the electric field will always point along the
z
axis. The magnetic field will always point along the
x
axis. They will not vary, as you vary
x
or
z
. They'll vary only if you vary
y
by assumption. In general, it can vary with everything, but I'm trying as a modest goal to find a simple solution which has a dependence on only two of the four possible coordinates. It depends on only
y
and
t
, rather than
x, y, z
and
t
. Let's get any solution. We cannot get every possible one; let's get something and something, I assume, has this form. So this is called a plane wave, because if you take the plane
y
= 0,
E
and
B
are constant on that plane. Because when
y
is fixed or some value,
E
and
B
are not changing as you vary
x
and
z
. So you should think of it as plane after plane and on each plane, the field is doing something. It's doing the same thing. If I draw a plane here, that field is a constant.
E
is a constant and that plane and
B
is a constant on that plane.
On another plane, it could be a different constant, but within the plane, it varies from plane to plane. So that is not an axiom, that's not a law. That's an assumed simplicity in the function I'm looking at. There's no theorem that says that every solution to Maxwell equations much obey this condition. In general, these functions will be functions of
x, y, z
and
t
. The trick will be superposition. If I can get a solution that depends only
y
and
t
, and you can get a solution that depends on
z
and
t
, I can add them up and they will still be a solution, because the wave equation is linear. You can add solutions. Then our sum of the two solutions will be a function of
y
and
z
. You can bring in the
x
and so on. So you do the simplest one, then you can add them. So here is my function and I have to know what I can say about these two functions. You understand? In general, the electric field has three components, the magnetic field has three components. Each of them depends on four quantities,
x, y, z
and
t
. Big mess. In our simplified solution, the only unknown component of
E
is
Ez
. I'm assuming there is no
Ex
and there is no
Ey
. And there is no
By
and there is no
Bz
.
Now you might say, "Why don't you go a little further? Kill the
B
also." You can try that. If you kill the
B
, you will find the only solution is to get everything equals 0. So by trial and error, we know this is the first time you can get something interesting going. If you make it simpler than that, you get nothing. You can make it more complicated, but not simpler.
So now, will this satisfy the surface integral condition? Let's check that? So what do I need to do for that? I have to take a cube, right? Let me take the cube. It's infinitesimal, but I'm just keeping it near the origin. It can be anywhere you want, but I'm drawing it near the origin. It's a surface, and it's got these outward going normals. And I must take
E
⋅ surface area for every face. And I've got to get 0. That's the condition. So is that going to work or not? Let us see. There are six faces in this cube, so I'm going to draw 1, 2 and 3 that I can see, and -1, -2 and -3 refer to the faces on the opposite side. This is 3, that's -3.
So I can only show you 1, 2 and 3. Let's look at surface 1 and ask what I get from the surface integral of
E
. Do you agree that
E
points this way? So
E⋅dA
is a non-zero contribution on surface 1. But on surface -1,
E
still points up, but
dA
points down, because
E
doesn't vary from the upper face to the lower face, because in going from upper to lower, I'm varying the coordinate
z
, but nothing depends on
z
. The same electric field is sitting on the upper plane of this cube as on the lower plane of the cube. Therefore the surface integrals will cancel and give you 0, because the area vectors are opposite. That is a simple statement, that if you've got a constant electric field going through a cube, the net flux will be 0 because what's coming in on one side goes out of the other side. So that's the cancelation of 1 and -1 giving me 0. But there are other faces, like 3 and -3. What surface integral will I get from 3? The area vector looks like this, the electric field looks like that, the dot product is 0. In other words, the field lines are parallel to this face, so they are not going to penetrate it. You're not going to get any flux. Or the area vector is perpendicular to the field vector.
So on this face,
E
is 0, on the opposite face is also 0. The same thing goes for 2 and -2. If you go to face number 2 here, the electric field is pointing like that, but there is no flux and there is no flux on the opposite face. So if you get 0, either because the field is parallel to the face, or if it's perpendicular, it has the same value on opposite faces, with opposite pointing normals, or opposite pointing area vectors and you get 0. That's how you get the surface integral of
E
to be 0 on this tiny cube. But if it's 0 on a tiny cube, it's 0 on anything you can build out of tiny cubes. That means 0 on any surface. If you repeat the calculation for
B
, you'll get pretty much the same logic, except that
B
now points like this. So on the top face,
B
will have no flux because it's running along the face. There is no flow through that. Top and bottom are 0 and 0. The only faces that matter are 2 and -2, because 2 is coming out of the board and
B
is coming out of the board. But on the other face, which you cannot see, the -2,
B
is still going this way, but
E
, the area vector is going the opposite way. The key to this is that
B
does not vary.
You see, if the flux was not constant, if the field was not constant, the fact that you've got two faces with opposite pointing area vectors doesn't mean the answer is 0. Even though the area vectors are opposite, the field strength would be bigger on one face, smaller on the opposite face, in which case they won't cancel. But the field is not varying in the coordinate in which I've displaced the planes. That's the reason you get 0 for both of those. All right. So far what I've shown you is that the solution I have automatically satisfies 0 surface integral without any further assumptions. Of course, it's very important that
E
did not vary with
x
and
z
. But with the assumed form, I don't have to worry. I still have to only worry about the other two Maxwell equations involving line integrals. I've got to make sure that works out.
So let's see. So here I have to take loops and I told you, when you take loops now, you've got to take loops in that plane, that plane, and that plane, because it takes three kinds of little flat Lego pieces to form a curved surface in 3D.
So let me take this loop first. I want to take an infinitesimal loop that looks like this. I choose the orientation of this so that if I do the right hand rule, the area vector is pointing in the positive y direction. In other words, this is a tiny loop of size
Δy
— let's see.
Δx
this way and
Δz
that way. The area vector is coming out like that. So I have to now look at the line integral of
E⋅dl
and equate it to -
d
Φ
B
/dt
. I have to see, is that true or false? Well, take this loop and look at the line integral of
E
and see what happens. There is an
E
going up this face.
E
is perpendicular to that face , and
E
is perpendicular to that edge.
E
is anti-parallel to this edge. You see that? If
E
is pointing up, it cancels between these two. These two have no contribution, because
E
is perpendicular to
dl
. But these two cancel. They cancel again because the
E
that you have here going up is the same
E
that you have here also going up, but the
dl
is going in opposite directions. Therefore
E
⋅
dl
around this tiny loop is actually 0. You understand why it is 0? Cancelation between opposite edges, and two edges that don't give you anything. So what we hope for is that on the right hand side, there better not be any magnetic flux coming out of this thing, because otherwise right hand side will give you a non-zero contribution.
But luckily, that is the case, because the magnetic field looks like this. It's in the plane of this loop. The dot product of the area vector, which is perpendicular to the loop and the
B
field is 0, so that's also 0. So this is identically satisfied on that loop. Now if you take line integral of
B
⋅
dl
, and that's supposed to be +
μ0ε0 d
Φ
/dt
of the electric flux, again, you should try to do the exercise with me. Magnetic field, I said, is going in the
x
direction, so it has nothing to do with those two edges, because they are perpendicular to it, but it cancels between these two. It cancels because the edges are going in the opposite direction, but
B
doesn't vary from this edge to that edge. It varies only with y, so again you get 0. And there is no electric flux coming out of this surface, because electric field lines also lie in the plane of that loop. They don't cross it. So those equations are also satisfied.
But I'm not done, because I still have to consider loops in this plane and loops in that plane. So far I've gotten no conditions at all. What this means so far is that there are no further restrictions on
Ez
and
Bx
. They can be anything you like. But I'm going to get restrictions by finally considering loops in this plane and loops in that plane. So let's see how you get conditions on one of them.
This is
x, y, z
. So let's take a loop that looks like this. I've chosen it so that with the right hand rule, the area vector is perpendicular and coming out the x axis. I remind you once again,
E
looks like that, and
B
looks like this. So let me give the edges a name, 1, 2, 3, 4. And let's take the condition
E
⋅
dl
= -
d/dt
of the magnetic flux. Now this loop has dimension
dy
in this direction,
dz
in that direction. This is an infinitesimal loop. I've drawn it so you can see it, but it's infinitesimal. Okay, so what do I get on the right hand side? Right hand side says −
d/dt
of the magnetic flux coming out of the board. The magnetic flux is coming out like this, right? It's coming out of the blackboard, so there really is a magnetic flux. That magnetic flux is the number I wrote down,
Bx
times the loop area which is
dy/dz
. That gives me -
ΔyΔz Bx dt
. That's the right hand side. This loop is so tiny, I am approximating
B
by the value at the center if you like. You might say, "Look, I don't think
B
is a constant on the loop.
B
is varying. Why do you take the value of the center?" Well, if it varies, the variation is proportional to
Δx
. I'm to
Δy
or
Δz
, therefore that will be a term proportional to
Δy
squared or
Δz
squared. But we are going to keep things to first order in
Δy
and
Δz
, so it doesn't matter.
Now how about the left hand side? If you look at the left hand side, I hope you'll try to do this one. If you go like that on edge 2, you will get
Ez
times
Δz
— I'm sorry. Let me write it as
Δz
times
Ez
at the point
y
+
Δy
. And on this edge, I will get -
Δz
times
Ez
at the point
y
. In other words, the electric field is everywhere, going up, so it goes up here.
E
is parallel to it, so that should be that times
Δz
. These two don't contribute, because
E
and Δ
L
are perpendicular, so forget that. But this one, it goes in the opposite direction, so I subtract it, but I bear in mind that this is
y + Δy
, but that's only
y
. So here I hope you guys will know what to do. You will say that is then roughly equal to
dEz/dy
times
Δy
. Therefore the line integral of the electric field is proportional to the derivative of
dz
with respect to
y,
times the area of the loop. And the surface integral of the flux change is also proportional to the area of the loop, and you get
dBx/dt
. So this is the final equation you get by considering that loop. So what is remarkable is the line integral and the surface integral are both proportional to the area. The surface integral being proportional to the area of the loop is obvious, because it's the surface integral.
Why is the line integral proportional to the area? Because one part of the line integral is the width of the loop,
Δz
, other one comes in because the extent to which they don't cancel is due to the derivative of the field in the transverse direction. That brings you a
Δy
. So if you cancel all of this, you get the equation that I'm interested in, which is very important:
dEz/dy
= -
dBx/dt
. This came from looking at this equation.
The last one, another loop equation, I'm going to go through somewhat quickly, because it's going to be 0 = 0. Suppose I take the integral of the magnetic field around this loop. Do you understand why it is 0? The magnetic field is coming out of the blackboard.
dl
's are all lying in the plane, so line integral of
B
is then 0. And that better be equal to -
μ0ε0 d
Φ
electric
/dt
. That is the case, because there is no electric flux coming out of this face. The electric lines are in the plane of the loop. There is no electric flux, there is no rate of change, so it's 0 = 0.
So from this loop, I've managed to get one equation. So my plan now is, I don't want to do yet another loop, because you've got the idea, or it's not going to help to draw one more loop. But I would just say that if you draw the last loop, which lies in what plane? Which lies in this plane. You will get one more equation. I'm just going to tell you what it is. I got
dEz/dy
is -
dBx/dt
. You'll get another equation,
dBx/dy
= - μ0ε0
dEz/dt
. So I confess, that I've not derived this one, but it's going to involve just drawing one more loop and doing it. Now it's really up to you guys how much you want to do this, but you should at least have some idea what we did. It turns out these are the only restrictions I have to satisfy. If this is true of my field, I'm done, because I've satisfied every Maxwell equation. Every surface integral was 0 on every tiny cube and therefore 0 everywhere for
E
and
B
. The line integrals, some were identically satisfied, some were 0 = 0. There were some that led to non trivial conditions and it's these two. Therefore I'm told that if the fields that I pick, that depend on y and t, have the property that the y derivative of this guy is the t derivative of that guy, and the y derivative of
Bx
is up to some constant, the -t derivative of the other guy, you're done.
That's all you require of that function. So let's do the following: take this equation, take its y derivative on both sides. IN other words, I want to take y derivative of this and I want to take y derivative of that. Then here you will get
d2Ez/dy2
= -
dBx/dy dt
. Take the
d/dz
of this. Now you know partial derivatives, you can take the derivatives in any order you like, so let's write it as
d/dt
,
d/dy
. But
dBx/dy
is
μ0dEz/dt
. Another
dt
makes it +
μ0ε0d2Ez/dt2
. Take first the y derivative,
dBx/dy
, is that one single time derivative. Take one more time derivative, you get this. Now we get this wonderful — we really have the wave equation now, because I get
d2Ez/dy2
μ0ε0d2Ez/dt2
= 0, which you recognize to be the wave equation. That's what the wave equation looks like in the top of the blackboard. But the things that are oscillating now are not some string. It is really the electric field oscillating. It's not a medium that's oscillating. There's nothing there. This is all in vacuum.
So let's find the velocity.
v2
will be 1/
μ0ε0
, right? Because this thing that comes with our equation is the 1/
v2
term. Then you go back to your electrostatics and magnetostatics and find out what these numbers are. And I remind you that ¼
Πε0
is 9×109 and
μ0/4Π
is 10-7.
So let's write this as 4
Π/μ0
times ¼
Πε0
, because we know what those guys are. ¼
Πε0
is 9×109. And 4
Π/μ0
is 107, so you get 9×1016. Or the velocity is 3×108 meters per second. So this was the big moment in physics, when you suddenly realize that these things are propagating at the velocity of light. So people knew the velocity of light from other measurements. They had a fairly good idea what it was. They know μ0 by doing experiments with currents. They knew ε0 from Coulomb's law. It's one of the greatest syntheses that you put them together and out comes an explanation. Now this doesn't mean that electromagnetic waves are the same as light. You agree that if you run next to a buffalo at the same speed, you are not a buffalo. You just happen to have the same speed. So that was a bit of a leap to say it is really light. But it was also known that whenever you have sparks in electrical circuits and so on, you see light. So it took a little more than that, but it's quite amazing, because gravity waves also travel at the speed of light. You cannot assume that the speed means the same phenomenon. But they were really right this time. It really was the speed of light.
Chapter 4: Light as an Electromagnetic Wave [00:56:48]
So we now have a new understanding of what light it. Light is simply electromagnetic waves traveling at the speed. It consists of electric and magnetic fields. What we have is an example of a simple wave, but one can show in general that if you took the most general
E
and
B
you can have, you will get similar wave equations. You will get it for every component of
E
and every component of
B
. So waves in three dimensions will satisfy the general wave equation. But I'm not interested in the most general case, because this is enough to show you where everything comes from.
So you have to think about how wonderful this is, because you do experiments with charges, with currents, and you describe the phenomenology as best as you can. Then Maxwell added that extra term from logical consistency, by taking this capacitor and drawing different surfaces, and realizing that unless you added the second term,
d
Φ
E
/dt
it didn't work. And without the second term, you don't get the wave. It's only by adding the second term and then fiddling with equations, he was able to determine that waves can travel. So the reason that electromagnetic waves travel in space without any charges is, once you've got an
E
field or
B
field somewhere, it cannot just disappear. It's like the LC circuit. If your capacitor is charged, by the time it discharges, it has driven a current in the inductor. Inductor is like a mass and it's moving with velocity. Current is like velocity, so it won't stop. So the current keeps going till it charges the capacitor the opposite way. Then they go back and forth. They are the only 1 degree of freedom, which is the charge in the capacitor or the current in the circuit, which are related. Here
E
and
B
are variables defined everywhere, but you cannot kill
E
because the minute you try to destroy
E
, you will produce a
B
. The minute you try to destroy
B
, you'll produce an
E
, so they keep on swapping energy and going back and forth. So it is self sustaining and it's an oscillation if you like, but it's an oscillation over all of space, and not over 1 or 2 degrees of freedom.
So I'm going to now write down a specific form. The specific form I'm going to write down looks like E = k times E0. Now I'm going to pick a particular function, ky - ωt, and I'm going to take B to be I times B0 sine ky - ωt. Now I'm making a very special function of y and t. Till now, I just said it's a function of y and t. All I needed was it's a function of y and t.
That was enough to get me all this. I'm going to find a relation between these constants,
E0
and
B0
, by putting them into these two Maxwell equations I had. That's all I want to do now. So one condition I had was
dEz/dy
was -
dBx/dt
. Then I had
dBx/dy
is -
μ0ε0dEz/dt
. These are the two equations. I'm going to demand that these particular functions obey these two equations. If they obey these two equations, they will obey the wave equation, because when I combine this equation with that, I got the wave equation. Do you understand? I have an equation A and an equation B, if I put one into the other, I got the wave equation. But you really should satisfy separately equation A and equation B, because it's not enough to satisfy the one you get by shoving one in the other. They should be true independently.
So let's demand that this be true and demand that be true. So what is
dEz/dy
? If I take the
d/dy
of this, this is what I call
Ez
and this is what I call
Bx
.
dEz/dy
, if you take the
d/dy
of that, will give me
kE0
cos
(ky - ωt).
And we want that to be = -
dBx/dt
. So take the
d/dt
of this guy.
d/dt
of this guy is
B0
ω
cos
(ky - ωt)
. So these things cancel out, then I get
B0ω
. So this tells you that
E0 = ω/k B0
. It tells you about the magnitude of the
E
and
B
vectors, what size they should bear in relation to each other. This is one condition. I'm almost done. So I want to take this condition now. So
dBx/dy
, what is that equal to?
B0k
cos
(ky - ωt)
= -
μ0ε0dEz/dt
which will be -
ωE0
cos
(ky - ωt)
. Cosines cancel, then I get a condition
B0k
=
μ0ε0
ω times
E0
. But that equals
ω/c
squared times
E0
, because
μ0ε0
is 1/
c2
. So I get a second condition which I can write as
E0
=
c2
/
ω
times
B0
. So these are the two conditions in the end. If you want the function to look like this traveling wave, with sine waves in it, then the amplitude for
E
and the amplitude for
B
have to satisfy these two conditions. But look at these two equations. They're both telling you something about
E0
. One says
E0
should be
ω/k
times
B0
. The other says
E0
should be
c2/ω
times
B0
. That means
ω/k
better equal
c2
— I bet I dropped a
k
somewhere.
Student:
You had
B0k
in the —
Professor Ramamurti Shankar:
Thank you, yes. So
c2k/ω
. That tells me that
ω2= k2c2ω = kc
+ or -. Or if you like,
k
is ±
ω/c
. It doesn't matter how you write it, but you can see what that means. What this is telling you is that if you take the function sine
ky - ωt
, and if
ω = kc
, it becomes sine of
ky - kct
. That becomes sine of
k
times
y - ct
which is a function of
y - ct
. In other words, we knew this was going to happen, because the wave equation says the function should be a function only of
y - ct.
That will happen if
ω = kc
. You see that? If
ω = kc
, you pull the
k
out, you get
y - ct
. Or you can have
y + ct
, but my solution was
y - ct
.
I'm almost done. So the last thing I want to get from this same equation, now that that condition is satisfied, if
ω
=
kc
, I get
E0
=
c
times
B
. So now I'm going to summarize this. Don't worry about the details. I will tell you the part you should know all the time. So I know this is somewhat heavy. I had to do this calculation at home to make sure I got all the - signs right. There's an orgy of - signs. I'm not that interested in that.
I know that you guys, unless you're going to major in physics and want to do it for a lifetime, don't want to know all that. So what should you know? What you should know is that by doing a few experiments, one wrote down these Maxwell equations. You've got to understand a little bit where everything came from. Then the whole class was demonstrating that they implied some waves and the demonstration was shown for proving it for infinitesimal loops and infinitesimal cubes and then seeing what conditions I had. And I found that I could get a set of functions that are dependent on y and t, and that they really travel at the speed of light. So that was the bottom line. Actual derivatives and how everything happened is really not something I expect you to carry in your head, so don't let the exams ruin that for you. I don't care. I will not quiz you on that part of this derivation. But you must understand that the structure of physics was such that it was an interplay between some experiments and some purely theoretical reasoning on the nature of equations. And you put them together and what makes it worthwhile in the end is to get fantastic productions like this that unify electricity and magnetism and light into one shot.
So the picture I get now, if you look at all of this, the final answer is
E
looks like
k
times some number
E0
sine
ky
ωt
. But I want you to know that ω =
kc
there. Then I get
B
=
IB0
also the same sine, with the extra restriction that
B0
times
c
=
E0
.
So here is what the electromagnetic wave looks like. One guy, the electric field, is always living in this plane. This is the
E
field. At one instant, if you take a snapshot, that's what it will be doing, going up there, coming down here, going up there. That's
E
.
B
field looks like this, lies horizontal here, goes like hat and comes out. So this is in that plane and that is in the vertical plane. That's horizontal plane, that's the vertical plane. So that is
E
and this is
B
. And the point is,
E
over
B
=
C
. In other words,
E
is much bigger than
B
. The ratio of them is the velocity of light. This is interesting, because if you took the force on a charge, you remember is
q
times
E
+
v
x
B
. That means if you took an electron and you left it in the electromagnetic field, the field comes and hits you. If
E
field is oscillating one way, the
B
field is oscillating perpendicularly.
The wave is traveling in a direction perpendicular to both. If you want, it's in the direction of
E
x
B
, is the direction of propagation of the wave. If it hits an electron there, the oscillating up and down electric field will make the electron move up and down. It will also be feeling a magnetic force,
V
x
B
. But notice that the size of
B
is the size of
E
divided by
c
. So the electric force to magnetic force ratio, or magnetic electric will be the ratio of
v
over
c
. So for most velocities, for electrons and circuits and so on, the velocity is much tinier than the velocity of light. So when a radio wave hits your antenna, gets the electric charges in action, it's the electric field that does most of the forcing, not the magnetic field. But in astrophysics and cosmic ray physics, where particles can travel at velocities comparable to that of light, then these forces can become comparable.
All right, so we will resume this after the break. I'll see you in the exam. I'll be traveling, but if you have any worries, any concerns about the exam, you can email me. I'll look for it. I think the exam is very reasonable. It's not as difficult as the homework. I think there are no fantastic tricks you have to think up in the last minute. I would say go over the exam once and find the friendly problems and do them first. Then when you're warmed up, do the others. Yeah?
Student:
[inaudible]
Professor Ramamurti Shankar:
I don't think — somebody asked me that. I dug them up from some stuff. I don't know where the solutions are, and the TAs are already overloaded, so sorry.
Student:
What is
k
in ω =
k
—
Professor Ramamurti Shankar:
Oh yeah. I should explain that next time. Good point.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/spring10/phys201/mp3/phys201_14_022410.mp3) |
