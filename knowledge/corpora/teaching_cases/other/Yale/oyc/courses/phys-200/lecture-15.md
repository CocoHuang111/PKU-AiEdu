> 检索摘要：Open Yale Courses「PHYS 200 Four-Vector in Relativity」。主要内容：继续讨论相对论中的四维矢量，这次聚焦粒子的能量-动量四维矢量，并说明其不变性来自静止质量在坐标变换下保持不变。页内标题：Lecture 15 - Four-Vector in Relativity；Overview；Lecture Chapters。分隔线后是英文原文，未翻译、未改写。

- Source: https://oyc.yale.edu/physics/phys-200/lecture-15
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 15 - Four-Vector in Relativity

### Overview

The discussion of four-vector in relativity continues but this time the focus is on the energy-momentum of a particle. The invariance of the energy-momentum four-vector is due to the fact that rest mass of a particle is invariant under coordinate transformations.

### Lecture Chapters

1. Recap: The Four-Vectors of Position, Velocity and Momentum in Space-Time
2. The Energy-Momentum Four-Vector
3. Relativistic Collisions
4. Law of Conservation of Energy and Momentum Using the Energy-Momentum Four-Vector

1. 0
2. 953
3. 1940
4. 2469

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 15 - Four-Vector in Relativity
Chapter 1: Recap: The Four-Vectors of Position, Velocity and Momentum in Space-Time [00:00:00]
Professor Ramamurti Shankar:
This is the last and final chapter of this subject, and I think it's, again--we're starting by backing off a little bit towards the end of last class. I think that there are maybe parts of it were maybe difficult for you to follow.
Let me remind you of what we were trying to do. We had learned that space-time is described by four coordinates, so that if you're following some particle or some event, you label it with four numbers
c
,
t,
x
,
y
and
z
, which I want you to let me combine into the single vector
r
. They are written as
x0
,
x1
,
x2
,
x
3. Now, I'm of two minds about
x2
and
x3
; sometimes I carry them around, sometimes I don't.
x1
is just our familiar
x
;
x2
is
y
and
x3
is
z
. It's possible to arrange all the motion to take place in the
x
direction, in which case
y
and
z
don't change when you go from one frame to the other, so I don't usually bother with that. But sometimes I put it back because if you have only two components,
x0
and
x1
, you might say, "Hey, the world is two dimensional." So, I want to keep reminding you now we think of it terms of four dimensions. So, at least for that reason sometimes they carry all the three components of position, sometimes only one. But I'm sure you guys can figure out from the context which is which.
So, going back to the simpler situation of only
x
and time, the point of those coordinates is that if you went to a moving frame,
x1
′ will be
x1
βx0
, divided by the square root. And
x0
′ will be
x0 - β
times
x1
, divided by that square root, where
β
is
v
/
c
. Sometimes it's useful to introduce
γ
, which is [reciprocal of square root of ] 1 - u2/c2. Also to prevent all confusion,
u
will be the velocity of your frame relative to mine.
v
will stand for the velocity of some particle that we are both studying. So, let's reserve the symbol
v
for motion of actual particles, which is why we are there. We are all observers but we're observing something. That something has a velocity that I'll call
v
and you will call
w
, and
u
is the speed relative to your frame and my frame.
All right, so this is the notion of space-time because space and time are getting mixed up when you go to a new frame of reference. But even in this world where nothing is sacred, the following combination is very important, which we denote as
X
dot
X
. There's a new dot product now in space-time. The new dot product will be the square of the time-like part minus the square of the space-like part. If you wanted to bring in all the components of space-time, then you can modify it to
x02 - r
dot
r
.
r
dot
r
will be
x2 + y2 + z2
. So, you can use either notation. Whenever possible I just keep two, but you've got to remember, this is why it's a four-dimensional dot product. And this is the same for all people. So, I can calculate it, you can calculate it, our
x0
and
x1
will differ, but it's the property of the Lorentz transformation, that if I square this guy and subtract it from the square of this guy, on the right-hand side some magical things will happen and I'll get the same combination without the primes. That's like the length of the vector. And that's called the space-time interval. Let's call that
s2
, the space-time interval.
If it took two events separated in space by
Δx
and separated in time by
Δt
, then we like to use the symbol
Δs2
for the space-time interval. That's the same thing applied to the differences rather than to the coordinates themselves. And this is invariant. Invariant is a term mathematicians use for saying same for all people, or unaffected by Lorentz transformation. It's the analogue of how far you are from the origin in the old days, when I took two frames, one which is the standard
xy
, the other is the rotated
xy
. If you go to the rotated frame, the components
x
and
y
change, but how far you are from the origin, or what's the length of the vector is the same for all people. More generally, the dot product of two vectors is invariant under rotations, and this is the new dot product. I use the symbol dot product, but I don't draw arrows, because if I don't draw any arrows and use capital letters, it means it's a four-vector. That's the
X
vector.
Then I said, "Let's try to reason by analogy and try to invent a momentum vector." How did we invent the momentum vector in the old days? We said, let the particle move a distance
Δr
, vector
Δr
, in a time
Δt
, and a divide by
Δt
, and take some limit. But I know this is a vector because
Δr
is a difference in two vectors. Where the particle is now, and where it is later, the difference of two vectors is also a tiny vector going from here to there. Dividing by a scalar, by a scalar I mean something that is not affected by rotations, means taking a vector and multiplying it by some number. Therefore, that's also a vector, so this ratio is also a vector, and the limit of the ratio is also a vector. I'm sorry, I forgot the mass here, and we call it the momentum vector. So, you can manufacture vectors starting with a position vector by taking derivatives with respect to something like time that is the same for all observers, where observers, I meant in the old days, people with an axis rotated anyway you like.
I wanted the same thing now in this present problem, but I now want to define obviously a four-dimensional vector. So, to do the four-dimensional vector, my plan is to define something called momentum, which is now going to be the change in this fourth position divided by something. The question is, "What do I divide it by?" I cannot divide by
Δt
. In the old days
Δt
was a sacred number, same for all people. Now
Δt
is like
Δx
or
Δy
, it's one of the components, and you don't divide the change in the vector components by the change in one of the components to get a velocity. You've got to divide by something that's going to play the role of time, and have the same value for all people. Well, we sort of know what that quantity is. Obviously, if a particle is moving from here to here in space-time, this is
x0 = ct
and this is
x1
. It moves the distance
Δx1
in a time
Δt
, and we know that for this piece of its motion the following quantity,
Δs
, which is [root of]
c Δt2 - Δx2
, is the same for all people. So, I should really be dividing by this.
Let me write it slightly differently as
c Δt
times the square root of 1 minus
Δx
over
Δt2
times 1/
c2
. So, we are asked to divide by this crazy thing. Well, let me write this crazy thing as
c
times something I want to call
dτ
, is
dt
times the square root of 1 minus
Δx
over
Δt2
times 1/
c2
. Then I said, "We can give a meaning to this thing." In fact, let's take the derivative with respect to
τ
not
s
. They differ only by this factor
c
, which is a constant so it doesn't matter.
τ
has units of time, and you can ask, "What does that time stand for?" It's not the time according to me, but I argued that it's the time according to the particle. Why? Because you can evaluate this quantity in any frame you like. So, go to the frame moving with the particle. If you're moving with the particle, and if you're here now and there later, later is certainly later, but here remains here for the particle. It doesn't move in its own frame. So,
Δx
will vanish, therefore
Δs
simply reduces to
c
times the time elapsed according to the particle. So,
dτ
is the time elapsed according to the particle itself. According to the particle. That's what we're going to divide by.
So, it's a very clever way to circumvent the question of what should I take the derivative respect to, my time and your time all are variable, we don't agree on it. But let's ask how much time elapsed according to the one thing we are studying, and let's divide by that time. That answer will be the same because you and I may not agree on how long it took to go from here to there, but we can all ask how long did the particle say it took to go from here to there. We're talking about the same thing, and we'll get the same answer. To get the particle time you've got to take the time according to you and me and multiply it by this factor. This factor, by the way, is nothing but usual time dilatation. Because the particle says it took time
dτ
because the clock has slowed exactly this amount, I will say it took longer by this amount.
So, let's rewrite this in a way that's going to be more helpful to us. Take the ratio and write
dt
over
dτ
is 1 over the square root of 1 minus
v2/c2
. I'm going to use that in a minute. That just says the time according to me and the time according to the particle are related by the time dilatation factor that's controlled by the velocity of the particle. Now, we are ready to define the four-momentum
p
. The four-momentum
p
is going to be
m
times
dx0/dτ
times
mdx1/dτ
. I'm not going to bother with the other components. You can always put them back. But
x0
you remember was
ct
. So, this really becomes
mdt
divided by
dτ
,
mdx
divided
dτ
. This is guaranteed to be a four-vector. That means, if you know the components of this in one frame of reference, and you call one of them as
p0
, and you call this one as
p1
. Then, in a frame that's moving relative to your
x
speed
u
, our
p0
′ will be
p0
minus
β
times
p
1 over the square root, and
p1
′ will be
p1
minus
β
times
p0
over the square root. It will transform just the components of
x
. Yes?
Student
: For
p0
, where does the
c
go?
Professor Ramamurti Shankar
: Where did the
c
go? No, it did not go, you're quite right. The
c
,
x0
the
ct
, you're quite right. It is
c
times
dt
. You need that; then, this is correct. So, we've got a four-vector, but we don't know what it means. Because we don't know what
dτ
means. Of course it's the time according to the particle, but I don't care about the particle. I'm studying this particle, I've got my own clock, I've got my own meter sticks, I want to think in terms of time according to me. Period. Well, we can do that. We can do that by going to anything where you take a derivative such as
dx1/dτ
and you can write is as
dx1/dt
times
dt/dτ
.
dx1dt
is something we understand, it's just the velocity according to you and me. If you use that rule here, you will find the momentum has got components
m
times
c
,
dt/dτ
is
dt/dt
, which is 1, times
dt
divided by
dτ
, which is this factor here. And the second thing will be
mv
divided by the same thing. In other words, you can trade
τ
derivatives for
t
derivatives everywhere, provided you attach this factor. That's the ratio of the
τ
derivative to the
t
derivative.
So, now I have a four-vector. I still don't know what it means, but at least it is written in terms of things with a direct operational significance for me. I see a particle moving, it's got a velocity, put that in and I get this thing. Apparently, the relativity theory says this should play the role of momentum, but a four dimensional momentum in your new world. If you want to bring the other components, we'll put an arrow, you can keep it or leave it; it doesn't matter.
Now, notice once again that--Okay, I'll continue some more. I've already done this last time, but let me remind you. We looked at this guy and said, "Look, at smaller velocities, when
v/c
is very small, the denominator is just 1. Numerator is
mv
. And then I said, "Uh-huh, that's the momentum." So, it must be that with all these factors, this is the momentum in the new relativistic theory. In the new relativistic theory momentum is not just mass times velocity. Mass times velocity divided by all this stuff. The theory says, "Use that as your momentum." That's good. Then, we say, "Okay, that's my momentum, who is this?" I expanded this out for small velocity. If you put velocity equal to 0, you get
mc
. That looks like just the mass and we don't know what that corresponds to. It's the mass, nothing kinematical. But if you expand the square root a little further out to one more term, we found that the 0 component,
p0
, looks like
mc
times 1 plus
v2
over 2
c2
plus dot dot dot. That becomes
mc
+ 1/2
mv2
times 1 over
c
plus dot dot dot. And now I finally have something I understand, because ½
mv2
is familiar kinetic energy. But I don't like this annoying
c
here. If I multiply both sides by
c
, I learn that
c
times
p0
is
mc2
plus ½
mv2
, plus more stuff that's more and more powers of
v
over
c
. But this I argue. If that's the kinetic energy, everything is an energy formula, so the whole thing stands for energy. So, I learned that the first component, of
P
is energy divided by
c
. So, I come back here and I write this as
E/c
.
Chapter 2: The Energy-Momentum Four-Vector [00:15:53]
So, for all of you, or for many of you who found some of this mathematics difficult to follow, it depends. For me it was love at first sight. This is really when I said, "I want to go into business." For some reason this worked for me. But it doesn't matter. What you have to know is what I'm going to tell you now. Operationally, I'm not going to hold you responsible for this part of the material at all. For me, it's part of explaining how logically starting with the very first axiom--first two axioms you can deduce everything. But now, I want to tell you operationally what you guys are supposed to know. You are supposed to learn the following two things. In the old days, we had time and we had space; they have been united into a single quantity; (
ct,r
), which we write as
x0
,
x1
etcetera. In other words, the three components of a vector joined with one quantity that looked like a scalar together to form a four-dimensional object. Now, we are learning that there is another four-dimensional object, one of which is just the momentum, and the other is energy divided by
c
. And we want to call that as
p0,
p1
etcetera. Again, the familiar momentum, which is a vector, joined with another quantity, which the best way to think about it is kinetic energy, plus rest energy, plus other corrections. But it's a scalar; it doesn't depend on orientation of axis in the old days. But now under Lorentz transformation, namely, when you go from one frame to another,
E
and
p
will all mix with each other just like
x
and
t
will mix with each other, but this is the new four-vector. It's called the energy-momentum four-vector. Just like that's called the space-time four-vector. This is the energy-momentum four-vector. So, all over relativity you will find three objects, which used to be part of a vector, will combine with the fourth one, which used to be a scalar; together, they'll form a new four-dimensional vector.
So, we should know the following. When we are studying particle dynamics, we have to know in more detail--in fact, let me dedicate a whole board to that, it's very important. The new definition is that it's
E
over
c
and
p
. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: Well, it looks like
mc2
plus ½
mv2
plus other stuff, right? So, I recognize ½
mv2
as an energy; then, the other powers
v4/c4
, they're all corrections obviously to the energy at higher velocity. Just like momentum, even in relativistic theory was not
mv
. It started out like
mv
, but when you expand the denominators and powers to
v/c
you get more and more corrections. I identify this as an energy because if I go to very low velocities, it reduces the rest mass, which is never going to change, plus a ½
mv2
, which played the role of kinetic energy.
That's why it has units of energy, and one term in it looks like energy. So, the whole thing, the theory is telling you, it's all just the energy of the particle. In the old days when velocities were very small, we saw only that two terms are written: ½
mv2
and
mc2
.
mc2
we didn't bother with because it doesn't change in any collision. You add the
mc2
before, each particle has got its own
mc2
before and after; they simply cancel. So, the ½
mv
squares before and after that would equal, and we use that to solve collisions. Now we will be told you should use the conservation of this energy and the conservation of this momentum in a collision.
Okay, so the first thing is this is
E
and this is
p
, and if anyone says, "What is
E
?" It is
mc2
divided by 1 minus
v2/c2
, and
p
in one dimension is
mv
divided by 1 minus
v2
/
c2
. This you must know. So, momentum and relativity looks a bit like the old momentum but it's got this ubiquitous factor. And energy looks really weird; doesn't look like anything on Earth, but if you expand this in powers of
v
, you will see the terms we wrote down. Rest energy plus everything else you can call energy of motion, and the first term of the energy of motion is the familiar ½
mv2
. In other words, this is how the world always was. It was revealed to us in the old days when we only looked at low energy particles as
mc2
+ ½
mv2
. And we couldn't see the dot dot dot terms because
v/c
was so small, the fourth power and sixth power and eighth power of
v/c
were too small for us to detect.
Likewise, the momentum of a particle was never
mv
; it was
mv
divided by all this. But for small values the
v/c
looked like that, and they thought, "Hey, that's what is really happening." So, we were looking at an approximation to these quantities in the old days when velocities were small, and as velocities go up, those quantities aren't useful, this is what the theory says should play the role of the new four-momentum. So, the significance of this being the forward momentum, first of all is what is written in the top right corner there; namely, if you know the energy and momentum in one frame, you can find the energy and momentum in another frame of reference moving relative to me.
For that purpose, you should take the energy and divide by
c
, you should call it
p0
, the momentum can be left as it is, and this will behave like
x0
, that will behave like
x1
, under Lorentz transformation. But there are other consequences of the fact that
P
is a four-vector. The first consequence it this: you remember the dot product of a vector with itself is the same for all observers. So, what's the dot product of
P
with itself?
Well, before I do that, let me remind you in general, in relativity you will have four-vectors: (A) you'll have one part that looks like time, and one part that looks like an ordinary vector. And (B), is another four-vector, it's got a part that looks time and another part that looks like an ordinary vector. It's a union up of former vector with a former scalar. And they will transform under Lorentz transformation just like
x0
and
t
. But the following quantity
A
dot
B
, which is
A0 B0
minus the usual dot product of the spatial components, is invariant. That means all people will agree on this quantity. And a special case is
A
dot
A
, which equals
A02
minus the length of the vector part, which for our purpose will be just
A02
A12
. This is all reasoning by analogy. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: No. Quaternion are a slightly different object. You can form with these four numbers something that you may call a quaternion. Right. They were invented before relativity by Hamilton, and they are of great mathematical beauty. They're a generalization of numbers. You know, we generalize real numbers to complex numbers; then, we went from complex numbers to things called quaternions. They are also numbers; you can multiply them by each other, but the product
AB
differs from the product
BA
. They're called hyper-complex numbers where the order in which you multiply them matters.
Okay. So, now let's ask what is the invariant length square of the momentum four-vector with itself. That means, you've got to do
p02 - p2
. That means you are trying to take
m0
--I'm sorry, you're going to take
mc
over this factor square, minus
mv
over this factor square. Well, let's try to do this in our head, guys.
m2
is going to come out of the whole thing, you agree? On the top, I have got 1 over 1 minus
v2
over
c2
, yet I have minus
v2
over 1 minus
v2
over
c2
, so they will all cancel giving you
mc2
. Uh,
m2c2
.
[Note: Here, the Professor has started dropping the subscript on
m0,
]. So, the four-vector of any particle has a length that does not at all depend on how fast it's moving. It depends only on this.
When you take a velocity vector for a particle, it doesn't have a fixed length. The particle can be moving slow, it can be moving fast. So
vx2 + vy2
could be whatever you like depending on how it's moving. But this relativistic length square of a four-vector is independent of velocity because the velocity here when combined with this number just cancels out. Well, that's just the way it is. Now, if you're not good in algebra, there's a shortcut for finding this. Let me tell you what the shortcut is, and we love the shortcuts because they're very helpful. And the moral of the story is also illustrated by the shortcut.
I want to find
P
dot
P
. It's an invariant because it's like a dot product, so anybody can calculate it. How about somebody riding with the particle? If you're riding with the particle your 0 component is
m0c
, is
mc
, there is no velocity for you, and you have no momentum. As the particle has no momentum as seen by the particle so the components of the vector
P
become
mc
and 0. What's the length square of this vector? Well, it's the square of this guy and case closed; there's nothing here to subtract from here. That's a quick way to verify that this length of vector with itself is in fact
m2c2
. In other words, the trick is ride with the particle and calculate the vector. Then, the vector has only one component, namely
mc
. It doesn't have a spatial part because it's not moving according to itself. That's where
P
dot
P
is
m2c2
. So, people write it also as follows: remember
p0
was
E
over
c,
this is just
P2
is
m2c2
. This is one way to write it explicitly, but here is how people write it: multiply both sides by
c2
and write
E2
is equal to
c2p2
- m2c4
; that deserves a box. That's how we remember it. I have just rearranged this equation.
P
dot
P
is
m2c2
. By definition
P
dot
P
is the time-like component square minus the spatial component square. We agree the time-like part is
E/c
; the spatial part is just the momentum. So, I've just rearranged it to get this. And it says the energy of the particle depends on its momentum, if it comes complete to rest, you kill this term, that's
E = mc2
; that's the rest energy of a particle.
Now, I am almost finished with the kinematics except for one thing. There are strange particles in the world called photons. A photon has no rest mass; therefore, if you naively went by any of these formulas, if you killed the mass of the photon, you might think energy and momentum vanish because
m
is going to 0, but we all know enough mathematics to know that if it's 0 on the top, you could beat it if there's a 0 in the bottom. That will occur only for
v = c
. So, particles moving at the speed of light do have energy and momentum, but they don't come from a mass divided by something, or mass times velocity divided by something. They simply have energy and momentum that obeys this equation without an
m
on the right-hand side. For a photon,
E2
equal to (
c
times
p
)2 is what a photon obeys. So, photons can have energy, and photons can have momentum, but their energy will be
c
times their momentum so that if you find the invariant square of the photon momentum you will get 0. So, photons are particles whose momentum square is 0. But the square is the four-dimensional square with the time square minus the spatial square.
So, let me summarize once more for people who may not want to follow every detail. The practical part of what you must understand from what I've been teaching you is that when you study a single material particle, which has a mass, so that it can be brought to rest and made to sit on the table, we associate with that at four-vector. The first part of that is the energy over
c
; the second part of that is called the momentum, and the explicit formula for these are
m0
, or
mc
divided by this and
mv
divided by this. And one can explicitly verify that
P
dot
P
is
m2c2
. This is a summary of all that I've said. If you don't know anything at all, know this. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: Yes. A capital
P
without any arrows on it is supposed to be a four-vector, and the dot product of it is defined as the square of the first component minus the square of the second one. That is correct. And for photons, we always like to use the symbol
K
for the momentum of a photon rather than
P
. Luckily, people agreed more or less by convention, photon momentum is called
K
, and it's called
Q
by some people, but we call it
K
. And the energy of the photon is when we call , the momentum of the photon is going to be called
k
. And the condition is
= kc
. And there's' the condition
K
dot
K
= 0.
K2
if you like, shorthand for
K
dot
K
, is 0 for photons. A photon is a particle whose square of the four-momentum is 0. Material particles that can come to rest have a square of the fourth momentum, which is
m2c2
. This is something you have to know.
Another thing you have to know is that when I write them in this notation as four-vectors, you should know the following: if you know the components,
p0
and
p1
in one frame, and you move relative to
S
with speed
u
,
p0
′ and
p1
′ will be related to
p0
and
p1
by the Lorentz transformation. Just like
x0
′ and
x1
′ are related to
x1
and
x
by that formula on the top left. I'm going to do a lot of problems for you so you get used to doing relativistic kinematics.
Last thing I want to tell you is why do we take this definition of momentum. Okay, you agree with the theory naturally gave out something that it said deserves to be called momentum. But what's so nice about this? Why is it important that the momentum-energy form a vector? I'm going to give you a reason for it, and try to follow the reason. The whole advantage of energy and momentum--What is the big deal about energy and momentum, let me ask you that. Yes?
Student
: [inaudible]
Chapter 3: Relativistic Collisions [00:32:20]
Professor Ramamurti Shankar
: They are conserved. They were not useful unless the special utility came from the fact they're conserved. So, you can put a restriction on possible collisions. You add the momentum before, it's got to agree with momentum after. You add the energy before, it's got to agree with the energy after. Of course, in relativity, energy and momentum have been assembled into four-vector, so conservation of momentum will mean really four equations. The zero part will be the energy before, will be the energy after, and the three special parts will be
x
component and momentum. Before will be
x
component after and so on. That's all very good, but you've got to make sure that if a momentum is conserved for me, forward momentum, it must also be conserved for you. There's no use having a quantity that's conserved for me and not conserved for you. So, by the time you bring up something and say, "We're going to use it as a conserved quantity," you've got to make sure the conservational law is not limited to one observer. And that's what I want to show you. I want to argue without writing any questions that if energy and momentum are conserved for me, they are going to be conserved for you, because they are vectors.
Let's understand why. Suppose you've got a collision; a lot of particles come in; one particle brings momentum-energy
P1
, other one brings in energy and momentum
P2
. And at the end of the collision maybe they become particle 3 and particle 4 and particle 5. In relativistic theories, if two particles come in, you can have 36 particles coming out. In fact, that's why they built accelerators. If two went in and two came out, it's a waste of time. You can smash any two things and with that energy you can produce matter. So, it's not a mistake I've made. I do mean that sometimes two can go into three, or four or five. Let's take an example where this is true.
Each
P
is a four-component object like this. Suppose I say incoming equals outgoing. Now, if you see the whole collision from your frame of reference, then I maintain that the numbers you get,
P1
′ and
P2
′, will also equal
P3
′ plus
P4
′ plus
P5
′. That's guaranteed, and I want to tell you why. Suppose these were ordinary vectors, and let me make life simple by saying that
P1 + P2
became
P3
. What that means is one vector,
P1
, another vector,
P2
, added up to one vector,
P3
. Except these are not ordinary arrows, these are arrows in four dimensions. The fact that two arrows add up to a third one, are equal to a third one, means they form a triangle. Now, if they can form a triangle for me, and you can stand on your head and do what you like, it will still be true. Even though it looks like this, it is still true that this guy plus this guy is equal to that guy. If two vectors add up to a third one; namely, if a sum of two vectors is equal to another vector; namely, the left-hand side vector is equal to the right-hand side vector, going to a rotated frame will continue to say that the rotated vector is equal to the rotated vector. That's because equal vectors upon rotation will remain equal vectors. That's the whole point. The total incoming momentum four-vector, call it
P
incoming, and this is the outgoing momentum, call it the
P
outgoing. If
P
incoming is equal to
P
outgoing for me, so two vectors that equal in space-time, for the rotated observer they will be equal.
Do you understand why? Because my total incoming vector will undergo Lorentz transformation to become your incoming vector. My outgoing vector will undergo Lorentz transformation to find your outgoing. But if the input of the Lorentz transformation is the same, the output will also be the same because you will be putting the very same numbers to get out the output numbers. That's why it's very important that this momentum that we have be used, because it has a chance that if it's conserved in one frame, it's conserved in all frames. If you went and said, "You know what? I don't like your formulas. I'm really wedded to this formula for momentum," what you will find is that even if it's conserved in your frame of reference, in a different frame of reference, that combination, sum over
mv
, will not be conserved. Okay, that's the final property of four-vectors you've got to use. Again, if you don't follow the details, you must know that in collisions that we are going to study we will add up all the [energy-momentum] four-vectors coming in, we'll equal them to all the four-vectors going out. That's it.
So, now I'm going to do sample problems to give you a feeling for that. So, as usual, they will start out with the simplest one and then try to make it more complicated. So, the first problem is this. I'm standing here, I've got some mass
m
, and a photon is coming towards me with some momentum
P
. And this hits me on the face and I absorb the photon. It's completely possible for the atoms forming the body to absorb a photon. They absorb it; so in the end there is no photon. There is me, but possibly with a new mass,
m
′. In relativistic collision, there is nothing called inelastic collisions. Remember the old days when one thing came and stuck to another thing, and they moved together? Momentum is conserved, but energy is not. There is no such thing. Energy will always be conserved in relativistic theories. In other words, even though this will become a single unit, you might say, "What happened to the energy? Previously, I had a moving photon, I got nothing moving here." Well, first of all, I will be moving; secondly, I will have more mass. The best thing is to consider two particles coming in opposite directions. They collide and form a new mass. In relativity, there is no momentum in the final particle, it is not moving at all. But it will be more massive than before, and that extra mass times
c2
will be the extra energy brought by the particles that are formed.
So anyway, the question here is, "What is
m
′ ?" That's what we have to figure out. So, the equation we will use is, I will call my momentum as
P
. I will call
P1
as the initial one, and
P2
as the final one. Let's write down all the equations we can; the only equation in town is
K + P1 = P2
. Everybody is a four-vector, so don't be fooled. It's four equations. But in this problem--;luckily, since there is no motion perpendicular to the
x
axis, we can have this
x
momentum; there's no need for
y
and
z
. Because the photon comes this way, and I can start moving this way, but all the action is in the
x
direction. So, here it will be actually two-dimensional vectors and not four. There's nothing vertically before or after, it will be 0 = 0. So, what are those equations? Before you do that, let's write down the momentum of the photon first. Momentum of the photon has got some energy [should have said
p0
]
/c
, and it's got some momentum
k
, where
= kc
, you've got to remember that.
P1
has got an energy which is
mc
, and no spatial momentum because I'm not moving. At the end of the day
P2
, I am moving, but I also have a new mass, and I have a new velocity, which we don't know, and I have
m
′
v
divided by the square root of 1 minus
v2
/
c2
. Now,all of you should be able to write this part down. If you're not, you should take a minute, you should think about it, you can stop me, you can question me. But if you cannot do this, you cannot do any of the problems. You've got to think, "Would I have done this? Does it make sense to me?" The bookkeeping is all in the top. When you've got a material particle, it's first term, 0 component, will be
m
times
c
divided by the square root of all those things. But if the particle is at rest, you only have
mc
. There is no momentum. The final object, me--After I got hit by the photon, I am recoiling; so, I will have a velocity. I don't know what it is, but my energy in terms of that, the first term,
p0
will be this; this will be
P1
.
Chapter 4: Law of Conservation of Energy and Momentum Using the Energy-Momentum Four-Vector [00:41:07]
Now, the Law of Conservation of Energy and Momentum, namely
K1 + P1 = K2 + P2
, will really be saying all the energy parts of the 0 components will add up before and after, and the first components will add before and after. In other words,
/c
plus
mc
, will be equal to
m
′
c
over this. Then,
k
plus 0 will be equal to
m
′
v
divided by this. This is not any different from the old days. You had Law of Conservation of Momentum, you had Law of Conservation of Energy, except energy is not ½
mv2
; energy is this crazy thing. Plus, even if a particle is not moving, don't forget to give it
mc
as the energy; that's the new part. So, what is the question I asked you? I said, "What is
m
′." So, your job is to take these two simultaneous equations, this one and this one, and solve for
m
′. So, what should I do? Can you think of a strategy that will give me
m
′ ?
Student
: [inaudible]
Professor Ramamurti Shankar
: Into this one here? Yes, you still have to solve for
m
′, and you also don't know the velocity here. Remember, you have to solve for the velocity, and you have to solve for the
m
′. If you say what are the unknowns and what are the knowns, let's be very clear. The photon has a known momentum and known energy--that's given to you. Initial me has a mass
m
, that's given to you. Your job is to find the unknown mass
m
′, and the unknown velocity. Two equations for two unknowns, but they're not simple linear equations where you can add and subtract. The simple linear equations are multiply this by three, multiply that by four and subtract, and you'll get what you want. But it's more complicated. The trick that you really want to use is the fact that for any particle, if you took the square of the 0 component, subtract from it the square of the spatial component, the answer will be
m
′ square
c2
. So, I'm saying: this square minus this square will be
m
′ times
c2
, and that you get by taking the square of this minus the square of this. You can juggle that, but I'm not going to do it that way, I'm going to show you a much more efficient and rapid way to do this.
So, let's do it the more efficient way, so let me come down here so you can see. Here is a shortcut. The shortcut is to work entirely with four-vectors and four-dimensional dot products, and don't get down to the ugly business of writing each component. We know that
P2
is
P1
plus
K
, right? And who are we after? We're after
m
′; then we remember that
P22
, namely
P2
dot
P2
is equal to
m
′ square
c2
. Yes? So, the question you are asked is--No one asked you how fast I am moving after I got hit by the photon; you're only asking me what is my new rest mass. See, I've swallowed a photon, so I weigh more; it's really that. How much more do I weigh is the question; namely; what is my rest mass. Namely, I swallowed it, and I recoiled, and if you travel with me and find me at rest, what mass
m
′ will you measure? So, no one's asking me my velocity of recoil
v
. So, you shouldn't bother to calculate that. You could if you wanted to, but no one is asking you that. So, go directly for
P22
. So, the quantity we're looking for is
m
′ square
c2
. That's got to be
P1 + K
, the whole thing square. Well, do the old algebra. That's equal to
P12 + K2
plus twice
P1
dot
K
. Okay, now let's see if I can do what we do next. Would you like to guess? Yes? No? Do we know any of these quantities? Do we know anything about the three terms I've written here? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
:
K2
= 0 because of what?
Student
: [inaudible]
Professor Ramamurti Shankar
: For a photon I told--For any particle the square root of its momentum is really the square root of its mass times
c2
. For photons, I told you long back,
K
dot
K
is 0. You don't have to worry about that. How about the square of the momentum of me? Well, that was my rest mass before, times
c2
plus 0. Now,
P1
dot
K
you've got to be careful. That dot product means--let me write down the vector of
P1
and
K
for you.
P1
was
mc
and 0, and
K
was /
c
, and the spatial momentum, where was equal to
kc
. Remember that? For a photon, once you pick the energy, you have no choice with the momentum. The magnitude of the momentum has to be the magnitude of energy divided by
c
. So, let's take
P1
dot
K
; let's try to do
P1
dot
K
. Remember the dot product of two vectors is time times time.
mc
times over
c
minus space dot space, that was 0. So, I cancel that, and I find it's really
m
. And that's equal to
m
′
c2
. Yes?
Student
: Can you just remind me what the stands for again?
Professor Ramamurti Shankar
: Yeah, the photon, remember the four-vector's first component is energy over
c
. Second component is the momentum. It's traditional to call the energy of the photon by the symbol
ω
. And it's traditional to call the momentum of the photon, the usual momentum, by the symbol
K
. And that's very helpful; otherwise, you're going to have
P1
and
P2
and
P1
sub-0 and
K1
sub-0, too many indices. So, what we're trying to do is whenever we write a
K
whose components are and little
k
, we know we're talking about a photon. And whenever I write a
P
, I know I'm talking about the electron. So, is just the energy of the photon. So now, if I cancel all the
c
squares, then I get
m
′ square plus
m2
plus 2
m
/
c2
. Now, you can take the square root, if you like, and that's the answer.
So, my mass would have gone up. You might think, "How much would the mass have gone up?" First of all, this guy swallowed a photon of energy , so maybe that energy over
c2
will be the change in mass. That is not correct, and you've got to think about why that is not the answer. Why is that wrong? Why doesn't the photon energy turn into my extra mass? Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: In other words, when I absorb the photon, I also have to recoil to conserve the momentum of the photon. Consequently, my final energy will equal old energy plus photon energy, but that does not mean all of it is rest energy because there's some energy of motion. So, you've got to make sure that in the end you calculate it so that the total energy is balanced, but it's not contained in rest mass. Because you produce the [extra] rest mass, and you also move the rest mass. And for all of that you've got only the energy of the photon to work with.
Okay, so this is one problem. I was going to do one or two more, but I want to make sure you guys are following; I just don't know. See, if I ask you what you would do next, if you have some idea, then we can proceed, but if you don't know, maybe we should slow down. And you've got to talk about which part of it you find more difficult. So, let me say a few things. And the first time you hear something that you find difficult, you've got to put your hand up, okay? Otherwise, you're not going to make progress. The first thing I say is this: particles of mass have an energy and momentum that depend on their velocity and rest mass as given by the first equation. And the energy and momentum are assembled into a four-vector, the first component of which is
E/c
, the second component is just the momentum. That much you should know. Secondly, if you took the dot product of that vector with itself, and the dot product is defined to be Lorentz invariant, so that it is the same for all people, that's
p02 - p12
, you'll always get
m2c2
for any particle of mass independent of its state of motion. And the simplest way to remember that is to evaluate the dot product in the frame moving with the particle. In that frame, it only has a
p0
, which is
mc
, and doesn't have a spatial momentum; so that's got to be the answer.
Second thing, when you deal with photons, they're a little tricky. Photons have energy, photons have momentum, but energy is not mass times some velocity square over 2 etcetera. They have no mass, but they have energy and they have momentum, and the condition of the photon is that the energy must be momentum times
c
. That will make sure that
K
dot
K
is 0. Because for a particle of mass
m
, I showed you the relation,
E2
= (
c
times
P
)2 +
m2 c4
. For a photon, there is no
m
. That means
E = pc
. So, photon energy and photon momentum have relative magnitude. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: That's what I'm telling you. For a photon, it's not defined as
mv
over something. It is not defined that way because you don't even get off first base because
m
vanishes, and
v
= 0, you're in real trouble. So, you've got to realize that for a photon there's an exception of how you think about it. You don't think of it as an object of some mass that moves and has some energy and some momentum. It always moves at one speed. You might say, if it always moves at one speed, it must have only one unique momentum. That's not true either. So, they are a little tricky. For photons, you have to accept the fact that photons have energy and photons have momentum, with
E = pc
. And apart form that, there is no restriction, you can give a photon any energy you like as long as the momentum you give it is such that
E2 = c2p2
. And you cannot go to the frame in which the photon is at rest; there is no such thing, it has no rest mass. But particles with no rest mass can have energy, and can have momentum. When enough photons hit you, you can feel the force, that's called radiation pressure. So, they carry momentum, they carry energy, but the formula for momentum energy is not written in terms of mass. So, that's the second thing I've said. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: For the photon? Yes.
k0 = k1
for the photon. And if I wrote
k0
as
/c
, then it means
= kc
. That's the second statement. That's not obvious from anything I've taught you. So, that's some new stuff. Because suddenly, I've got an object with no mass and the whole derivation for momentum started with
m
times some velocity and so on, so that fails for photons. But they exist and they carry energy, they carry momentum. You should think of them as particles that obey
E2 = (cp)2 + m2c4
, with
m
= 0, so they obey
E = pc
. That's a second statement.
Third statement is, in a collision you add up all the
P
s and the
K
s for everybody on the left, and that equals the sum of all the
P
s and the
K
s on the right. And you do that so you've got to make sure you can do that part. For particles, I will tell you this particle has this rest mass, it's going at this velocity. And you should be able to build up its energy and momentum. For photons, I won't tell you this is the velocity, velocity is always
c
. For photons, I'll have to tell you this is the of the photon; this is the
k
of the photon. So, you form a little
a
vector with /
c
as the first component, and
k
as the second one. Then it's very easy. Add all the first column, second column, third column, fourth column, and those four things are separately conserved.
That's it. That's the trick to collisions, balancing energy and momentum in one mega equation, which is four-momentum before equals four-momentum after. And the beauty is any observer can look at this collision from any frame of reference; different people will disagree on what's the energy and what's the momentum of the particle. For example, in this example I gave you, I said I am at rest, and I got hit by a photon, then I'm moving. Well, that's the point of view of some observers for whom I was at rest initially. You can see the whole thing from a rocket. In that case, my initial momentum will have a spatial part because on the rocket, I'll be moving backwards. This photon will also have a new and a new
k
, which you can find from Lorentz transformation; this final object will be moving at some speed, so everything will look different. Nonetheless, the momentum and energy will balance on the two sides for you as well. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: No. You've got to be very careful about what you mean by mass. Some people think of mass as
m
divided by square root of 1 minus
v
square root. I never want to take that point of view. The only mass is the rest mass, and nobody will disagree on what the rest mass of a particle is. Do you understand that? I may think the particle is at rest, you may think it's moving, that's just fine. But if we both ask the following question, "What is its mass in a frame in which the particle is at rest?" the answer to that question is a unique answer. To find that, you go sit with the particle and you find its mass. So, the rest mass, in this case
m
and
m
′, are the same for all people. You can see the whole collision on the rocket, the
m
′ is the
m
′.
E
and
p
are transforming as Lorentz variables, but
m
is the length squared of a four-vector; therefore, it's the same for all people.
Now I want to do a second very interesting problem, which is this. The year is 1953 or '54. You are trying to build a collider in Berkeley. It's going to have a proton target. By the way, I'm going to show you one more trick that's very useful. Put
c
= 1 everywhere. You can always put
c
= 1 by choice of units. For example, if your unit of length instead of being a meter stick was 3 times 108 meters, and that was your new unit of length, let's call it a light second. For you, the velocity of light is 1 because it goes 1 light second in 1 second, the distance over time will be 1. Even if that's not your unit, I say forget about
c
, do the math without
c
; in the end you can always put back the
c
. We'll always know in the end how to put back the
c
. Maybe I have an example here. Yeah, in this problem, if I've forgotten
c
everywhere, I get an answer that looks like this:
m
′ square is
m2
+ 2
m
. I already know that if that's the mass square and that's the mass squared. Well, that's the mass, and that's an energy, so I know that should be a
c2
here. You can always fudge the
c2;
at the end of the day, there's no reason to carry it from the beginning. Just from dimensional analysis, when you're looking for energy and you see a mass, put a
c2
there. When you're looking for a mass and you see an energy and it should be a mass, divide by
c2
. So, that's what I'm going to do.
So, here is a proton at rest. Here is a proton that I've created from my Bevatron, which is going to come and smash into this. And the job of this reaction is the following: where this notation is very unfortunate [
p + p
], this is not a momentum, this stands for proton. Proton plus proton should form two protons and a new proton and anti-proton created from the vacuum. Created from nowhere. This is what happens in a collider. Particles and anti-particles are created in pairs using the incoming energy. So, it's the opposite of the atomic bomb. In an atomic bomb, mass is destroyed and energy is created. In an accelerator, energy is converted into mass. Which is why two particles can go in, and four particles, or ten, or 14,000 can come out. We want to look at the experiment where people were trying to make anti-protons. The theory says the anti-proton mass is the same as the proton mass. It's a very general symmetry of the theory. But you want to make it, and the question is, "What is the minimum energy of this incoming proton that will make this reaction possible?" And this guy starts out at rest. So, what energy or what momentum should the incoming projectile have? Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: Let's see. So, here are four protons, and in the cheapest collision what will they be doing in the end?
Student
: [inaudible]
Professor Ramamurti Shankar
: Sitting in a clump. And what will be the energy of that clump?
Student
: [inaudible]
Professor Ramamurti Shankar
: Do you agree that's 4
m
?
Student
: Yes.
Professor Ramamurti Shankar
: Okay, this guy brings energy into the collision, being the static target. So, you would conclude the energy of this should be 3
m
. By that we'll mean
mc2
divided by 1 minus
v2
over
c2
should be 3 times
mc2
. That's the energy. Because that 3
m
plus this
m
will make 4
m
. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: No. The mass of these particles is always
m
. I'm saying the energy of this guy is 3
m
. Yes? If this is 3
m
and that guys brings an
m
just by sitting there, and we need 4
m
to make four particles, and we want the cheapest deal, so nobody is doing anything. But this wrong. This is an underestimate for what you need. You need more. You've got to think about why do we need more energy than this? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: No. Let's say they don't annihilate; they form and they just--they don't annihilate that fast, so they can be produced. Anti-protons can be produced. That's not the reason why. I want you to visualize the question we're asking. Obviously, if we send a super-duper proton beam, it can knock the hell out of this proton and produce however many particles you want. We want the minimum energy, and the picture we have is what's the minimum energy of four particles? Well, it's four particles at rest. That's the one for which we computed the energy, but there's something wrong with our argument. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: Yes. Let me repeat what he said. The Law of Conservation of Momentum will not allow you to take a situation where the proton comes in with momentum. This guy is doing nothing, and you cannot have four particles at rest, because their momentum is 0. Therefore, the four guys who are produced must be drifting forward with some minimum momentum, so that that momentum equals incoming momentum. That means, you've got to pay the price to make them, you've got to pay the price to move them at a minimum momentum to balance the incoming momentum. So, that should tell you that the real energy of the incoming particle has got to be more than just whatever I said, 3
m
. So, we've got to find out the real momentum.
So, the trick is again going to be the same. So, this is the initial state, this is the final state, but this final state has got some motion. It cannot be at rest. So, what's the initial momentum? Initial momentum for this guy is some energy
E
; for this guy is some mass
m
. And the momentum of this is some number
P
. And the momentum of this guy is 0; that's the initial momentum. And that's got to be equal to the final momentum. Very good. Final momentum you can write down in detail by taking these four masses, giving them some velocities, but I'm not going to do any of that. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: This
m
, this particle has an energy
m
. It's really
mc
. Sorry, it's
E/c
,
mc
and 0. This guy has got
E/c
and some momentum
P
. I've forgotten the
c
. Remember, we agreed that we're not going to worry about
c
in this problem? So, this is just
m
. So, this is the initial momentum, that's going to be the final momentum. That also means initial momentum square is final momentum squared. If two vectors are equal, the squares are equal. Now, the final momentum squared, I say we can evaluate not in the lab frame, but in another frame called the center of mass frame. And here is a center of mass frame. Suppose you start moving to the right at some speed, what do you think will happen? Imagine in your head. You move to the right, this proton will start moving to the left
,
this proton will appear slower. Is that clear to you? Pick up your speed until they're coming in exactly opposite momenta. That's a frame of reference you can imagine. In that frame, the collision looks rather different. In that frame, this guy and this guy are approaching each other with opposite velocities, and therefore equal and opposite momenta; the total momentum is 0. In that frame, these two guys are allowed to go into four sitting ducks, because the total momentum is 0. So, that is the frame of reference called the center of mass frame in which incoming momentum adds up to 0, so the final particles are allowed to be at rest if they want to, and the minimum energy collision, they will be produced at rest, because that's the least expensive way. So, I found a frame in which this is possible. That's not the lab frame, that's the fame in which they are moving in opposite directions. But what's the total momentum in this frame? Total momentum in this frame,
P
total, is 4
m
, 0. Now, no one says the total momentum in that frame has to be the total momentum in my frame, but--sorry, say
P
final. No one says that
P
final should be my
P
final, but the square of that
P
final is the square of my
P
final because the square of any vector is the same for all observers. So, what is
P
final square? You guys should know by now. This dot product of this vector with itself is the square of this number minus 0. There is nothing here. Therefore, I argue here, that
P
initial square is equal to
P
final square. That I calculate in the center of mass frame, and I get 16
m2
. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar
: Right. Why is the square of the four-momentum the same in two frames of reference? Anybody answer that? Why is the momentum not equal, but the square is equal? Why is that? Because it's a dot product of a vector with itself, and the whole idea of defining these squares is so that they are the same for all observers. The whole idea of defining four-vectors is that when you take the length square of a four-vector defined in this crazy way, 0 component squared minus the first component squared, that's the same for all people, right? That's the beauty. That's why, if you really look at the total momentum vector in the lab frame, it looks like this. And that's got to be the final total momentum too. These numbers are not--they are both non-0. So, no one says the total momentum vector is the same. In the center of mass frame it looks like this, but the square of the vector must be the square of the vector for all people.
Now, let me finish this and maybe we'll have a discussion. So,
P
initial square is 16
m2
, so this is the top most line. Find the square of this vector, is (
E + m)2
P2
= 16
m2
. Now, so, let's see where to write this; maybe I'll write it here. That means
E2 + m2 +
2
Em - p2
= 16
m2
. But you must know that
E2 - p2
is an
m2
. I'm saying
E2 = p2 + m2
, if you banish all factors of
c2
. So, this
E2 - p2
is an
m2
; there is already an
m2
here, so I get
2m2 +
2
Em
= 16
m2
. You cancel the 2 and make it 14
m2
, and you divide by 2
m
, you find
E
= 7
m
. By the way, this is posted on the web, on the internets. So, you guys can read it whenever you like. So, don't worry about this last detail; I've given you every possible detail here. If you didn't get every factor, it doesn't matter. What I want you to understand is, I've also given you the whole argument on how you go to this frame and that frame. The point is you can answer
E
= 7
m
, now we realize it's time to put back the velocity of light, and everybody knows, even man and woman on the street, that this should be really 7
mc2
. If we carried factors of
c
throughout the calculation, it would have been very messy, but here is where
c2
would have to turn up. So, if you're looking for an energy and you get a mass, you put back the
c2
.
So, what we are told is, the incoming proton, as it moves, its energy goes from
mc2
to bigger and bigger numbers, because the denominator of 1 over
v2
over
c2
is vanishing. Wait until the energy is 7 times the rest energy, and when it's 7 times the rest energy, that's when it's ready to hit the static proton and produce proton/anti-proton pairs from nowhere. So, some of the 7
m2
is going to give a momentum to the fragment of the collision, and some is to create them. And the way we found out the minimum energy is we did energy-momentum calculation. But the minimum energy configuration is easily imagined in the center of mass frame, that's the whole point. Not in the lab frame, the center of mass frame. That's why accelerators, nowadays, are taking one particle that can move faster and faster and hitting a target they produce intersecting storage rings where the particles are going in opposite directions. And every time they meet in the racetrack, they're allowed to collide. What's the beauty of that? The beauty of that is, since they come with opposite momenta, the final fragments don't have to move at all. So, you can make more and more mass. So, don't put your energy all into one beam and a static target; put them into two oppositely moving beams. Then, all the energy is available for producing mass.
All right, so I'll stop now. I think this is a difficult chapter, so you have to go and read, and you have to talk to each other and try to do as many problems as you can.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_15_103006.mp3) |
