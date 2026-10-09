- Source: https://oyc.yale.edu/physics/phys-200/lecture-6
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 6 - Law of Conservation of Energy in Higher Dimensions

### Overview

The discussion on the Law of Conservation of Energy continues but is applied in higher dimensions. The notion of a function with two variables is reviewed. Conservative forces are explained and students are taught how to recognize and manufacture them.

### Lecture Chapters

1. Calculus Review: Small Changes for Motion in 2D
2. Work Done in 2D; Dot Products and Cross Products
3. Conservative and Non-conservative Forces
4. Cross Derivative Test for Potential Energy Equations
5. Application to Gravitational Potential Energy

1. 0
2. 1085
3. 2176
4. 3149
5. 3835

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 6 - Law of Conservation of Energy in Higher Dimensions
Chapter 1. Calculus Review: Small Changes for Motion in 2D [00:00:00]
Professor Ramamurti Shankar:
If you've got a function
f(x)
, you know the value at some point, and you want to go to a neighboring point, a distance
Δx
away. You ask, "How much does the function change?" And the answer is, the change in the function
Δf
is the derivative of the function at the starting point times the distance you move. This is not an equality, unless
f
happens to be a straight line; it's an approximation and there are corrections to this. That's what all the dots mean; corrections are proportional to
Δx2
and
Δx3
and so on. But if
Δx
is tiny this will do; that's it.
But today, we are going to move the whole Work Energy Theorem and the Law of Conservation of Energy to two dimensions. So, when you go to two dimensions, you've got to ask yourself, "What am I looking for?" Well, in the end, I'm hoping I will get some relation like
K1 + U1 = K2 + U2
, assuming there is no friction.
U2
is going to be my new potential energy. Then, if it's the potential energy and the particle is moving in two dimensions, it's got to be a function of two variables,
x
and
y
. So, I have to make sure that you guys know enough about functions of more than one variable. So, this is, again, a crash course on reminding you of the main points. There are not that many. By the time I get here I'll be done.
So, how do you visualize the function of two variables? The function of one variable, you know, you plot
x
this way and the function along
y
. If it's two variables, you plot
x
here and
y
here and the function itself is shown by drawing some surface on top of the
xy
plane, so that if you take a point and you go right up till you hit the surface, that's the value of the function, at that point
xy
. It's like a canopy on top of the
xy
plane and how high you've got to go is the function. For example, starting with the floor, I can ask how high you have to go till I hit the ceiling. That function varies; there are dents and dimples and so on, so the function varies with
xy
. Another example of a function of
x
and
y
--
x
and
y
could be coordinates in the United States and the function could be the temperature at that point. So, you plot it on top of that, each point you plot the temperature at that point.
So, once you've got the notion of a function of two variables, if you're going to do calculus the next thing is what about the derivatives of the function. How does it change? Well, in the old days, it was dependent on
x
and I changed the
x
and I found the change in the function divided by the change in
x
and took the limit and that became my derivative. And now, I'm sitting in the
xy
plane, so here is
x
and here is
y
; I'm here, the function is coming out of the blackboard. So, imagine something measured out but I'm sitting here. Now, I want to move and ask how the function changes. But now I have a lot of options; in fact, an infinite number of options. I can move along
x
, I can move along
y
, I can move at some intermediate angle, we have to ask what do you want me to do when it comes time to take derivatives. So, it turns out, and you will see it proven amply as we go along, that you just have to think about derivatives on two principle directions which I will choose to be
x
and
y
.
So, we're going to define one derivative, which is defined as follows. You start at the point
xy
, you go to the point
x
+
Δx
, the same
y
and subtract the function at the starting point, divide by
Δx
and take all the limits,
Δx
goes to 0. That means you go from here to here, you move a distance
Δx
, you'd find the change in the function, you take the derivative. As you move horizontally, you notice you don't do anything to
y
;
y
will be left fixed at whatever
y
you had;
x
will be changed by
Δx
; you find the change; you take the derivative and take the limit that is denoted by the symbol
df/dx.
[Reader note: Partial derivatives will be written as ordinary derivatives to avoid using fonts that may not be universally available. It should be clear from the context that a partial derivative is intended here, since
f
depends on
x
and
y
.]
So, this curly
d
instead of the straight
d
tells you it's called a "partial derivative." Some people may want to make it very explicit by saying this is the derivative with subscript
y
. That means
y
is being held constant when
x
is varied, but we don't have to write that because we know we've got two coordinates. If I'm changing one, the other guy is
y
so we won't write that; that's the partial derivative. So, you can also move from here to here, up and down, and see how the function changes. I won't write the details, you can define obviously a
df/dy
. So, one tells you how the function changes, with
x
I should move along
x
, and the other tells you how it changes at
y
as you move along
y
.
Let's get some practice. So, I'm going to write some function,
f = x3y2
, that's a function of
x
and
y
. You can write any--let's make it a little more interesting, plus
y
, or
y2
; that's some function of
x
and
y
. So, when I say
df/dx
, the rule is find out how it varies with
x
keeping
y
constant. That means, really treat it like a constant, because number five--What will you do if
y
was equal to 5? This'll be 25 and it's not part of taking derivatives because it's not changing, and here it'll be just standing in front doing nothing; it will just take the
x
derivative, treating
y
as a constant. You're supposed to do that here; this is a derivative 3
x2y
; so that's the
x
derivative. Now, you can take the
y
part,
y2
, yes, thank you. Then, I can take
df/dy
, so then I look for
y
changes, this is 2
y
here, so it's 2
x3y
+ 2
y
; so that's the
x
derivative and the partial
y
derivative.
Okay, so then you can now take higher derivatives. We know that from calculus and one variable, you can take the derivative of the derivative. So, one thing you can think about is
d2f/dx2
, that really means take the
d
by
dx
of the
d
by
dx
. That's what it means. First, take a derivative and take the derivative of the derivative. So, let's see what I get here. I already took
df/dx
. I want to take its derivative, right, the derivative of
x2
is 2
x
, so I get 6
xy2
. Then, I can take the
y
derivative of the
y
derivative,
d2f/dy2
, that's
d
by
dy
of
df/dy
, if you take the
y
derivative there. You guys should keep an eye out for me when I do this. I get this. But now, we have an interesting possibility you didn't have in one dimension, which is to take the
x
derivative of the
y
derivative, so I want to take
d
by
dx
of
df/dy
. That is written as
d2f/dxdy
. Let's see what I get. So, I want the
x
derivative of the
y
derivative. So, I go to this guy and take his
x
derivative, I get 3
x2
from there, so I get 6
x2y
and that's it. So, make sure that I got the proper
x
derivative of this, I think that's fine. Then, I can also take
d2f/dydx
. That means, take the
y
derivative of the
x
derivative, but here's the
x
derivative, take the
y
derivative of that, put a 2
y
there, and I get 6
x2y
.
So, you're supposed to notice something. If you already know this, you're not surprised. If you've never seen this before, you will notice that the cross derivative,
y
followed by
x
and
x
followed by
y
, will come up being equal. That's a general property of any reasonable function. By reasonable, I mean you cannot call the mathematicians to help because they will always find something where this won't work, okay? But if you write down any function that you are capable of writing down with powers of
x
and powers of
y
and sines and cosines, it'll always be true that you could take the cross derivatives in either order and get the same answer. I'd like to give a little bit of a feeling for why that is true; it's true but it's helpful to know why it's true. So, let's ask the following question.
Let's take a function and let's ask how much the function changes when I go from some point
x
,
y
to another point
x
+
Δx
,
y
+
Δy
. I want to find the change in the function. So, I'm asking you what is
f(x + Δx, y + Δy) - f(x,y)
for small values of
Δx
and
Δy
. For neighboring points, what's the change? So, we're going to do it in two stages. We introduce an intermediate point here, whose coordinate is
x + Δ x
and
y
, and I'm going to add and subtract the value of the function here. Adding and subtracting is free; it doesn't cost anything, so let's do that. Then, what do I get? I get
f(x + Δx, y + Δy ) - f(x + Δx, y) + f(x + Δx, y) - f(x,y)
. I'm just saying, the change of that guy minus this guy is the same as that minus this, plus this minus that; that's a trivial substitution. But I write it this way because I look at the first entity here, it looks like I'm just changing
y
. I'm not changing
x
, you agree? So what will this be? This is going to be the rate of change of the function with respect to
x
times
Δx
, and this--I'm sorry, I got it wrong, with respect to
y
times
Δy
. This one is
df/dx
times
Δx
. Therefore, the change in the function, if I add it all up, I get
df/dx Δx + df/dy Δy
. But if you are pedantic, you will notice there is something I have to be a little careful about. What do you think I'm referring to, in my notation, yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
Meaning?
Student:
[inaudible]
Professor Ramamurti Shankar:
Oh, but this is nothing to do with dimension, you see. It's one number minus another number. I put another number in between and in this function; it's a function only of here. Let me see,
x
is not changing at all and
y
is changing, so it is
df/dy Δy
. I meant something else. That is, in fact, a good approximation but there is one thing you should be careful about which has to do with where the derivatives are really taken. For the term here,
f(x + Δx, y) - f(xy)
, I took the derivative, at my starting point. If you want, I will say at the starting point
xy
. The second one, when I came here and I want to move up, I'm taking the derivative with respect to
y
at the new point. The new point is
(x + Δx, y)
, so derivatives are not quite taken at the same point. So, you've got to fix that. And how do you fix that part? You argue that the derivative with respect to
y
is just another function of
y
;
f
is a function of
x
and
y
, its derivatives are functions of
x
and
y
. Everything is a function of
x
and
y
, and we are saying this derivative has been computed at
x + Δx
, instead of
x
, so it is going to be
df/dy
at
xy
+ d2f/dxdy
times
Δx
.
In other words, I am saying the derivative at this location is the derivative at that location, plus the rate of change of the derivative times the change in
x
. In other words, the derivative itself is changing. So, if you put that together you find it is
df/dx Δx + df/dy Δy
, where if I don't put any bars or anything it means at the starting point
xy + (d2f/dxdy) Δx Δy
. Now, you've got to realize that when you're doing these calculus problems, Δx is a tiny number, Δy is a tiny number, Δx Δy is tiny times tiny. So normally, we don't care about it, or if you want to be more accurate, of course, you should keep that term. In the first approximation, where you work to the first power of everything, this will be your
Δf
. But if you're a little more ambitious but you keep track of the fact the derivative itself is changing, you will keep that term.
But another person comes along and says, "You know what, I want to go like this. I want to introduce as my new point, intermediate point, the one here. It had a different value of
y
in the same
x
and then I went horizontally when I keep track of the changes." What do you think that person will calculate for the change in the function? That person will get exactly this part, but the extra term that person will get will look like
d2f/dydx
times
Δy Δx
. If you just do the whole thing in your head, you can see that I'm just exchanging the
x
and
y
roles. So, everything that happened with
x
and
y
here will come backwards with
y
and
x
. But then, the change between these two points is the change between these two points and it doesn't matter whether I introduce an intermediate point here or an intermediate point there; therefore, these changes have to be equal. This part is of course equal; therefore, you want that part to be equal,
Δx Δy
is clearly
Δy Δx
, so the consequence of that is
d2f/dxdy
=
d2f/dydx
and that's the reason it turns out when you take cross derivatives you get the same answer. It comes from the fact -- if you say, where is that result coming from -- it comes from the fact, if you start at some point and you go to another point and you ask for the change in the function, the change is accumulating as you move. You can move horizontally and then vertically, or you can move vertically and then horizontally. The change in the function is a change in the function. You've got to get the same answer both ways. That's the reason; that's the requirement that leads to this requirement.
Now, I will not be keeping track of functions to this accuracy in everything we do today. We'll be keeping the leading powers in
Δx
and
Δy
. So, you should bear in mind that if you make a movement in the
xy
plane, which is
Δx
horizontally and
Δy
vertically, then the change in the function is this [
df/dx Δx + df/dy Δy
]. Draw a box around that, because that's going to be--This is just the naïve generalization to two dimensions of what you know in one dimension. We were saying look, the function is changing because the independent variables
x
and
y
are changing, and the change in the function is one part, which I blame on the changing
x
, and a second part, which I blame on the changing
y
and I add them. So, you're worried about the fact that we're moving in the plane and there are vectors. That's all correct, but
f
is not a vector,
f
is just a number and this change has got two parts, okay. So, this is basically all the math we will need to do, what I want to do today.
Chapter 2. Work Done in 2D; Dot Products and Cross Products [00:18:05]
So, let's now go back to our original goal, which was to derive something like the Law of Conservation of Energy in two dimensions instead of one. You remember what I did last time so I will remind you one more time what the trick was. We found out that the change in the kinetic energy of some object is equal to the work done by a force, which was some
F
times
Δx
and then if you add all the changes over a not infinitesimal displacement, but a macroscopic displacement, that was given by integral of
F
times
dx
and the integral of
F
times
dx
from
x1
to
x2
. If
F
is a function only of
x
, from the rules of calculus, the integral can be written as a difference of a function at this limit minus that limit, and that was
U(x1) - U(x2)
, where
U
is that function whose derivative with a minus sign is
F
. That's what we did. Then, it's very simple now to take the
U1
to the left-hand side. Let me see,
K1
to the right-hand side and
U(x2)
to the left-hand side, to get
K2 + U2 = K1 + U1
and that's the conservation of energy.
You want to try the same thing in two dimensions; that's your goal. So, the first question is, "What should I use for the work done?" What expression should I use for the work done in two dimensions, because the force now is a vector; force is not one number, it's got an
x
part and a
y
part. My displacement has also got an
x
part and a
y
part and I can worry about what I should use. So, I'm going to deduce the quantity I want to use for
ΔW
, namely, the tiny work done which is an extension of this. I'm going to demand that since I'm looking for a Work Energy Theorem, I'm going to demand that, remember in one dimension
ΔK = F Δx
. If we divide it by the time over which it happens, I find
dK/dt
is equal to force [F] times velocity [v].
I'm going to demand that that's the power, force times velocity, is what I call the power. And I'm going to look for
dK/dt
in two dimensions, of a body that's moving. What's the rate at which kinetic energy is changing when a body is moving? For that, I need a formula for kinetic energy. A formula for kinetic energy is going to be again ½
mv2
. I want that to be the same entity, so I will choose it to be that, but
v2
has got now
vx2
+ vy2
, because you know whenever you take a vector
V
, then its length is the square root of the
x
part squared plus the
y
part squared. Any questions? Okay, so let's take the rate of change of this,
dK/dt
. Again, you have to know your calculus. What's the time derivative of
vx2
? The rule from calculus says, first take the derivative of
vx2
with respect to
vx
, which is 2
vx
, then take the derivative of
vx
with respect to time. So, you do the same thing for the second term, 2
vy dvy/dt
, and that gives me--the 2s cancel, gives me
mdvx /dtvx + m dvy /dtvy
. This is the rate at which the kinetic energy of a body is changing. So, what's my next step, yes?
Student:
So what happened to the half?
Professor Ramamurti Shankar:
The half got canceled by the two here. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
That's correct. So, what we want to do is to recognize this as
ma
in the
x
direction, because
m
times
dvx/dt
is
ax
, and this is
m
times
ay
. Therefore, they are the forces in the
x
and
y
directions, so I write
Fxvx + Fyvy
. So the power, when you go to two dimensions, is not very different from one dimension. In one dimension, you had only one force and you had only one velocity. In two dimensions, you got an
x
and
y
component for each one, and it becomes this. So, this is what I will define to be the power. When a body is moving and a force is acting on it, the force has two components, the velocity has two components; this combination shall be called "Power." But now, let's multiply both sides by
Δt
and write the change in kinetic energy is equal to
Fx
and you guys think about what happens when I multiply
vx
by
Δt
;
vx
=
dx/dt
. Multiplying by
Δt
just gives me the distance traveled in the
x
direction
+ Fy
times
dy
. So, this is the tiny amount of work done by a force and it generalizes what we had here, work done is force times
Δx
. In two dimensions, it's
Fxdx + Fydy
. It's not hard to guess that but the beauty is--this combination--Now you can say, you know what, I didn't have to do all this, I could have always guessed that in two dimensions, when you had an
x
and a
y
you obviously have to add them. There's nothing very obvious about it because this combination is now guaranteed to have the property that if I call this the work done. Then, it has the advantage that the work done is in fact the change in kinetic energy.
I want to define work so that its effect on kinetic energy is the same as in 1D, namely, work done should be equal to change in kinetic energy. And I engineered that by taking the change in kinetic energy, seeing whatever it came out to, and calling that the work done, I cannot go wrong. But now, if you notice something repeating itself all the time, which is that I had a vector
F
, which you can write as
I
times
Fx + J
times
Fy
, I had a vector velocity, which is
I
times
vx + J
times
vy
. Then, I had a tiny distance moved by the particle, which is
I
times
dx + J
times
dy
. So, the particle moves from one point to another point. The vector describing its location changes by this tiny vector. It's just the step in the
x
direction times
I
, plus step in the
y
direction times
J
. So, what you're finding is the following combination. The
x
component of
F
times the
x
component of
v
, plus the
y
component of
F
, times the
y
component of
v
. Or
F
component of
x
times the distance moved in
x
plus
y
component of
F
times the displacement in
y
.
So, we are running into the following combination. We are saying, there seem to be in all these problems two vectors,
I
times
Ax + J
times
Ay
.
A
, for example, could be the force that I'm talking about. There's another vector
B
, which is
I
times
Bx + J
times
By
. Right? For example, this guy could be standing in for
F
, this could be standing in for
v
. The combination that seems to appear very naturally is the combination
AxBx + AyBy
. It appears too many times so I take it seriously, give that a name. That name will be called a dot product of
A
with
B
and is written like this. Whenever something appears all the time you give it a name; this is
A.B.
So, for any two vectors
A
and
B
, that will be the definition of
A.B
. Then, the work done by a force
F
, that displaces a particle by a tiny vector
dr
, is
F.dr
. The particle's moving in the
xy
plane. From one instant to the next, it can move from here to there. That little guy is
dr
; it's got a little bit horizontal and it's got a little bit vertical, that's how you build
dr
. The force itself is some force which at that point need not point at the direction in which you're moving. It's some direction. At each point, the force could have whatever value it likes.
So, the dot product, you know, sometimes you learn the dot product as
AxBx + AyBy
, you can ask, "Who thought about it?" Why is it a natural quantity? And here is one way you can understand why somebody would think of this particular combination.
So, once you've got the dot product, you've got to get a feeling for what it is. The first thing we realize is that if you take a dot product of
A
with itself, then it's
AxAx + AyAy
, which is
Ax2 + Ay2
, which is the length of the vector
A
, which you can either denote this way or just write it without an arrow. So
A.A
is a positive number that measures the length squared of the vector
A
, likewise
B.B
. Now, we have to ask ourselves, "What is
A.B
?" So, somebody know what
A.B
is? Yep?
Student:
[inaudible]
Professor Ramamurti Shankar:
Okay, so how do we know that? How do we know it's length of
A
times length of
B
times cosine of the angle? You should follow from--Is it an independent definition or is it a consequence of this? Yep?
Student:
Well, you can derive using the Law of Cosines.
Professor Ramamurti Shankar:
Yes. He said we can derive it using the Law of Cosines and that's what I will do now. In other words, that definition which you may have learnt about first is not independent of this definition; it's a consequence of this definition. So, let's see why that's true. Let's draw two vectors here. Here is
A
and here is
B
, it's got a length
A
, it's got a length
B
, this makes an angle,
θA
with the
x
axis, and that makes an angle
θB
for the
x
axis. Now, do you guys agree that the
x
component of
A
with the horizontal part of
A
is the
A
cos θA
? You must've seen a lot of examples of that when you did all the force calculation. And
Ay
is equal to the length of
A
times
sin θA
and likewise for
B
; I don't feel like writing it. If you do that, then
A.B
will be length of
A
, length of
B
times
(cos θA cos θB + sin θA sin θB)
.
You've got to go back to your good old trig and it'll tell you this
cos cos
plus
sin sin is cos (θA - θB)
.So, you find it is length of
A
, length of
B
,
cos (θA - θB)
. Often, people simply say that is
AB cos θ
, where it's understood that
θ
is the angle between the two vectors. So, the dot product that you learnt--I don't know which way it was introduced to you first, but these are two equivalent definitions of the dot product. In one of them, if you're thinking more in terms of the components of
A
, a pair of numbers for
A
and a pair of numbers for
B
, this definition of the dot product is very nice. If you're thinking of them as two little arrows pointing in different directions, then the other definition, in which the lengths and the angle between them appear, that's more natural. But numerically they're equal. An important property of the dot product, which you can check either way, is the dot product of
A
with
B + C
, is dot product of
A
with
B
plus dot product of
A
with
C
. That just means you can open all the brackets with dot products as you can with ordinary products. Now, that's a very important property of the dot product. So, maybe I can ask somebody, do you know one property, significant property of the dot product?
Student:
When two vectors are perpendicular the dot product equals 0.
Professor Ramamurti Shankar:
Oh that's interesting, I didn't think about it. Yes. One thing is if two vectors are perpendicular the dot product is 0 because the cosine of 90 is 0. But what I had in mind--Of course it's hard for me, it's not fair I ask you some question without saying what I'm looking for. What can you say if you use a different set of axis? Yep?
Student:
In this case it doesn't matter.
Professor Ramamurti Shankar:
If you go to the rotated axis, the components of vector
A
will change. We have done that in the homework; we've done that in the class. The components of
B
will also change. Everything will get a′. But the combination,
AxBx + AyBy
, when you evaluate it before or after, will give the same answer because it's not so obvious when you write it this way. But it's very obvious when you write it this way because it's clear to us if you stand on your head or you rotate the whole axis. What you're looking for is the length of
A
, which certainly doesn't change on your orientation, or the length of
B
, or the angle between them. The angle
θA
will change but the angle with the new
x
axis won't be the same. The angle with the new
y
axis won't be the same. Likewise for
B
, but the angle between the vectors, it's an invariant property, something intrinsic to the two vectors, doesn't change, so the dot product is an invariant. This is a very important notion. When you learn relativity, you will find you have one observer saying something, another observer saying something. They will disagree on a lot of things, but there are few things they will all agree on. Those few things will be analog of
A.B
. So, it's very good to have this part of it very clear in your head. This part of elementary vector analysis should be clear in your head.
Okay, so any questions about this? So, if you want, geometrically, the work done by a force when it moves a body a distance
dr
, a vector
dr
, is the length of the force, the distance traveled, times the cosine of the angle between the force and the displacement vector.
Okay, I'm almost ready for business because, what is my goal? I find out that in a tiny displacement,
F.dr
, I start from somewhere, I go to a neighboring place, a distance
dr
away. The change in kinetic energy is
F.dr
. So, let me make a big trip, okay, let me make a trip in the
xy
plane made up of a whole bunch of little segments in each one of which I calculate this, and I add them all up. On the left-hand side, the
ΔK
s, this whole thing was defined so that it's equal to
ΔK
, right?
ΔK
was equal to this, that's equal to all that. So, if you add all the
ΔK
s, it's very clear what you will get. You will get the kinetic energy at the end minus kinetic energy at the beginning. On the right-hand side, you are told to add
F.dr
for every tiny segment. Well, that is written symbolically as this. This is the notation we use in calculus. That just means, if you want to go from
A
to
B
along some path, you chop up the path into tiny pieces. Each tiny segment, if it's small enough to be approximated by a tiny vector
dr
, then take the dot product of that little
dr
, with the force at that point, which means length of
F
, times the length of the segment, times cosine of the angle; add them all up. Then somebody will say, "Well, your segments are not short enough for me." We'll chop it up some more, then chop it up some more, chop it up till your worst critic has been silenced. That's the limit in which you can write the answer as this integral. Just like in calculus when you integrate a function you take tiny intervals
Δx
, multiply
F
by
Δx
, but then you make the intervals more and more numerous but less and less wide and the limit of that is the area under the graph and that's called "integral," you do the same thing now in two dimensions.
Chapter 3. Conservative and Non-conservative Forces [00:36:16]
So, now maybe it'll be true, just like in one dimension, the integral of this function will be something that depends on the end points. I'm just going to call it
U(1) - U(2)
, of some function
U
, just like it was in one dimension. If that is true, then my job is done because then I have
K1 + U1 = K2 + U2
. So, when I'm looking for the Law of Conservation of Energy, I've got to go to some calculus book and I got to ask the calculus book, "Look, in one dimension you told me integral of
F
from start to end is really the difference of another function
G
of the end minus the start, with
G
as that function whose derivative is
F
." Maybe there is going to be some other magic function you knew in two dimensions related to
F
, in some way, so that this integral is again given by a difference of something there minus something here. If that is the case, then you can rearrange it and get this. But you will find that it's not meant to be that simple. So, again, has anybody heard rumors about why it may not be that simple? What could go wrong? Okay so, yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
Okay, that's probably correct but say it in terms of what we know. What can go wrong? I'm saying in one end, I did an integral; the integral was the difference of two numbers and therefore I got
K + U = K + U
. So, something could go wrong somewhere here when I say this integral from start to finish is the difference only of the ending point minus the starting point. Is that reasonable or could you imagine it depending on something else? Yes?
Student:
Well, say you have one of your forces is friction. If you take a certain path from point one to point two, you should have the same thing in potential energy. But if you take a longer path and there's friction involved, your kinetic energy would be reduced.
Professor Ramamurti Shankar:
Absolutely correct. It is certainly true that if you've got friction, this is not going to work. It doesn't even work in 1D. In 1D, if I start here and end here, and I worry about friction, if it went straight from here to here there's amount of friction. If I just went back and forth 97 times and then I ended up there is 97 times more friction. So, we agreed that if there's friction, this is not going to work. But the trouble with friction was, the force was not a function only of
x
and
y
. It depended on the direction of motion. But now, I grant you that the force is not a function of velocity. It's only a function of where you are. Can something still be wrong?
Well, let me ask you the following question. Another person does this. [Shows a different path from 1 to 2] Do you think that person should do the same amount of work because the force is now integrated on a longer path? So, you see, in one dimension there's only one way to go from here to there. Just go, right? That way, when you write an integral you write the lower limit and the upper limit and you don't say any more because it's only one way in 1D to go from
x1
to
x2
. In two dimensions, there are thousands of ways to go from one point to another point. You can wander all over the place and you end up here. Therefore, this integral, even if I say the starting point is
r1
and the ending point is
r2
, that this is
r1
and that's
r2
, it's not adequate. What do you think I should attach to this integration? What other information should I give? What more should I specify? Yep?
Student:
Along a closed path.
Professor Ramamurti Shankar:
No, it's not a closed path. I'm going from 1 to 2. What more should I tell you before you can even find the work done? Yes?
Student:
What path you're going on.
Professor Ramamurti Shankar:
You have to say which path you're going on because if you only have two points, 1 and 2, then there is a work done but it depends on the path. If the work depends on the path, then the answer cannot be a function of
U(1) - U(2)
, cannot just be
U(1) - U(2)
.
U(1) - U(2)
says, tell me what you entered, tell me where you start, and that difference of some function
U
between those two points is the work done. In other words, I'm asking you to think critically about whether this equality really could be true. This is some function
U
in the
xy
plane evaluated at one point minus the other point. This is on a path joining those two points but I have not told you which path and I can draw any path I like with those same end points. And you got to realize that it's very unreasonable to expect that. No matter which path you take you will get the same answer. Okay, so you might think that I'm creating a straw man because it's going to turn out by some magic, that no matter what force you take somehow, due to the magic of mathematics, the integral will depend only on the end points. But that's not the case. In general, that won't happen. So, I have to show you that. So, I'm going to start by asking you, give me a number from 1 to 3. 2? Okay, 2. Then, I want a few more numbers, another number from 1 to 3.
Professor Ramamurti Shankar:
From 1 to 3, [audience laughs]. All right then, two more. Mark, you pick a number.
Student:
[inaudible]
Professor Ramamurti Shankar:
Good, thank you. Then I need one more, yes? 1 to 3, a number from 1 to 3.
Student:
[inaudible]
Professor Ramamurti Shankar:
2, very good. Okay, so you pick these numbers randomly, and I'm going to take a force which looks like
I
times
x2y3 + J
times
xy2
, okay? I put the powers based on what you guys gave me. So, we picked the force in two dimensions out of the hat. Now, let's ask, "Is it true for this force that the work done in going from one point to another depends only on the path, or does it depend, I mean, it depends only on the end points or does it depend in detail on how you go from the end points?" You all have to understand, before you copy anything down, where we are going with this. What's the game plan? So, let me tell you one more time because you can copy this all you want, it will get you nowhere. You should feel that you know where I'm going but the details remain to be shown or you should have an idea what's happening. If you try to generalize the Work Energy Theorem to two dimensions, this is what happened so far. You found a definition of work which has the property that the work done is the change in kinetic energy. Then, you added up all the changes of kinetic energy and added up all the work done and you said
K2 - K1
is the integral of
F.dr
; that's guaranteed to be true; that's just based on Newton's laws.
What is tricky is the second equality that that integral is the difference in a function calculated at one end point minus the other end point. If that was true, if the integral depended only on the end points, then it cannot depend on the path that you take. If it depends on the path, every path you take within the same two end points will give different numbers. So, the answer cannot simply be
U1 - U2
. First, I'm trying to convince you, through an example that I selected randomly, that if you took a random force and found the work done along one path, or another path, you will in fact get two different answers, okay? That's the first thing, to appreciate that there's a problem. So generally, if we took a random force, not a frictional force, a force that depends only on location and not velocity, it will not be possible to define a potential energy nor will it be possible to define a
K + U
so that it doesn't change. So, it's going to take a very special force for which the answer depends only on the starting and ending point and not on the path. To show you that that's a special situation, I'm taking a generic situation, namely, a force manufactured by this class, without any prior consultation with me, and I will show you that for that force the answer is going to depend on how you go.
So, let's take that force and let's find the work done in going from the origin to the point 1,1. So, I'm going to take two paths. One path I'm going to go horizontally till I'm below the point. Then I'm going straight up, okay. So, let's find the work done when I go this way. So again, you should be thinking all the time. You should say if this guy got struck by lightning can I do anything, or am I just going to say "Well, I don't know what he was planning to do." You've got to have some idea what I'm going to do. I'm going to integrate
F.dr
, first on the horizontal segment, then on the vertical segment.
F
is some vector you give me at the point
x
and
y
; I'll plug in some numbers, I'll get something times
I
and something times
J
. It may be pointing like that at this point, and that's
F
, that's given. Now, when I'm moving horizontally my displacement
dr
, has only got a
dx
part. I hope you see that. Every step I move, there's no
dy
in it, it's all horizontal. So,
F.dr
just becomes
Fxdx
because there is no
dy
when you move horizontally. So, when you do the integral, you have
Fxdx
.
Fx
happens to be
x2y3dx
,
x
going from 0 to 1. Now, what do I do with
y3
? You all know how to integrate a function of
x
times
dx
. What do I do with
y3
? What do you think it means?
Student:
[inaudible]
Professor Ramamurti Shankar:
Pardon me? What should I do with
y
? Evaluate
y
on that path at that point. Well, it turns out, throughout this horizontal segment
y
= 0, so this is gone. Basically, the point is very simple. When you move horizontally, you're working against horizontal forces doing work, but on the
x
axis when
y
is 0 there is no horizontal force; that's why there's nothing to do. Now, you come to this segment. I think you all agree, the distance traveled is
J
times
dy
. So, I have to have another segment, the second part of my trip, which is
Fy
times
dy
, and
y
goes from 0 to 1, and the
y
component is
xy2dy
, where
y
goes from 0 to 1. But now, on the entire line that I'm moving up and down,
x
= 1. Do you see that?
x
is a constant on the line so you can replace
x
by 1 and integral of
y2dy
is
y3
over 3.The work done is, therefore, 1/3 joules. So, the work done in going first to the right and then to the top is 1/3. You can also go straight up and then horizontally. By a similar trick, I won't do that now, because I want to show you something else that's useful for you, I'm going to pick another path which is not just made up of
x
and
y
segments. Then it's very easy to do this.
So, I'm going to pick another way to go from 0,0 to 1,1, which is on this curve; this is the curve
y = x2
. First of all, you've got to understand the curve
y = x2
goes through the two points I'm interested in. If you took
y
= 5
x2
, it doesn't work. But this guy goes through 0,0 and goes through 1,1. And I'm asking you, if I did the work done by the force along that segment, what is the integral of
F.dr
? So, let's take a tiny portion of that, looks like this, right, that's
dr
, it's got a
dx
, and it's got a
dy
. Now, you notice that as this segment becomes very small
dy/dx
is a slope; therefore,
dy
will be
dy/dx
times
dx
. In other words,
dx
and
dy
are not independent if they're moving in a particular direction. I hope you understand that. You want to follow a certain curve. If you step to the right by some amount, you've got to step vertically by a certain amount so you're moving on that curve. That's why, when you calculate the work done,
dx
and
dy
are not independent. So, what you really want is
Fxdx + Fydy
, but for
dy
I'm going to use
dy/dx
times
dx
. In other words, every segment
Δy
that you have is related to the
Δx
you took horizontally so that you stay on that curve. So, everything depends only on
dx
. But what am I putting inside the integral? Let's take
Fx
, the
x
component is
x2y3
. On this curve
y = x2
, so you really write
x2
, and
y = x2
, that is
x6
. This
x3
[should have said x6] is really
y3
written in terms of
x
. Then, I have to write
Fy
, which is
x
times
y2
, which is
x4
times
dy/dx
which is 2
x
. So, I get here, from all of this,
(x8 + 2x5)dx
. Did I make a mistake somewhere? Pardon me?
Student:
The second part of this.
Professor Ramamurti Shankar:
Did I, here? Here?
Student:
No.
Professor Ramamurti Shankar:
Oh here?
Student:
[inaudible]
Professor Ramamurti Shankar:
Oh,
x6
, right, thank you. How is that? Thanks for watching that; you have to watch it. So, now what do I get?
x8
integral is
x9
/9. That gives me 1, 9 because x is going from 0 to 1. The next thing is
x7
/7, which is 2 times that. Well, I'm not paying too much attention to this because I know it's not 1/3, okay? There's no way this guy's going to be 1/3, that's all I care about. So, I've shown you that if we took a random force, the work done is dependent on the path. For this force, you cannot define a potential energy whereas in one dimension any force that was not friction allowed you to define a potential energy. In higher dimensions, you just cannot do that; that's the main point. So, if you're looking for a conservative, this is called a "conservative force." It's a force for which you can define a potential energy. It has the property of the work done in going from
A
to
B
, or 1 to 2, is independent of how you got from 1 to 2. And the one force that the class generated pretty much randomly is not a conservative force because the work done was path dependent.
Chapter 4. Cross Derivative Test for Potential Energy Equations [00:52:29]
So, what we have learned, in fact I'll keep this portion here, if you're looking for a conservative force, a force whose answer does not depend on how you went from start to finish, then you have to somehow dream up some force so that if you did this integral the answer does not depend on the path. You realize, that looks really miraculous because we just wrote down an arbitrary force that we all cooked up together with these exponents, and the answer depends on the path. And I guarantee you, if you just arbitrarily write down some force, it won't work. So, maybe there is no Law of Conservation of Energy in more than one dimension. So, how am I going to search for a force that will do the job? Are there at least some forces for which this will be true? Yes?
Student:
The force is always parallel to the path along which you have [inaudible]
Professor Ramamurti Shankar:
No, but see the point is you've got to first write down a force in the
xy
plane. Then, I should be free to pick any two points and connect them any way I like and the answer shouldn't depend on how we connected them. Only then, you can have conservation of energy. I hope you all understand that fact. So, I'm saying, a generic force on the
xy
plane doesn't do that. Then we ask, "Can there ever be an answer?" It is so demanding. Yes?
Student:
Well, in the inverse square force they've got it.
Professor Ramamurti Shankar:
Right, so he's saying, "I know a force." The force of gravity, in fact, happens to have the property that the work done by the force of gravity does not depend on the path. We will see why that is true. But you see, what I want is to ask, "Is there a machine that'll manufacture conservative forces?" and I'm going to tell you there is. I will show you a machine that'll produce a large number, an infinite number of conservative forces, and I'll show you how to produce that. Here is the trick. The trick is, instead of taking a force and finding if there's a potential that will come from it by doing integrals, let me assume there is a potential. Then, I will ask what force I can associate with the potential, and here is the answer. The answer is, step one, pick any
U
of
x
and
y
. You pick the function first. That function is going to be your potential energy; it's been anointed even before we do anything. But then, from the potential, I want you to manufacture the following force. I want the force that I'm going to find to have an
x
component, which is [minus] the derivative of
U
with respect to
x
, and is going to have a
y
component which is [minus] the derivative of
U
with respect to
y
. That is step two. In fact, the claim now is this force is going to be a conservative force. And in fact, this potential energy associated with it will be the function you started with. So, how do I know that?
So, for example, I'm saying suppose
U = xy3
, then
Fx = -dU/dx
, which is equal to
-y3
, and
Fy
, which is
-dU/dy
would be
3
xy2
. The claim is, if you put
I
times
Fx
and
J
times
Fy
, the answer will not depend on how you go from start to finish. So, let me prove that to you. Here is the proof. The change in the function
U
, in the
xy
plane, you guys remember me telling you, is
dU/dx
times
dx + dU/dy
times
dy
. That's the whole thing of mathematical preliminaries which was done somewhere, I forgot, here. It says, here,
ΔF
is
dF/dx
times
Δx + dF/dy
times
Δy
. I'll apply that to the function
U
, but who is this? You notice what's going on here?
dU/dx
times
dx
, this is
Fx,
with a minus sign, that's
Fy
with the minus sign. Therefore this is equal to
-F.dr
. Right? Because we agree, the force that I want to manufacture is related to
U
in this fashion. Now, if you add all the changes, the right-hand side becomes the integral of
F.dr
, and the left-hand side becomes the sum of all the
ΔU
s with a minus sign. Add all the
ΔU
s with a minus sign, that'll just become
U
at 1
-U
at 2. It is cooked up so that
F.dr
is actually at the change in the function
U
. That's if you say, what was the trick that you did? I cooked up a force by design so that
F.dr
was a change in a certain function
U
. If I add all the
F.dr
s, I'm going to get a change in the function
U
from start to finish and it's got to be
U1 - U2
.
So, I don't know how else I can say this. Maybe the way to think about it is, why do certain integrals not depend on how you took the path, right? Let me ask you a different question; forget about integrals. You are on top of some hilly mountain. We have a starting point, you have an ending point, okay. I started the starting point, and I walked to the ending point. At every portion of my walk, I keep track of how many feet I'm climbing; that's like my
ΔU
. I add them all up. At the end of the day, the height change will be the top of the mountain minus bottom of the mountain, the height of the mountain. You go on a different path, you don't go straight for the summit, you loop around and you coil and you wind down, you go up, you do this, and you also end up at the summit. If you kept track of how long you walked, it won't be the same as me. But if you also kept track of how many feet you climbed and you added them all up, what answer will you get? You'll get the same answer I got. Therefore, if what you were keeping track of was the height change in a function, then the sum of all the height changes will be simply the total height change, which is the height at the end minus height at the beginning. Therefore, starting with the height function, by taking its derivatives, if you manufacture a force, this will be none other than the fact of adding up the changes. And that's why this will be
K2 - K1
, and then you will get
K1 + U1 = K2 + U2
. I hope you understand how conservative forces are not impossible to get. In fact, for every function
U
of
x
and
y
you can think of, you can manufacture a conservative force.
So, you may ask the following question. Maybe there are other ways to manufacture the conservative force and you just thought of one, and the answer is "no." Not only is this a machine that generates conservative forces, my two step algorithm, pick a
U
and take its derivatives, every conservative force you get is necessarily obtained by taking derivatives with respect to
x
and
y
of some function
U
and that
U
will be the potential energy associated with that force. So, when that force alone acts on a body the kinetic plus that potential will not change.
Finally, you remember that when the class picked a certain force, which I wrote here, I went on a limb and I said I'm going to do the integral of this force along this path and that path and I'm going to get different answers and show you we have a problem. What if the force you had given me was actually a conservative force? Then, I would be embarrassed because then I'll find, after all the work, this'll turn out to be again 1/3. So, I have to make sure right away that the force is not conservative. How can you tell? One way to say it is, ask yourself, "Could that be some function
U
whose
x
derivative of this was this, and whose
y
derivative was that?" You can probably convince yourself no function is going to do it for you because if you took an
x
derivative you should've lost a power of
x
here. That means, if you just took the
y
derivative to go here, you should have more powers of
x
and less powers of
y
but this is just the opposite way. So, we know this couldn't have come from a
U
. But there's a better test. Instead of doing all that, instead of saying I'm satisfied that this doesn't come from taking derivatives of the
U
by looking at possible
U
s are not being satisfied because maybe I'm not clever enough. There is a mechanical way to tell. The mechanical way to tell is the following. Maybe I want you guys to think for a second about what the recipe may be. If a force came from a function
U
by taking derivatives, as written up there, what can you say about the components of that force, from the fact--yes?
Student:
What is the cross derivative [inaudible]
Professor Ramamurti Shankar:
Right, we know that for every function
U
the cross derivatives are equal but the ordinary derivatives are just the
Fx
and
Fy
; therefore,
d2U
over
dydx
is really
d
by
dy
of
Fx
. And I want that to be equal to
d
by
dx
of
Fy
because that would then be
d2U
over
dxdy
. In other words, if the force satisfies this condition, the
y
derivative of
Fx
is the
x
derivative
Fy
. Then, it has the right pedigree to be a conservative force because if a force came from a function
U
by taking derivatives, the simple requirement of the cross derivatives are equal for any function
U
tells me. See, if I take the
y
derivative of
Fx
, I'm taking
d2U
over
dxdy
. And here, I'm taking
d2U
over
dydx
and they must be equal. So, that's the diagnostic. If I give you a force and I ask you, "Is it conservative?" you simply take the
y
derivative of
Fx
and the
x
derivative of
Fy
and if they match you know it's conservative.
So, I can summarize by saying the following thing. In two dimensions, there are indeed many, many forces for which the potential energy can be defined. But every one of them has an ancestor which is simply a function, not a vector, but a scalar function, an ordinary function of
x
and
y
. Then, the force is obtained by taking
x
and
y
derivatives of that function; the
x
derivative with a minus sign is called
Fx
, and the
y
derivative is called
Fy
.
Chapter 5. Application to Gravitational Potential Energy [01:03:55]
Okay, so let's take the most popular example is the force of gravity near the surface of the Earth. The force of gravity we know is
-mg
times
J
. Is this guy conservative? Yes, because the
x
derivative of this vanishes and the
y
derivative of
Fx
you don't even have to worry because there is no
Fx
; it's clearly conservative. Then you can ask, "What is the potential
U
that led to this?" Well,
dU/dy
with a minus sign had to be
-mg
and
dU/dx
had to be 0. So, the function that will do the job is
mgy
. You can also have
mgy
+ 96 but we will not add those constants because in the end, in the Law of Conservation of Energy,
K1 +U1 = K2 + U2
, adding a 96 to both sides doesn't do anything. So this means, when a body's moving in the gravitational field ½
mv
2 +
mgy
, before, is the same as ½
mv2 + mgy
, after. Now, you knew this already when you're moving up and down the
y
direction but what I'm telling you is this is true in two dimensions.
So, I'll give you a final example so you guys can go home and think about it.
That is a roller coaster. So, here's the roller coaster, it has a track that looks like this. This is
x
, this is the height of the roller coaster, but at every
x
there's a certain height so
y
is the function of
x
and it looks like this. It's just the profile of the roller coaster. But that is also the potential energy
U
, because if you multiply this by
mg
, well, you just scale the graph by
mg
it looks the same. So, take a photograph of a roller coaster, multiply the height in meters by
mg
, it's going to still look like the roller coaster. That is my potential energy for this problem and the claim is that kinetic plus potential will not change, so
K + U
is a constant; let's call the constant
E
.
So, if a trolley begins here at the top, what is its total energy? It's got potential energy equal to the height, it's got no kinetic energy, so total energy in fact is just its height. And total energy cannot change as the trolley goes up and down. So, you draw a line at that height and call it the total energy. You started this guy off at that energy, that energy must always be the same. What that means is, if you are somewhere here, so that is your potential energy, that is your kinetic energy, it's very nicely read off from this graph, to reach the same total. So, as you oscillate up and down, you gain and lose kinetic and potential. When you come here your potential energy is almost your whole energy but you've got a little bit of kinetic energy. That means, your roller coaster is still moving when it comes here with the remaining kinetic energy. You can have a roller coaster whose energy is like this. This is released from rest here. It is released from rest here. That's the total energy and this total energy line looks like this. That means, if you released it here, it'll come down, pick up speed, slow down, pick up speed again, and come to this point, it must stop and turn around because at that point the potential energy is equal to total energy and there is no kinetic energy. That means you've stopped, that means you're turning around, it'll rattle back and forth. By the way, according to laws of quantum mechanics, it can do something else. Maybe you guys know. You know what else it can do if it starts here? Yes?
Student:
It can tunnel.
Professor Ramamurti Shankar:
It can suddenly find itself here and that's not allowed by classical mechanics because to do that it has to go over the hump. Look what's happening at the hump. I've got more kinetic energy than I have total energy. I'm sorry, I've got more potential energy than I have total energy. That means kinetic energy is negative, that's not possible, because ½
mv2
can never be negative. So, quantum theory allows these forbidden processes and it's called tunneling. But for us, the roller coaster problem, you will just turn around. There's one thing I want you to think about before you go. You should not have simply accepted the Law of Conservation of Energy in this problem because gravity is not the only force acting on this. What else is acting on this roller coaster?
Student:
No friction.
Professor Ramamurti Shankar:
Pardon me? No friction, then what?
Student:
The normal force.
Professor Ramamurti Shankar:
The force of that track. Look, if I didn't want to have anything but gravity, here's a roller coaster ride you guys will love, just push you over the edge. That conserves energy and it's got no track and it's got the only gravitational force and you can happily use this formula. Why am I paying all this money? Because there's another force acting on it, but that force, if it's not frictional, is necessarily perpendicular to the motion of the trolley, and the displacement of the trolley is along the track, so
F.dr
vanishes. So, I will conclude by telling you the correct thing to do would be to say
K2 - K1
is the integral of all the forces, divided into force due to the track and the force due to gravity. The force due to the track is 0. I mean, it's not 0, but that dot product with
dr
would be 0, because
F
and
dr
are perpendicular. For that reason, you'd drop that and the force of gravity is cooked up so then it becomes
U1 - U2
and that's what we used.
Okay, one challenge you guys can go home and do this, take any force in two dimensions,
F
; it is parallel to the direction where you are measured from the origin times any function of the distance from the origin. Show, convince yourself that this force is a conservative force by applying the test I gave you and the trick is to use
x
and
y
instead of
r
. Take this force, write it now in terms of
x
and
y
, take the cross derivatives and you can see it's conservative. So, any radial force, yep?
Student:
[inaudible]
Professor Ramamurti Shankar:
Oh, here. This is the force to which you should try your thing and gravity is a special example of this. Okay, judging from the class reaction, and the stunned and shocked look, a lot of you people, maybe this material is new, so you should think about it, talk about it, go to discussion section, but this is the level at which you should understand energy conservation in a course like this.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_06_092506.mp3) |
