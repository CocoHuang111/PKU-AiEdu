- Source: https://oyc.yale.edu/physics/phys-200/lecture-10
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 10 - Rotations, Part II: Parallel Axis Theorem

### Overview

Part II of Rotations. The lecture begins with an explanation of the Parallel Axis Theorem and how it is applied in problems concerning rotation of rigid bodies. The moment of inertia of a disk is discussed as a demonstration of the theorem. Angular momentum and angular velocity are examined in a variety of problems.

### Lecture Chapters

1. Review and Derive the Parallel Axis Theorem
2. For System of Masses: Derive KEtotal = 1/2 MV2 + 1/2 ICM2
3. Derive KEtotal in Terms of Equivalent Rotation about Stationary Point
4. Effect of Rotational Kinetic Energy on Translational Motion for No Skid
5. Example Problem: Torque on a Disk
6. Advanced Example Problem: Pulley Rotating and Translating
7. Example Problem: Systems with Angular Moment Conserved
8. Application: Angular Momentum Changes for Spinning Ballerina

1. 0
2. 987
3. 1675
4. 2320
5. 2621
6. 2970
7. 3734
8. 4149

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 10 - Rotations, Part II: Parallel Axis Theorem
Chapter 1. Review and Derive the Parallel Axis Theorem [00:00:00]
Professor Ramamurti Shankar:
Let's begin Part II of Rotations. I thought I should summarize for you the main points, because you learned a whole lot of stuff, but you don't have to carry all that in your head. What I'm going to write down is the essential subject you should know. So, we were going to do rotation of rigid bodies, which are forced to lie on the
xy
plane. They have some shape. And here are the main ideas we should know. You first pick a point around which you want to rotate the body by driving a little skewer through that. That's the point of rotation. Then, here are the things we learned. First of all, the body has a mass
M
, which is a simple thing. You put it on the weighing machine, that's the mass. Then, it has a moment of inertia, which, if the body were made of a discreet set of points, would be the mass of each point,
mi
times the square of its distance from the point of rotation. For a continuous distribution of matter like this one, the sum is replaced by an integral.
For example, for a rod it was
ML2
/12 around one of the ends, around the center of mass. And for a disk, it was
MR2
/2. So, every body has a moment of inertia. Here is the important caveat, with respect to a particular point. There is nothing called "the moment of inertia," because depending on the point, these distances will vary. Okay. Then, if you want the rigid body to start doing interesting things, you wanted it to move around, it will have an angle of velocity
ω
, which is rate at--which goes round and round. It's the usual frequency times 2
π
because 2
π
radians are full circle. Then, it has an angular momentum, which is the analog of the mass, times analog of the velocity, as is universally noted by the symbol
L
. Then, if you want to change this angular momentum, it's like asking, "How do you change the ordinary momentum of a particle?" You apply a force. So, now we apply what's called a torque. And the torque is the reason the angular momentum changes. That's--The analog of force is the reason the usual momentum changes. I remind you,
P = mv
, so it is really
mdv/dt = ma
. So, you can also write analogously here,
τ = Iα
because if you take the
d/dt
of this guy, that's a constant, and
α
is a rate of change of
ω
.
The last thing I have to tell you is what is the torque of the total torque on a body. Well, if there is a force, for example, acting in that direction, let me just take one force, and it's separated by distance
r
, or vector
r
from the point of rotation. Define that angle
θ
as the angle between this point of separation distance, and separation
r
, and the applied force. Then, the torque is
F
times
r
times
sin θ
. If you took
F
to be perpendicular to this separation vector, then
sin θ
= 1. If you took
F
to be parallel to the separation vector, torque vanishes because it's no use applying a force in the line joining you to the center, because you don't produce rotations then. The
sin θ
tells you how much of the force is good at producing rotations. If you got many forces and many torques, you got to add all the torques. There's one thing to be careful about. For example, you can have a body where one force is trying to do that, and here maybe a second force acting that way, trying to do the opposite. So, we keep track of the torque by saying either it's clockwise or counter-clockwise. Each force you can tell intuitively by looking at it. This guy's making it go counter-clockwise. This is rotating clockwise. Counter-clockwise will be taken positive; clockwise will be taken negative. Similarly, angular acceleration will be positive if it's counter-clockwise, increasing. So, this is a summary of everything we did yesterday, on Monday. You guys follow that?
So, there's the analogy to
F = ma
. Everything has a rotational counterpart, but life is more difficult because in the case
of F = ma
,
m
was simply given to you. Here, the moment of inertia has to be calculated from scratch, given the mass distribution that forms the body. Similarly, you may have been simply given the forces in
F = ma
. But here, even after I give you the forces, you got to do some work, calculating the torque. But every force you got to find how far it is from the point of rotation, watch the angle between the force and the vector separating where the force is to where the rotation is taking place and calculating the
sin θ
. Okay, that's all we did. And what I did towards the end of the class was to calculate the moment of inertia for a couple of objects. I showed you for a disk, it's
MR
2/2. For a rod, I did two calculations: one was around this end, and the moment of inertia around the end was
ML2
/3, and the moment of inertia around the center was
ML2
/12.
And at the end of the lecture I said, "Notice the following fact. The moment of inertia through the end and the moment of inertia through the center of mass are related in a very simple way, which is the moment of inertia with respect to the new point, the moment of inertia with respect to the center, plus the mass of the entire rod times the square of the distance, (
L
/2)2 separating the axis going through the center of mass, and the new axis. And that's called the Parallel Axis Theorem.
Chapter 2. For System of Masses: Derive KEtotal = ½ MV2 + ½ ICM2 [00:16:27]
And I'm going to show you in general why it is true. The Parallel Axis Theorem says, "If you know the moment of inertia through the center of mass, you are done," because then the moment of inertia through any other point does not require you to go back and do the whole integral one more time. I'll tell you the answer once and for all. The answer is: take the moment of inertia at the center of mass, add to it, in general the mass of the whole body times the square of the distance between the center of mass and your new axis. For example, you want to rotate it around this point. That's the distance
d
; add that
Md2
. So, I said I don't want to just give you a result; I want to tell you where everything comes from. So, I will now prove this. So, let's start with that proof.
So, this is the proof of the Parallel Axis Theorem. Before I do the Parallel Axis Theorem, I'm going to use one result in vectors, so you might as well be reminded of that, because I use it freely, and I don't want you to get caught in that. If
A
is a vector, then the length of
A2
is found by taking
A
dot
A
.
A.A
is the length of
A
times the cosine of the angle between
A
and
A
. Well, the angle between
A
and
A
is zero, and cosine is just 1; therefore, the way to find the length of a vector is to take the dot product of the vector with itself. Another way to say this is, the dot product of
A
and
B
, you remember is
AxBx + AyBy
, so
A
with itself is
Ax2 + Ay2
which is the length squared of
A
. The result I want to use today is, if you take vector
A
and add to it vector
B
, and you want to find the length squared of
A + B
, well, you take the dot product of that with itself, and when you do the dot product you can open out the brackets as if it is an ordinary product. So, you can do this in your head, you'll get the length of
A2
from doing the
A.A
, length of
B2
from doing the
B.B
; then, you'll get an
A.B + B.A
, and these are both equal; then, you will get twice
A.B
. That's the result I want to use. So, here is the calculation.
Let's take some arbitrary object. And you want to find the center, the moment of inertia around that point. This is the center of mass. This is a part of the body that I'm calling
i
. Actually, you should integrate over it, but let's do it as a sum. Mentally, divide this body into a hundred thousand million tiny little squares, which when tiled together form this object because it's easier for me to work with a sum than with an integral. So, this fellow has some mass
mi
. It has a location, which is
r
i and I'm going to call it
ri
′, because the prime means it's the distance measured from this new axis. I'm going to reserve the symbol
ri
for the separation from the center of mass. Because the center of mass is a privileged point, all distance measured from it won't carry off prime. If you pick an arbitrary point, I want to put a′ for that one. Then,
d
is the vector that tells you how to go from your chosen axis to the center of mass.
So, what is the moment of inertia I'm trying to calculate with respect to this point? It's the sum over
i
, the mass of the little fellow here,
mi
times
ri
′ squared. But
ri
′ squared, you can see, is the length of
ri
+
d
dot, product with
ri
+
d
, using the result I established above. Okay, now, let's start opening out the brackets and look at the terms you will get. First, you'll take dot product of this guy or this guy, because
ri2
, that's going to be
miri2
, sum over
I
. I think you guys can recognize that as the moment of inertia with respect to the center of mass. That's what you would do to find the moment of inertia with respect to the center of mass. You'll take the square of that distance. So, the first time I get is just the
I
with respect to center of mass. Now, I purposely want to skip the middle term and go the last term. In the last term, there is no sum over
i
because
d
is a fixed vector, it doesn't have anything to do with the particle
i
. I get
d.d
, which is just
d2
times sum over all the masses, which is just the total mass, and that's part of the theorem because I got the two parts I like.
I
=
ICM + Md2
. The trouble is I got what I want, but I got more stuff. I got to hope that the stuff I don't want will go away. Okay, it's like putting a washing machine or something, and when you're done you find three or four parts on the ground. You don't know why they're there. In that case, there's no solution to that problem. But in this problem, there's a very nice solution. There's stuff I don't want that is going to vanish. It's going to vanish. And let's see why it vanishes.
Let's take the cross terms. The cross terms are like the 2
A.B
terms. So, here is the 2. One of the vectors
A
is the vector
d
. And it's going to be taking the dot product with
miri
summed over
i
because there's going to be a
d.ri
twice. But
d
is not dependent on the summation index. It's common to all the terms in the sum and you pull it out. Now, you can think about what this is. This is every mass multiplied by its position. So, take this guy, sum over
i
,
mir
i, divide it by the total mass, and multiply it by the total mass. But what is this? Yep, that's the center of mass, but that's a center of mass in a coordinate system with the center of mass as the origin. So, you will get zero. If I use this as the origin, take
miri
, that's the center of mass. It will have some coordinates from that origin. But these
ri
's are all measured from the center of mass itself. To compute the center of mass with the center of mass as your origin of coordinates, then it's a zero. One way to say that is if you're sitting at the center of mass, then all the masses are surrounding the center of mass in such a way that the way of some of the positions will be the center of mass, but which will be then zero, if that's your origin of coordinates. That's the reason this will vanish. This is a very useful result. The center of mass coordinates, in a coordinate system with the center of mass as the origin, will therefore be zero, and that's why this sum vanishes; then, I get the result I mentioned to you.
I
is
I
center of mass +
Md2
.
And the rod was a special case of this where I put
d = L
/2 to do that example. But it's generally true.
Okay. One place where you might find the result useful is the following. Let's think about the moment of inertia of a coin, or a disk. If I run the moment of inertia through the center, I truly have to calculate it. You divide it into concentric rings. The answer for each ring is simple, you do an integral, you get
MR2
/2. But suppose I say I want the moment of inertia through that point. Do you know what I mean? Stick the pin through that and rotate it. With some wobbly motion, it will perform with that at the center. The moment of inertia through that point, if you just went back to basics, is very hard to calculate because you can try your little trick with concentric circles, that'll be nice. That'll be nice. Then, you'll run to the edge, and after that, the circles are not really full circles. And depending on how far you go, you take different fractions of a circle, it's not easy to do that summation. Luckily, the moment of inertia was through the center, the whole object is divided into concentric rings; then, you can do the sum easily. But here is where this theorem comes into play. You don't have to do any more work through this point. It is
MR2
/2, that's the answer through the center plus
Md2
, where
d
is simply the distance from the center of mass to where you set your axis. Okay? All right, so that's one demonstration of the Parallel Axis Theorem, of the proof of the Parallel Axis Theorem.
Now I'm going to show you a similar result, because that's going to be also useful in the study of rigid bodies. It has the very same flavor, so I want to do that side-by-side. And that's the following question. Suppose you have, in two dimensions, a whole bunch of masses:
m1
with the location
r1
,
m2
with a location
r2
, and they're all moving around. You know that given all the masses that it's something, some right here, that's the center of mass,
R
. As the bodies move, this is not a fixed situation. The whole--It could be a bunch of planets traveling as seen by another galaxy. The whole Solar System is drifting. As the whole thing is drifting, the center of mass, which is the weighted average of the location, will also drift with that. Now, I want to write a formula for the kinetic energy of this complex, which is ½, sum over
i
,
mi vi2
. But now, I want to look at the velocity of this object, of every object
vi
; I want to see it as the velocity of the center of mass, plus the velocity relative to the center of mass, which I will denote maybe with the symbol
r
for relative. Do you see that? Every little speck is moving.
But let's ride in a frame moving with the center of mass. Wherever it goes, we go with that. We latch onto it. As seen by us, the body will have a velocity
vi
relative to us, but from the point of view of the ground, we should add to that velocity, the velocity of the center of mass to get the velocity with respect to the ground, or some fixed coordinate system. So let's do that same trick with the expansion, ½
m
i. Now, I think it will let me do this a little faster, because we've done the thing similar to it before. Now, I'm squaring velocities and not squaring positions. So, one term will be this capital
V
, I remind you is the velocity of the center of mass. I just don't want to show it subscript every time, but capital
V
is center of mass. So, when I squared this
vi2
, I'll get a
V2
term; then, I'll get a
vi
relative squared term. Then, I'll get a cross-term twice
V
,
vi
relative, summed over all the particles. So, let's expand the three terms. In the first term, there's a velocity of center of mass; it has nothing to do with index
I
, so you can pull it out of the sum, and what will I get? I'll add up all the masses, I'll get the total mass.
So, I'll get the result, ½
MV2
. That is the kinetic energy of the center of mass. In other words, the center of mass, if it's treated as a point containing the entire mass of the object, moving to the velocity
V
, that's the kinetic energy of the center of mass. Then, let me take this term. This is sum
mivi
relative squared. What is that? You guys should think about what does this quantity stand for? Can you tell me what it stands for? Yeah.
Student:
The kinetic energy of the objects relative to the center of mass?
Professor Ramamurti Shankar:
Yeah, by that it means, if you're really traveling with the center of mass, and you made a measurement on how fast every body's moving, this is the energy you will attribute to these particles. It's not that kinetic energy as seen by somebody on the ground who is static, but by somebody riding with the center of mass. So, this is the kinetic energy relative to center of mass. We can give it some name. It's whatever it is. But once again, the cross terms are going to vanish. That's what I want to show you. Let's look at a cross term, the 2 cancels the half; then, I get this capital
V
which can be pulled out of the summation,
mivi
relative, summed over all the particles.
mivi
relative is the momentum of particle
i
as seen by this co-moving observer who is moving with the center of mass. So, this term is really sum over
i
of the individual momenta of the particles. But if you go back to your notes, you'll find that sum of the momenta of all the particles is the momentum of the center of mass. But it is the momentum of the center of mass as measured by a person co-moving with the center of mass. So, what will that person get? They'll get zero. That's the same trick as before. For that reason this vanishes.
So, don't say to me, "How can he say the center of mass momentum is zero?" We know the center of mass is moving. But that is from the vantage of this person here. But if you go and ride with the center of mass, this is how you would compute the momentum of the center of mass, by looking at the momenta of the fragments as seen by you; they better add up to zero. What it means is, if there're two masses moving at different velocities, there're only two of them. If you go to the center of mass, and ride with the center of mass, whatever momentum one guy has, the other will have the opposite momentum. So, the momentum of a system will appear to be zero as seen by the center of mass.
Okay, therefore, here is the result. The kinetic energy of a collection of masses is the kinetic energy that you can associate with the center of mass motion, less kinetic energy relative to center of mass. Let's just call it
K
relative, but it's understood as relative to center of mass. This result is true no matter what I'm talking about. Collection of loosely moving, loosely connected particles. But now, apply it to the case where these particles form a rigid body. Think about it now. It's not a swarm of bees, they're all connected by rigid rods, so they form a rigid complex. In that case, what motion is allowed, if you ride with the center of mass? Think about it. What motion can you have? Yes?
Student:
Rotational.
Professor Ramamurti Shankar:
It's rotational, but you can be more specific. Rotation about which point?
Student:
[inaudible]
Professor Ramamurti Shankar:
And was that a good guess, or was there a reason for that?
Student:
[inaudible]
Professor Ramamurti Shankar:
Yeah, let me repeat what he said. If you are riding with the rigid body and you are sitting wherever the center of mass is sitting, then the only motion allowed for you is the rotation around the center of mass. Because if it is not around the center of mass, then the center of mass will be moving relative to the axis of rotation. But that's not allowed, because according to you the center of mass is not moving; therefore, any rotation that takes place must be around an axis passing through the center of mass. In that case, we know what the kinetic energy is. It's ½
MV2 +
½
ICM2
or whatever the angular velocity is at that moment. So, this is the statement that the kinetic energy is the sum of two terms, the translational part, and the rotational part, provided you separate it as the kinetic energy of translation of the center of mass, and rotation relative to center of mass.
It's a very useful result, because so far what we did is in the early part of the course, we took bodies which just translate. They are point particles; they have a mass; they have a velocity. We got used to ½
MV2
as the answer. Last lecture, we took a rigid body which has a size and a shape, we nailed one part of it so it couldn't move, so all it could do was rotate around a point, and we learned that energy of rotation written somewhere there is ½
Iω2
. But in reality, a body can translate and rotate. Throw anything you want in the air, it will spin or move and also rotate. Then the kinetic energy of that complicated motion remarkably is the sum of two terms. One, you ignore all the wobbling. Just zero in on the center of mass. Treat it like a point, and associate an energy with its motion. Then, think of the rotation around the center of mass, which is all that is allowed to that [co-moving] observer, and add that energy. Maybe for the more mathematically-minded people, what is interesting is if you take
A + B
whole squared, there's an
A2
term, and a
B2
term, and they told you, long back, not to forget the 2
AB
term, the cross term. The fact is, the cross term always vanishes both in that derivation and in this derivation. It has to do with the fact that the point that I'm talking about is not any old point, but the center of mass. So long ago, when you learned about the center of mass, you say, "Why did people think of this notion?" You can see repeatedly, it's a very powerful notion. But if you want to study a rigid body, if you want to pick any one point that you want to focus on, it's got to be center of mass. Yes?
Student:
[inaudible] is ignoring the effects of gravity of a body [inaudible]
Professor Ramamurti Shankar:
No. This is kinematical statement. That doesn't require that the particles are not subject to gravitational force. They can be subject to any force, external forces, internal forces, whatever you like. All I've done is at a given instant, take a snapshot, take the kinetic energy, and write it in a different way. Take the kinetic energy as seen by a static observer, and rewrite it as seen by an observer moving with the center of mass. So, I'm going to apply this to a simple problem so you can get a feeling for this. The simple problem is going to be a disk. You can think of the problem as either a disk or as a cylinder. A cylinder is just a disk with a certain thickness. So, a disk is like a coin. The cylinder is a stack of coins. But the moment of inertia for a disk or a cylinder is the same. Do you guys understand that? If I took one coin, it has got
MR2
/2. Then, we put a second coin on top of it and rotate them through the same axis, then it's
MR2
/2 for this guy plus
MR2
/2 for that guy. It then is equal to the total
MR2
. For a cylinder or a disk, the moment of inertia is just
MR2
/2 through the center of mass. Okay, just remember that.
Chapter 3. Derive KEtotal in Terms of Equivalent Rotation about Stationary Point [00:27:55]
Now, let's take this disk, which is sitting now and give it some energy of motion. Think of it as a tire in a car, one of the four tires. They're spinning. So, there are different things you could imagine. Lift the car off the ground in a service station, and you let the tires spin; that is rotational energy. For that, the answer is ½
Iω2
. That's what we've been doing all of last time. But let's do something else. Let the tire hit the ground. And the car is going at say 50-miles-an-hour; then you slam the brakes, so you prevent the tire from turning. If you prevent the tire from turning, you lock the brakes, the tire can still move with a certain velocity
v
, which is just the translational motion of the center of mass. So, this is a car which is skidding, this is a tire which is either spinning or its wheels are lifted off the ground. They are the two simple kinds of motion you can imagine. One is simple translation, there's no rotation to worry about. The energy's ½
mv2
. Other than simple rotation, which we learned, no translation, the kinetic energy of all the little guys are moving in the tangential direction is ½
Iω2
.
All right, in a real car both things are happening. In the real car, the tire is rolling along the ground and also rotating around the center and also translating. It's got both motions. Now, the two motions, namely the linear velocity of the center and the angular velocity around the center in general don't have to be connected in any way. Suppose you start your car on a slippery road. The tire's spinning, the car's not moving. So, that's
ω
equal to not zero, but
v
= 0. Or when the car is moving along and you slam the brake, then you kill the
ω
but not the
v
. I'm just trying to tell you, in general, there are two velocities. The linear motion of the center and the angular motion around the center are independent. But one is a skidding car, and one is a car that's spinning its wheels. But I want to talk about the car the way we like it. In a car that's moving the way we like it, there's a correlation between the angular velocity and the linear velocity. And that is called "rolling without slipping." That's the term people use. And when it's rolling without slipping, I think you have an intuitive feeling. If this car is to roll without slipping on the ground, can you see that by the time it finishes one full revolution, when it's come over here, the center will have moved the distance equal to circumstance of that tire. So, every part of the tire touches the ground; then, that comes down and that comes down, and when it goes all the way to this end, it has also finished one full revolution.
For example, if every part of that circle was colored with some chalk, then when it finished the full revolution, every part of the circle would have touched the road and made an impression. And the length of that thing should be the circumference of the circle. That's when it rolls without slipping. So, what does it mean to roll without slipping? What's the velocity? But let's calculate the velocity when you roll without slipping. When you roll without slipping, the velocity of the center of mass, which is always denoted by
V
, is equal to
2πR
divided by the time to make one full revolution. But what is 2
π/T
? Well, let me write it another way. It is 2
π
times the frequency of revolution, because 1/
T
is the frequency. And 2
πf
is the angular frequency and radiance per second. So, here is the connection between linear velocity and angular velocity, if you're rolling without slipping.
V = ωR
. All right? So, in general,
V
and
ω
are independent, but rolling without slipping refers to a particular situation.
Now, in that case, let's find the kinetic energy of an automobile tire that's rolling without slipping. So, what do I want to get? The kinetic energy is ½
MV2
+ ½
Iω2
; that's always true.
I
is always
I
relative to the center of mass. But now I'm going to use the fact that it is ½
MV2 +
(1/2) (
MR2/
2
)ω2
. Not done anything different. But now, we must remember that
ωR
is the velocity of the car. So, if I do that, I find going back to this car right here,
K
= ½
MV2
+ ¼
MV2
. So, you can write it as ½ times 3
M
/2
V2
. So, the kinetic energy of a rotating tire is not just ½
MV2
. If it's rolling without slipping, it's incumbent on the tire to have some rotational energy that's correlated with its translational energy. So, the total energy will be this. But I'm going to write this in a different way. Let's replace
V
by
ωR
, so I can write it as ½ times (
M
+
M
/2) times
R2ω2
. And that means it's equal to ½
MR2
+ ½
MR2ω2
. This is a lot of re-writing, so if you don't follow all the details now, you can go back and check the intermediate steps. But what do you notice about this formula? I want you to think about what the formula suggests to you. Suggest anything? The stuff in the brackets? Yes? Yeah? What do you see in the brackets?
Student:
½
MR2 = I
.
Professor Ramamurti Shankar:
That is
I
. You can be more specific than just saying
I
.
Student:
I
= center of mass.
Professor Ramamurti Shankar:
That's correct. So, this term is a moment of inertia with respect to the center of mass. And this looks like--what now? Yes, somebody in the last row. Yes?
Student:
Moment of inertia [inaudible]
Professor Ramamurti Shankar:
A hollow ring, but I'm having something else in mind. Yes?
Student:
The moment of inertia [inaudible]
Professor Ramamurti Shankar:
Right. Let me repeat what he said. If you will ask me, "What's the moment of inertia of the tire with respect to this point?" What will you do? You'll do the Parallel Axis Theorem; it will give you
MR2
/2 for the moment of inertia through the center, and an extra
Md2
which now becomes
MR2
. So, this is really ½ I-- what shall we call it? Road or something. It's up to you. You can call it whatever you like. There's a moment of inertia with respect to this point of contact on the road.
Now, you have to think about this result. It's a very interesting result. It is telling you the entire energy of this tire is as though it is rotating around this point with angular velocity
ω
. Forget translation, it's a just a pure rotation around this point. Now, when it's rotating around the point, it means that point cannot be moving. And I will now convince you that that is actually true. If you look at your car tire, how fast are the different parts of the tire moving? The car as a whole is moving at a speed
V
. On top of this, the tire is spinning, so if you take a point here to that
V
, you got to add an extra tangential velocity, which is
V + ωR
. That just happens to be 2
V
. If you come to the bottom part of it, as seen by the car, it's moving backwards at this velocity minus
V
. Add to that the speed of the car, you get 0.
In other words, the top of the tire is moving along with the car, with the same velocity as the center. The bottom of the tire is moving opposite to the car with the same velocity as the center, so its real velocity is seen by the ground as zero. So, this is a very surprising result. A car going past you at 200 mph. There is a part of the car that has zero velocity relative to the ground. It's not obvious that a zooming car has one part of it that's not moving at all. It's not the same part, otherwise the car is really not moving. But at every instant, the part of the tire that touches the ground has zero velocity. I hope you understand why it's a cancellation of the central motion, of the overall motion with the rotational motion. You can see the rotational motion on the top adds to the speed of the car. Rotational motion on the bottom subtracts from the speed of the car. And if you write
V = ωR
, the two precisely cancel here and double there. So, if the bottom point is at rest, then the only thing the car can do is to rotate around that point. And that's the reason why the energy comes out to be purely rotational energy around the center. So, this is a simple problem that illustrates all the things you have learned today: how to use the Parallel Axis Theorem, how to do the energy calculation, how to interpret the energy calculation.
Chapter 4. Effect of Rotational Kinetic Energy on Translational Motion for No Skid [00:38:40]
but now, this is useful for the following example. Suppose I have a little slope. I release an object from the top. And I ask you, "How fast is it moving when it comes here?" If it's a point mass and the height is
h
, we know from very elementary ideas, if it's a point mass, so don't quote me on this--If it's a point mass, I'll say
mgh
has become ½
mv2
. Kinetic potential has become kinetic. But if it is a cylinder rolling without slipping, and it comes here, the center of mass cannot move at this speed because it's got to be a lower speed, so that the rotational energy plus translation energy will add up to
mgh
. So, this must be equal to the total kinetic energy, and I've solved it for you guys. You remember that. You have to write 3/2
mV2
. This will go back to whatever was done here. Here. So, you can see that if you cancel the mass, you're going to get
V2 ≠ 2gh
, as you normally would. You're going to get
V2
= 4/3
gh
. So, it'll be moving somewhat slower than a point particle. See, if it rolls without slipping, then you will be traveling slower at the foot of the ramp.
So, what did I do? I used the Law of Conservation of Energy. That's all I did. But in finding the kinetic energy at the bottom, I was careful to not just take ½
MV2
. This is the energy of a point particle, but take the kinetic, the energy of translation and rotation, which I've done for you here. That's the kinetic energy. The translation, that's the kinetic energy of rotation. By the way, don't make the mistake of thinking it is 3/4
V2
for everything. It is 3/4
V2
for a cylinder. If it's a sphere or something, you got to add a different thing. But every time you will have to find a moment of inertia, you do rotation and add to the energy of the rotation, the energy of translation. You follow that? For each body, you'll have a different moment of inertia. So, you've got to use, in the place of ½
mV2
, let me just tell you for a sphere. If this was a sphere, not a disk, they all look the same, but if it's a sphere, this ½
mV2
, I think it's 2/5
MR2
. It's a different number. But then, it's all
MR2
times some number, so you can take the
R2
out of this and turn it into
V2
. So, you will find instead of just the mass, you'll get some multiple of the mass entering here in the kinetic energy. And to the extent that's bigger than the mass, the velocity will be that much slower.
So, there're all kinds of variants you can have. Here's the variation of this theme. You remember that when you want to do the loop-d-loop, if you release a block from here at the top, I've shown you many times, the velocity squared has to be bigger than or equal to
Rg
. That's to make sure that it doesn't just fall down to the track. That's the critical time at which the track is exerting zero force. If you went faster than that, it'll push you down and everything will be fine. If you go slower than that, you will fall down. Okay.
But now, suppose it's not a point mass, but an object like a coin or a disk rolling without slipping. It is still true
V2
at least has to be equal to
Rg
, but to find the
V2
here, you will use the Law of Conservation of Energy. That's all just fine. The potential energy here will be
mg
times 2
R
, the potential energy here is
mg
times
R
[correction: should have written
h
not
R
]. Just don't make the mistake of saying the kinetic energy is ½
mv2
and put
V2 = Rg
. That would be wrong. This
m
here may become 3/4 or 9/7 or whatever it is for that body. So, it's the same idea, but you can add more and more ideas and put them together and make a more interesting problem. But if I were to summarize in one sentence what I have told you all of this time is that, when rigid bodies move, they have a translational and rotational energy. In general, they're independent numbers, but when you have rolling without slipping, the angular velocity and the linear velocity are connected in this fashion. So, it's not surprising that the total energy has got a contribution from both, which you can write either in terms of the angular velocity or the linear velocity. In other words, if I know how fast the wheel is spinning, I can tell you how fast the car is moving. If I tell you how fast the car is moving, I know the rate at which the wheels are spinning, provided it's not skidding. If it's skidding, these bets are off.
Chapter 5. Example Problem: Torque on a Disk [00:43:41]
All right, so now we continue with this saga of rotations. And let me remind you where we stand. When I did
F = ma
after telling you a little bit about how mass is measured, and everybody knew how acceleration is measured, what did we do? We first took a bunch of problems where some forces are acting on a body. Maybe something's pulling, something's pushing, then we learned how to find the acceleration. Then, I took other cases where there are many bodies exerting a mutual force on each other. Then, if there are no external forces, we saw the total momentum of the system is concerned. We're going to do analogous things with our newfound equation of
τ = Iα
. You want to get used to this more. That's all I'm going to do from now on. I already told you the beginning, the new thing you learned was
τ = Iα
, and we're going to use it.
So, let's take various situations where we can do this. Let me take a simple example. You can make up your own problem, doesn't matter, but get practice. One possibility is: here is a disk like a merry-go-round. It's sitting still. It's got a mass, it's got a radius, and I want to apply a torque. So, one way to apply the torque is the way kids do. You know, you grab this end and you run with it on the side; as you run with it, it picks up speed, but what you're trying to do is apply a tangential force as long as you can. And the force times the distance will turn into a torque. And that'll produce angular acceleration. Another way to do that if you're really high-tech is to buy yourself a rocket; it's got some flames coming here. Then, if you just put one rocket, the danger--What do you think the danger is, if you just put one of these rockets? You know what the problem may be? It'll certainly exert a torque. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
Yeah, because, look, there will be translational motion left to itself, because that is the force. And
F = ma
has not gone away just because we're in chapter 11; that's still true. So, what'll happen is, this pivot point is trying to hold the merry-go-round in place. They're putting a lot of force on it, because it'll try to move. It has to counter the force at every instant. As long as the merry-go-round doesn't fly off, what'll happen is, that the rocket's emitting gas this way, and applying a force that way, the pivot will apply an opposite force. And as the rocket goes there, it'll apply an opposite force in the other direction. But to spare this pivot this unwanted agony, what you do is you get a second rocket, similar thrust, put it diametrically opposite, and have its flames going out like this. So, when you buy a rocket, they will tell you, "This rocket has a thrust of so many Newtons." That's the force it will exert by emitting the gas. So, if it got a certain thrust,
F
here. You got another rocket the same thrust,
F
here. The radius is
r
, the torque you're applying is an
F
times
r
times sine of 90, which is 1. And another
F
times
r
from the other guy, and the two torques are added. That'll be the torque. Then, the rest is very easy. What's the angular acceleration of this guy? It is 2
Fr
divided by the moment of inertia, which in this case is
MR2
/2, if it's a disk. What if I put some passengers on this? Suppose I put one lone passenger here on some mass; let me call it little
m
. Then what happens? Would you like to guess? Yep.
Student:
Yeah, if you add the moment of inertia at a distant point [inaudible]
Professor Ramamurti Shankar:
Right, so what you'll add to the denominator?
Student:
Would that be
mR2
?
Professor Ramamurti Shankar:
Yes.
Student:
It's not something that I [inaudible]
Professor Ramamurti Shankar:
That's also correct. So, my picture is wrong. So, my picture is wrong. Sorry for this one. This
r
should be capital
R
. And let's use for this mass here, small
r
; then, there's small r2. Capital
R
is the symbol I want to use for--oh, my God! This is a nightmare! I have to change it in so many places. I guess once I started down this road, I have to do that. Okay, so look, it's very natural that big
R
is the disk radius, and small
r
is some point inside. But I was not planning to put this guy in the platform, so I just used a random symbol. Does everybody understand now? For the moment of computation, it's the radius of the disk. For the moment of inertia of the little person we put on this little
r2
.
Okay, so that's the simplest example of using
τ = Iα
. Once the rockets start burning, you got this
α
. I can ask you things like, "How many degrees has it rotated after 19 seconds?" And you should know what to do.
θ = θ0 + ω0t
+ ½
αt2
.
θ0
you can choose to be zero. Initial angular velocity was zero. Just ½
αt2
. But
α
is this. You put the number of seconds they gave you, that'll tell you how many degrees it has rotated. By that time you can say, "How many revolutions has it made? Then, what will you do?" Yes? Any idea? Yep?
Student:
Divide [inaudible] by 2
π
.
Professor Ramamurti Shankar:
Divide by 2
π
because 2
π
is one full revolution. These are things you must know. Okay, then, if I say, what's the angle of velocity after 36 seconds? Well, there's
α
times 36. These are simple problems.
Chapter 6. Advanced Example Problem: Pulley Rotating and Translating [00:49:30]
So now, I'm going to do a slightly more complicated problems. Here is the first complication you can have. There is a pulley, and there is a mass. I better get everything right here. This is--Let's call it little
m
, let's call the radius
R
, and mass big
M
. And I just let go of the mass. And the question is, "What's the acceleration of this mass?" So, there's a combination of rotational problems and translation. So, there's a combination of rotational problems and translation. The mass is translating, the pulley is rotating. And the point is, what's the acceleration of this mass? So, we know from the old days that if you want to find what's happening with the mass, you should draw free-body diagram with a downward force
mg
, and some tension
T
on the rope. Then, you must also draw a free-body diagram for the pulley. When you look at the free-body diagram for the pulley, our tension
T
, is acting down here. Have I drawn all the forces on this? Yep?
Student:
[inaudible] pulley in place?
Professor Ramamurti Shankar:
Right. So, this pivot point is going to apply some force. Basically, what it has to do is to overcome the weight of this mass, and overcome this tension
T
. But I'm not going to bother to write that. I'll tell you why. So, this is an incomplete picture. There is something else here but I won't pay any attention to it because I'm going to use
τ = Iα
, and I'm going to take the torque through the center. And this is something that'll come over and over again. If you take a torque through a certain point, the forces acting through that point, they don't get to contribute because in the formula for torque,
Fr sin θ
,
r
vanishes, and the forces don't do anything. That's why I don't pay any attention to what the pivot is doing. This
T
is trying to rotate it this way, and I know that
T
times
R
is the torque, and that's going to be
MR2
/2 times
α
. But
α
is the angular acceleration of this guy. For the mass, it is
mg - T = ma
. So, let's go and cancel one power of
R
here. But we seem to have two unknowns in this problem: the tension
T
-- sorry, three unknowns -- the acceleration
a
, and the tangential angular acceleration
α
, of the pulley.
But here is where you do the trick you did even with the two masses. They're not independent accelerations, because if this point has an angular acceleration
α
, you can see that point has a tangential acceleration of
R
times
α
. That has to be the acceleration of this mass also, because the rope is being given out at a certain rate and that's the same. So, the mass can go one inch only if the pulley turns by a corresponding amount to release one more inch. So, the tangential velocity of the point here is the velocity of the mass. The acceleration of that contact point is the acceleration of this. Therefore, you have to use the fact that
a = Rα
;
a
is really what I called
a
-tangential in the first lecture. So, if you do that, you can see that this
R
times
α
is just
a
. This combination becomes
a
. Now, I'm ready to add these two equations,
-T
and
+T
cancel, giving me
mg = a
times (
m + M
/2). So, we can get the acceleration. So, the acceleration is
gm
divided by
m + M
/2. So, does it make sense?
When you get a calculation like this, you can test it in many ways. First, if the pulley is massless, capital
M
vanishes; forget it downstairs. Cancel little
m
with little
m
and you get
a = g
; that's the correct answer. It's just falling down freely. Now, I'm going to subject it to another stringent test. Suppose I ask you--Suppose it's got a distance
h
through which it can fall. How fast is the block moving when it hits the ground? Just before it hits the ground, what's the velocity? So, you have to think about what ideas you'd invoke to do that. Is the acceleration constant, first of all? Yes? Gentleman in the back said "yes."
Anybody know if it's constant or variable? How many people think it's constant? Okay. See, I don't know what you guys are thinking. So, I'm always worried whether your silence means that you have no idea what I'm saying, or it's so obvious you don't want to tell me. Now, that's going to happen in a class with 100 people. It's very unfortunate, it'd be a lot nicer if I had 10 people and I can stop and ask each one of you. But I ask you, if you don't follow something, you got to tell me, because otherwise I just don't know. So, if
a
is constant, and a lot of you seem to agree
a
is constant, then you go back to lecture number 0. What did we find?
v2
is
v02
, which is 0, plus 2
a
times the distance traveled, which in our case would be
h
. So, let's put that in. 2
a
is this number here.
m + M
/2 times
h
. So, I'm going to write it in a very suggestive language as
[
2/
(m +M
/2
)]
times
mgh
. Anyway, that's the square of the velocity when the block hits the ground. So, what do you think I'm trying to test now? What's my goal? Any idea where I'm going with this? Yeah?
Student:
Because it's moving slower when it hits the ground, and it has less kinetic energy, that means that energy is stored in rotational kinetic energy.
Professor Ramamurti Shankar:
That is correct. But if I wanted to test this, if I wanted to subject this answer to a test, what test do you think I can apply here? This has to meet a certain requirement. Yep?
Student:
You want to show that energy is conserved.
Professor Ramamurti Shankar:
I want to show that the energy is conserved. There is no friction; nothing in this problem. So, if you wanted to say energy is conserved, we know what we want. We want
mgh
has to be the kinetic energy of all these objects. Right? So, I go to my answer; here is
mgh
. Let's send all the other stuff to the left-hand side. If I do that, I get
(m/
2
)v2 + ½ (M/
2
) v2 = mgh
. All I've done guys is to transfer this fellow to the other side. Well,
mgh
is wonderful! That's my initial potential energy; there is no kinetic energy; nobody was moving. This is clearly the kinetic energy of the mass. And the last thing is, this is the kinetic energy of the pulley. I think by now you recognize this is the kinetic energy of the pulley. If you're not convinced, I can replace this
v
by
ωR
, and bring the
R2
in here, and write this last term as ½ [1/4]
MR2ω2
, which is the kinetic energy of the pulley.
So, you got to understand the linear velocity of the mass and the angular velocity of the pulley are connected. And the connection factor's always
R
.
R
is the number that connects linear to angular quantities. So indeed, this answer satisfies the Law of Conservation of Energy. That's a very good test.
Now, you can have variations of this problem. I don't want to do too many variations. In fact, I'm just going to draw it in the corner of the board, and I don't feel like pursuing it, because there is a limit to how many things can be done in the class. So, here is a pulley, and here is a mass. And you guys can work out the accelerations of the mass down here. It's the same story that I did here, okay? You got to draw the free-body diagram of the mass; you're going to draw the free-body diagram of the pulley, and you're going to say, "The net force on this is bringing it down. The net torque on this is turning it." And you'll realize that the
a
of this and the
α
of this are not independent, but that the
a
of the block is related to the
α
of the pulley by this factor; then, you'll be home. Things will just work out. And it will of course depend on this angle
θ
. Suppose you did the calculation, and you wanted to subject that to a test. What can you do? Yeah?
Student:
Well, you can still raise the [inaudible]
Professor Ramamurti Shankar:
There is no friction, so what he's saying is you can use the Law of Conservation of Energy. For example, if there's dropped a certain height
h
, from that height to the ground, your answer should satisfy the condition that
mgh
was equal to the kinetic energy of the mass and the pulley at the end of the day, and your answer will satisfy it. Another thing you can do is if this angle
θ
goes to 90 degrees, look what happens. If
θ
goes to 90, forget about the block, it is just falling freely, and that's the previous problem. You can check if the answer you get agrees with the previous problem. So, I'm just teaching you that it's good to have constant checks on the problem. One way to check the calculation is to go back and do it again. Most of the time, if you screw it up the first time, you'll probably screw up the second time because one of the basic rules of nature is that if you repeat a certain experiment under the same conditions, you'll get the same answer. That's why when I proofread anything, I write, I don't find any mistakes. But my readers are gleefully pointing out this and that typo, because we cannot detect those errors. That's true even for a scientific calculation. Because for some reason you forgot something the first time, you'll keep making the same mistake. That is known in the business as "chasing after
π
." In all the calculations we do, we look at the right answer, and we look at our answer, and we take the ratio it's always 3.14; so, we know somewhere we lost the
π
. It's called "chasing after
π
," and "chasing after factors of 2," is roughly how I spend 80 percent of my time when I'm debugging something. So, how do you beat those things is by all these extreme limits.
That's another thing I want to tell you with this. All of us are partial to working these things with symbols and not with numbers. I think it's a big issue in Introductory Physics. There's a resistance to working with symbols. People want to know what's the mass
M
. What's the number
R
? Let me put that in. If you put numbers in too early, you cannot test your answer for anything. In the end you just got a number. You cannot take the limit of one particular number. But if you got a function that depends on all the parameters, you can vary them and in some extreme limit, you would know what the answer is. That's why you should be ready, even in the exam; that's not a secret. I will tell you right now, most of the problems I give, you will work with symbols. Now, I don't know why it's harder working with symbols. For me, it's just the opposite. Once I put numbers in, I don't know what the number stands for. What is it? But if I call it
M
, if I call it
R
, if I call it
G
, I know what it stands for. So, you guys have to get used to, even in a homework problem where numbers were given to you. A block of mass 46 kg, collides with some elephant. First, call them all 1, 2, 3. Give them masses, solve the equation, then put the numbers in. That's what I would recommend. Anyway, I think you can see here the advantage of working with symbols.
Chapter 7. Example Problem: Systems with Angular Moment Conserved [01:02:14]
Okay, so what I have done now, I took examples of
τ = Iα
. In all the problems I did, something had a torque and it was spinning. The torque either came from the rockets, or it came from the pull of this mass, or from the pull of this mass. Now, I'm going to take a subset of problems, in nature, where the torque, the total torque on a collection of bodies is zero. So, I'm going to take a system. There are many torques, but the external torque, due to forces outside the things forming the system is zero; then, you remember when the external forces vanished, then the momentum of the system was the same.
P1 + P2 = P1
′,
+ P2
′. So, here you will find
L1 + L2
, or
L3
, any number of them will be conserved. In other words, in the absence of external torques, the angular momentum of the system is conserved. That means it has the same value. Angular momentum is conserved if
τ
-external is zero. That's like saying linear momentum is conserved if the external force is zero.
So, let's take some examples of this. Here's one example. There is a disk on a spindle that's spinning around. The disk has some moment of inertia
I1
, spinning at some angle of velocity
ω1
. On top of this is a second disk, just one millimeter away, and it's at rest. And it's got some moment of inertia
I2
, but it's got the same center as this guy. And then, this one falls on that one, and the question is what happens? So, I think we all know what happens. We all know the two will now stick together and rotate as a single unit with a common angular velocity. So, the Law of Conservation of Angular Momentum will say,
I1ω1
for the first guy plus 0 for the second guy is now =
I1 + I2
times my final
ω
. So, it's a trivial thing to solve for
ω
.
This should remind you of the following problem in translational motion. There is a body sitting at rest,
m1
, or
m2
. There's a body
m1
coming at a speed
v1
. They stick together and travel as a unit. What happens? Then, we say the initial momentum is the momentum of
m1 + m2
, traveling at some final speed. It's identical to that with the usual dictionary for translating quantities here.
Okay. Now, let's take a slightly more interesting problem. The merry-go-round is spinning. I'm seeing it from the top. It's got some angle of velocity
I1
. I mean, angle of momentum,
I1ω1
, because of moment of inertia and angular velocity. This is the top view, and I dropped a piece of chewing gum on it. What happened? It's very simple. The chewing gum and the thing will start rotating together. The new moment of inertia you should use here, would be just
MR2
. I think people seem to know that if you stick a point of mass on a disk, the extra contribution
MR2
, it'll slow down. Remember, these are problems in which there are no external torques. One disk, this disk is speeding up that disk, slowing--I'm sorry, this is speeding that up, and that is slowing this, but together they cannot change the total; that's the whole point. What if this putty, or chewing gum, was not just dropped, but shot from the site like this, with some speed
v0
? It's got some mass
m
. This guy is radius
R
, big
M
. Now what happens? This is something that may not be obvious to you. A putty that's traveling and then comes and lands and sticks to it. What's the difference now? Yep?
Student:
The distance and [inaudible] apply a force to stop the motion of a body. So, that's the torque.
Professor Ramamurti Shankar:
Very good. Excellent. So, let me repeat what he said. This moving chewing gum has to be brought to rest [in the frame of the disk]. It'll be brought to rest by the disk that'll push it backwards, and the chewing gum will push it forward, so it'll apply a torque. That means it'll change the angular momentum. But instead of going through that route of finding the torque, if I only knew the angle of momentum of this putty, then that will add it to the angle of momentum of the disk. Then, I say, that's the total angular momentum that should not change. So, the question is, "What's the angular momentum of a mass that's not really moving in a circle, but that's moving in a straight line?" And the answer is: pretend that it's part of a circle right there, moving at this velocity. What will be its angular momentum? In other words, if you are the moving putty, and you look to your left, the disk is spinning, and you are going at a certain speed, at that instant you are not distinguishable from another body that's actually orbiting the center. But what will be the relation of your velocity to your angular velocity? Where your tangential velocity is
v0
, your angular velocity will be
v0
divided by
R
. At that instant, that'll be your angular velocity because somebody will be looking at you, you'll be there now, you'll be there later. Your
θ
will change. And the angular velocity will be
v0/R
. Your angular momentum will be
mR2
times
ω
, which you can write as
mR2
times
v0/R
, which becomes
mv0R
, which I would like to write as
p
times
R
, where p is the usual momentum.
So, when a body comes with a tangential momentum
p
, and it plants itself on the disk, it actually is an angular momentum
p
times
R
. This is not very surprising. Just like
R
times
F
gives the force,
R
times
p
gives the angular momentum. So, the surprising thing for you guys is, things don't have to be going around in a circle to have an angular momentum. They can be going in a straight line, but at every instant, I can find the angular momentum by asking, "What's the moment of inertia, namely
MR2
, and what's the angular velocity?" The angular velocity is easiest to find when this guy is right next to the disk. You know from what we did earlier, angular velocity is linear velocity divided by
R
.
Chapter 8. Application: Angular Momentum Changes for Spinning Ballerina [01:09:08]
Okay, the last problem that I want to do, which I'm not going to do quantitatively, but qualitatively is a very, very interesting problem. Go to a single particle in translational motion, whose momentum is
mv
. And we know if there are no forces, the momentum cannot change. So,
mv
is a constant. Now, that translates into
v
is a constant. Because
m
is a constant, there's nothing you can do. Now come the interesting possibilities that are available to you when you do rotations. That's the famous Icecapade example, okay? So, let me do the Icecapade thing. So, here is ice, here is some dancer. All right. This person is spinning around with some velocity
ω
with her hands out. To emphasize the whole thing, let's imagine this ice dancer has no mass, except for the two dumbbells on the two hands or the two masses, okay? And the person is rotating with some angular velocity
ω
. That means the angular momentum is
I
times
ω
. And that cannot change.
But then, suppose the ice dancer decides to do the following, which is to drop the arms right to the side so that for all purposes the mass is at the center now. You really reduce the moment of inertia. So, what'll happen? So, I will signify that angular velocity; she got her hair is kind of standing out. It's a rapidly spinning ballerina, and that's because what is changing is
I
. If bodies could change their mass, it'll be very interesting. If a body can reduce its mass in half, it can double the velocity. But bodies have no way of getting rid of their mass. If bodies can change their moment of inertia just by redistributing the mass. And that's why all these ice dancers, you know, they spin around, then they bring their hands together. Then, they speed up and slow down, and they speed up, then they slow down. What is interesting is the following. If you go back and find the kinetic energy, you'll find the kinetic energy's not the same because kinetic energy is ½
Iω2
to begin with. It is ½
I1,ω12
. At the end of the day, it's ½
I2
,
ω22
, but
ω2
can be written as
I1
/
I2ω12
. And you can easily compare the two numbers in the geometry I've given you to show the final kinetic energy's actually higher. When you start spinning faster, in fact, the bigger the kinetic energy. Because if your
ω
doubles because your moment of inertia went down by a factor of half, that keeps
Iω
constant. But you're supposed to square the
ω
, so in the product
Iω2
, when you reduce one by half and double the other, you gain a factor of 2. So, take the simple case where
I2
is half of
I1
and you will see it. Okay, so you can ask, "Where does that energy come from? How does this ice skater pick up speed, pick up angular momentum or kinetic energy?" The angular momentum doesn't change, but the rotational energy changes. Yep?
Student:
I got like sort of potential angular energy. Is that sort of [inaudible]
Professor Ramamurti Shankar:
You can do this without invoking any new concepts, using this old concept. You just go back and say, "Look, I know only one rule in this game." If the energy went up, then what? Yes.
Student:
The system itself is performing work on different elements of the system. So that work is increasing but [inaudible]
Professor Ramamurti Shankar:
But who is doing work?
Student:
The skater is doing work by bringing together the dumbbell she's carrying.
Professor Ramamurti Shankar:
Yeah, and why does that take any work? Because if gravity is pulling you down, you're moving perpendicular to gravity, so why are you--you got an answer in the last row? Yes?
Student:
Doing work against gravity.
Professor Ramamurti Shankar:
No, but see, you're not doing work against gravity, because you're not changing the height of those barbells. You're just pulling it in. Yes?
Student:
When you pull, you have a difference in potential energy. You have less potential energy when you're holding it up.
Professor Ramamurti Shankar:
No, no, but oh. Oh, I see. I am sorry. I know why you guys are giving those answers. It's not your fault. Take the case where you don't change the height of the dumbbells; go from there to here. Not changing the height. So, the
mgh
is not the answer. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
Yes.
Student:
Energy comes from the muscles.
Professor Ramamurti Shankar:
It comes from the muscles, but the question is why do you have to do any work? And I think since I'm running out of time, I will repeat that answer, which I believe is close enough to what I was looking for. When the dumbbells are spinning, they're going in a circle. And we know that they have an acceleration
v2/R
, and we know somebody's got to provide
mv2/R
, and the person is providing that force. But as long as she's providing the force, but not moving, you can move tangentially. But the force and velocity are perpendicular, so you're not doing any work. But the minute you pull in, you're applying a force and a displacement which are both parallel. Then
F
times
d
is no longer 0, you will find that these things are going to fly off, as he said, and you're trying to not only hold on to them, but trying to bring them in. During that time, it'll be just like lifting weights. If you want to lift weights, and you go to a planet where there is no gravity, tell somebody to spin you, then when you pull the stuff in, it'll be like lifting weights, okay? That's what the person's doing, and that's where the energy's coming from.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_10_101106.mp3) |
