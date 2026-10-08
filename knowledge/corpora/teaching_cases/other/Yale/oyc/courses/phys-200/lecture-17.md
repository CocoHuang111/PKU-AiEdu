> 检索摘要：Open Yale Courses「PHYS 200 Simple Harmonic Motion」。主要内容：以简谐运动为重点，Shankar用质量块连弹簧等物理系统说明受扰动后的行为，定义振幅、频率和周期，并解多题展示不同振动情形。页内标题：Lecture 17 - Simple Harmonic Motion；Overview；Lecture Chapters。分隔线后是英文原文，未翻译、未改写。

- Source: https://oyc.yale.edu/physics/phys-200/lecture-17
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 17 - Simple Harmonic Motion

### Overview

The focus of the lecture is simple harmonic motion. Professor Shankar gives several examples of physical systems, such as a mass M attached to a spring, and explains what happens when such systems are disturbed. Amplitude, frequency and period of simple harmonic motion are also defined in the course of the lecture. Several problems are solved in order to demonstrate various cases of oscillation.

### Lecture Chapters

1. Example Equations of Oscillating Objects
2. Superposition of Solutions to Linear (Harmonic) Equations
3. Conditions for Solutions to Harmonic Equations
4. Exponential Functions as Generic Solutions
5. Undamped, Under-damped and Over-damped Oscillations
6. Driving Harmonic Force on Oscillator

1. 0
2. 649
3. 1816
4. 2337
5. 3048
6. 3628

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 17 - Simple Harmonic Motion
Chapter 1. Example Equations of Oscillating Objects [00:00:00]
Professor Ramamurti Shankar:
Stable equilibrium, and if you disturb them, they rock back and forth and there are two simple examples. The standard textbook example is this mass on spring. This spring has a certain natural length, which I'm showing you here. It likes to sit there. But if you pull it so the mass comes here, you move it from
x
= 0 to a new location
x
; then, there is a restoring force
F
, which is -
kx
, and that force will be equal to mass times acceleration by Newton's law, and so you're trying to solve the equation
d2x/dt2 = -k/m
times
x
, and we use the symbol,
ω2 = k/m
, or
ω
square root of
k
/
m
. And what's the solution to this equation? I think we did a lot of talking and said look, we are looking for a function which, when differentiated twice, looks like the same function up to some constants, and we know they are trigonometry functions. Then, we finally found the answer. The most general answer looks like
A cos ωt - φ
. A is the amplitude,
φ
is called the phase. That tells you what your clock is doing when
x
is a maximum, and we can always choose
φ
to be 0. That means when the time is 0,
x
will have the biggest value
A
.
This is an example of simple harmonic motion. But it is a very generic situation, so I'll give you a second example. Now, we don't have a mass but we have a bar, let's say, suspended by a cable, hanging from the ceiling, and it's happy the way it is. But if you come and twist it by angle
θ
, give it a little twist, then it will try to untwist itself. So, now we don't have a restoring force but we have a restoring torque. What can be the expression for the restoring torque? When you don't do anything, it doesn't do anything, so it's a function of
θ
that vanishes when
θ
is 0. If
θ
is not 0, it'll begin as some function of
θ
, but the leading term would be just
θ
. But now, you can put a constant here. It'll still be proportional to
θ
, and you put a minus sign for the same reason you put a minus sign here to tell you it's a restoring torque. That means if you make
θ
positive, the torque will try to twist you the other way. If you make
θ
negative it'll try to bring you back. So, you have to find this
κ
. If you find this
κ
then you can say
-κ
times
θ
is
I
times
d2θ
over
dt2
. Mathematically, that equation's identical to that, and
θ
then will look like some constant. You can call it A
cos (ωt- φ
, and
ω
[squared] now will be the ratio of this
κ
at the moment of inertia, because mathematically that's the role played by
κ
and
I
. They are like
k
and
m
.
Now, if someone tells you this is
κ
, then you are done. You just stick it in and mindlessly calculate all the formulas. You can find
θ
, you can derivatives and so on. Sometimes, they may not tell you what
κ
is. In the case of a spring, they would have to give you
k
or they may tell you indirectly if I pull this spring by 9 inches, I exert a certain force, they're giving you
F
and they're giving you
x
and you can find
k
. But in rotation problems, the typical situation is the following.
Let us take the easiest problem of a pendulum. The pendulum is hanging, say a massless rod, with some mass
m
at the bottom. So, it's very happy to stay this way. If you leave it like this, it would stay this way forever. No torque, no motion. Now, you come along and you disturb that by turning it by an angle
θ
. If you do, then the force is like this, the separation vector
r
from the pivot point is this, and
r
cross
F
will be non-zero because the angle between them is not 0, and you remember that torque is equal to
rF sin θ
, and I told you for small angles, this can be
rF θ
, and
r
happens to be, in this problem, the length of the pendulum, so it's really -
mgl θ
.
So, you have to do some work to find
θ
[correction: should have said
κ
]. It wasn't just given to you on a plate. You did this piece of thinking, and namely, you disturbed the system from equilibrium and found the restoring torque. Then, you stared at the formula and say hey, this guy must be the
κ
I'm looking for because that number times
θ
is the restoring torque. Then the
ω
here will be--this
κ
is a generic
κ
that goes into whatever it is for that problem. For our problem,
κ
happens to be
mgl
. That's something you should understand. It's not a universal number that's known to everybody like the spring constant of anything. In the case of mass and this pendulum, it depends on how long the pendulum is, how big the mass is, but you can work it out and extract
κ
. Downstairs, you need the momentum of inertia for a point mass
m
at a distance
l
from the point of rotation, which is
ml2
. So, you can cancel the
l
, you can cancel the
m
, and you get
ω
is root of
g
over
l
. Let me remind you guys that
ω
is connected to what you and I would call the frequency by this 2
π
, or what you and I would call the time period by 2
π
over
T
.
Okay, so this is the situation. Let me give one other example. This is a homework problem, but I want to give you a hint on how to do this. Don't take a pendulum with all the mass concentrated there. Take some irregularly shaped object, a flat planar object. You drive a nail through it there, hang it on the wall. It'll come to rest in a certain configuration and you should think about where will the center of mass be if I hang it like this on the wall? Center of mass is somewhere in the body here. So, I want you to think about it. I'll tell you in a second. The center of mass, they claim, will lie somewhere on this vertical line going through that point. I know that by default because if the center of mass is here, for example, we know all the force of gravity can be imagined to be acting here [pointing to drawing]. Then if you do that separation and do the torque, then you will find this is able to exert a torque on this point, but that cannot be in equilibrium. So, center of mass will align itself. The body would swing a little bit and settle down; the center of mass somewhere there.
If you now disturb the body, I don't want to draw another picture, but I'll probably fail. This is the rotated body, off from its ideal position, then there will be a torque. What will the torque be? It'll be the same thing minus
mgl sin θ
, which I'm going to replace by
θ
.
l
is now the distance between the pivot point and the center of mass. That's your torque. So, you can read the
κ
. In fact, it's just like the pendulum. In other words, as far as the torque is concerned, it's as if all the mass were sitting here. The difference will be in a moment of inertia. Moment of inertia of this is not
ml2
, so don't make the mistake. All the mass is not sitting here. All the mass is sitting all over the place. So, you should know that if you want the moment of inertia, it is
I
with respect to center of mass plus this
ml2
. That's the old parallel axis theorem. So, take that moment of inertia and put that into this formula here; take this
κ
and put it there, you'll get some frequency. That's the frequency with which it will oscillate. So, every problem that you will ever get will look like one of these two. Either there is something moving linearly with a coordinate that you can call
x
, or it's rotating or twisting by an angle you can call
θ
. And if you want to find out the frequency of vibration, you have to disturb it from equilibrium, either by pulling the mass or by twisting the cable or displacing this pendulum from its ideal position here, then finding the restoring torque. Yep?
Student:
What can we say [inaudible] its restoring torque in the twisting example? How do we describe that?
Professor Ramamurti Shankar:
That's a very good point. His question is, if I gave you a cable and I twist the cable by some angle, how are we going to calculate restoring torque? Here is the good news. This problem is so hard we'll give it to you. In other words, there is, of course, an underlying answer. Given a cable, made of some material and its torsional properties, how much of a torque you'll get if you twist it by some amount, but it's not something you can calculate from first principle, so they'll simply have to give it to you, okay, in such problems. The only time you'll have to find the torque on your own is in a problem like this where I believe you know enough to figure out the torque.
Okay, what you will find is, if you leave it alone, it'll go to a position where there is no torque. If you move it off the position, there will be a torque, and the torque will always be proportional to the angle by which you've displaced it. You read off the proportionality constant and that's your
κ
. You should look at the forces too. It is pretty interesting. This body, when it is hanging in its rest position, has two forces on it. The nail, which is pushing up and the weight of the body which is pushing down, and they cancel each other. The nail will keep it from falling. The nail will not keep it from swinging, because the force of the nail acting as it does at the pivot point is unable to exert a torque, whereas the minute you rotate the body,
mg
is able to exert a torque. That's why if you twist it, it'll start rattling back and forth.
Chapter 2. Superposition of Solutions to Linear (Harmonic) Equations [00:10:49]
Alright. So, what I'm going to do now is to go over more complicated oscillations using some of the techniques we learned last time. So, here is the mega formula. I'm going to give it to you guys. You're allowed to tattoo it on your face. You can carry it with you. I will allow you to bring it but you cannot forget this formula. I think you know the formula I'm driving at. Ready?
e
to the
ix
, or
θ
, I don't care. Let me call it
θ
here, is
cos θ + I sin θ
. That's a great formula from Euler. From this formula, if you take the complex conjugate of both sides, that means change every
i
to minus
i
, you will get
e
to the minus
iθ
is
cos θ - i sin θ
. That also you should know. If you got this in your head--By the way, this is something you're not going to derive on the spot. It takes a lot of work. If you tell me what are the few things you really have to cram, that you don't want to carry in your head, well, this is one of them. Okay, this is a formula worth memorizing, unlike formula No. 92 of your text. It's not worth memorizing. This is worth memorizing. Once you got this, you should realize that in any expression involving complex numbers, you can get another equation where every
i
is changed to minus
i
. That'll give you this one. That's called complex conjugation. I generally said, if you have a complex number
z
,
z
star is equal to
x
iy
, if
z
is equal to
x
plus
Iy
. So, in our simple example, this fellow here is
z
. This is the
x
and this is the
y
.
Now, you should be able to invert this formula. To invert the formula, you add the 2 and divide by 2. Then, you will find
cos θ
is
eiθ
+
e-iθ
over 2. If you subtract and divide by 2
i
, you will find
sin θ
is
eiθ
eiθ
over 2
i
. In other words, my claim is that this funny exponential, sum of exponential, is the family of cosine. It'll do everything your cosine will do. It'll oscillate, sine squared plus cosine squared would be 1, it'll obey all trigonometric identities, like sine 2
θ
is 2
sin θ cos
θ
, everything comes out of this expression.
So, you should know, here is the main point you should learn. We don't need trigonometric functions anymore. Once you got the exponential function, provided you let the exponent be complex or imaginary you don't need trigonometric functions. This is one example of grand unification. People always say Maxwell unified this, and Einstein tried to unify this. Unification means things that you thought were unrelated are, in fact, related, and there are different manifestations of the same thing. When we first discovered trigonometric functions, we were drawing right-angle triangles and opposite side and adjacent side. Then, we discovered the exponential function which, by the way, was computed by bankers who were trying to calculate compound interest every second. The fact that those functions are related is a marvelous result, but it happens only if you got complex numbers. So, this is another thing you should know.
Okay, now, armed with this we are ready to do anything we want. Let me just tell you that every complex number
z
can be written as its absolute value times some phase. In other words, if my complex number
z
is here, it is
x
+
iy
; that's one way to write it. You can also write it as its absolute value. It'll be
e
to the
iφ
φr
,
re
to the
iφ
.
r
is the radial length which also happens to be the length of the complex number. That's called the polar form of the complex number.
x + iy
is the Cartesian form of the complex number. I may have called them
r
and
θ
,
r
and
φ
. I just don't remember. I'm going to use these symbols back and forth because people do use both the symbols, which is why I'm sometimes calling this angle as
θ
and sometimes this angle as
φ
, but the basic idea is the same. This entity here can do it either in this form or in this form. This is something you should know. If you don't know, or you don't understand, you should stop and ask. Everything is built on this.
So, what I'm going to do now is to go back to this rather simple equation,
d2x/dt2 = -ω2x
. By the way, today I'm going to call this
ω
as
ω0
. It's the same guy. I'm going to call it
ω0
because we will find as the hour progresses, there are going to be many
ω
s in the game. Two more
ω
s are going to come in. So, we've got to be able to tell them apart. As long as there's only one
ω
in town, you just call it
ω
. If there are many, you call this
ω0
to mean it's the frequency of vibration of the system left to its own design, and you pull it and let it go. What's the frequency? An angular frequency, that's what we call
ω0
.
Now, how did we solve this equation? The way I tried to solve it for you is to say, turn it into a word problem. I'm looking for a function,
x(t)
with a property that two derivatives of the function look like the function, and we rake our brains [inaudible] and we remembered, hey, sines and cosines are the property. One derivative is no good. Turn sign into cosine. Two derivatives bring back the function you started with, which is why the answer could be sines or cosines. But now I'm going to solve with a different way. My thinking is going to be: I know a function that repeats itself, even when it differentiated once. Namely, the function has a property; its first derivative looks like the function itself. It's obvious that his 90-second derivative will also look like the function because taking the derivative leaves the function alone, except for pulling out some numbers. So, why not say, "I want an answer that looks like this:
x
equals some
A
to the
αt
." That certainly has a property that if you take two derivatives it's going to look like
e
to the
αt
on the left-hand side, and
e
to the
αt
on the right-hand side, and then you can cancel them and you've got yourself a solution. Do you guys remember why I didn't follow this solution for the oscillator? Why was it rejected? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: Ah. That's a very good point. So, maybe I will take
e
to the minus
αt
. How about that? Will that give me a second derivative which is negative? You didn't fall for that, right? Because the first time you'll get
-α
but second time you'll get +
α2
. That's correct. So, this function is no good. Also, it doesn't look like what I want. Even without doing much mathematical physics, I know if you pull this spring it's going to go back and forth, whereas these functions are exponentially growing; they're exponentially falling, they just don't do the trick. But now, we'll find that if you're willing to work with complex exponentials, this will do the job.
So, we're just going to take this guess and put it in the equation and see if I can get an answer that works, okay? This is called an
ansatz
.
Ansatz
are something we use all the time. It's a German word. I'm not sure exactly what it means, but we all use it to mean a tentative guess. That's what it is. If you're lucky, it'll work. If you're not lucky, that's fine. You move on and try another solution. So, we're going to say, "Can a solution of this form be found, with
A
and
α
completely free?" Maybe the equation will tell me what
A
and
α
should be. So, let's take it, put it here. By the way, I'm going to write this equation in a form that's a little easier.
x
double dot is minus
ω02x
but each dot is a derivative. It's just more compact that way rather than to write all of this stuff.
So, let's take that guess and put it here and see what we get. I get, when I take two derivatives, you can say, "Do I want
e
to the
αt
or
e
to the -
αt
," you'll find it doesn't matter so I'm going to take
e
to the
αt
and put it in. Now, the beauty of the
x
function now is to take one derivative,
x
dot. I hope everybody knows the
x
dot of this is,
A
[
α
]
e
to the
αt
, and
x
double dot is another
α
.
Aα2e
to the
αt
. That's the beauty of the exponential. The act of differentiation is trivial. You just multiply it by the exponent,
α
. See, this being the result of taking two derivatives, let me write it here now. What do I get? So, I'm going to go to
x
double dot equal to minus
ω0
squared
x
. Into that, I'm going to put in the guess,
x
equals
Ae
to the
αt
, and what do I find?
In fact, let me write the equation in a nicer way:
x
double dot plus
ω0
squared
x
has to vanish. I just brought everything to one side. Now, put
eαt
,
A
to the
αt
as your guess, then you find that
α2
,
Aeαt
, plus
ω0
squared
Aeαt
has to be 0. So, we know what to do. Let's group a few terms. So, this means I get
A
times
α2
+ 1,
eαt
has to vanish. If you can make that happen, you got a solution because you've satisfied the equation. No one's going to say, well, you got it by guesswork. Well, it turns out solving differential equation is only guesswork. There's no other way to solve the equation other than to make a guess, stick it in, fiddle with the parameters, see if it will work. So, we're not done yet because we want this to vanish. How many ways are there to kill this answer? You can say maybe
A
is 0.
A
is 0; you've got what you call a trivial solution. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: Ah, yes. Thank you. Yep. Thank you very much. So, this one is α2 + ω02. Does everybody follow that? Yes, from here to here it's very clear what to do. So, we cannot kill
A
. Yep?
Student:
[inaudible]
Professor Ramamurti Shankar:
Yeah, yeah, yeah. I'm trying to rule out certain options I don't like. The option I don't like to get this to be 0 is to say that is 0. That's not happening.
eαt
is not going to vanish. Maybe it'll vanish for some negative infinity time, but I want this to be true at all times. The equation has to be obeyed at all times, so this guy certainly is not zero at all times, so the only way to fix that is to have
α2 + ω02
= 0. That's the only solution, which is not a trivial solution. Well, that's a simple equation, right? It's a quadratic equation that means α2 = ω02, or
α
is plus or minus
iω0
. So, when we were young and we didn't know about complex numbers, we would come to this stage and we would quit and say, "Look, exponentials won't work, but now we are not afraid of complex exponentials, so we embrace the solution." So now, I've got two solutions.
By the way, what's the value of
A
? Think about this. If this condition is satisfied, you realize
A
can be whatever you like.
A
is completely arbitrary. So, what this equation has told me is the following. Yes, there are solutions of this form. For
A
you can pick any number you like, in fact, real or complex, it doesn't matter. The equation is satisfied. But your
α
is not an arbitrary number. It can be only one of two numbers:
+iω0
or
-iω0
. So, we've got a problem now that I look at one answer, I got two. So, I will write them both. So, let's say that the solution
x1
of
t
, which is some number
A
,
e
to the
iω0t
, then I got another solution
x2
of
t
, which is equal to any other number
B
,
e
to the -
iω0t
. Now, I think you guys can see in your head that if you take this and you put it in the equation, it works, and if you take this and put it in the equation, that also works. Because when you take two derivatives,
iω
whole square would be minus
ω
square, minus
iω0
whole square would also be minus
ω
not square, so both would work.
Now, we have to ask, "How do I decide between that solution and that solution?" It turns out that we don't have to pick. We can pick both, and I'll tell you what I mean by "we can pick both." Now, this is a very, very important property for all of you who are going into economics or engineering or chemistry. This or other disciplines, which are mathematical, the property I'm going to mention of this equation is very important, so please pay attention.
This is called a linear equation. A linear equation will obey a certain property called superposition. I'll have to tell you what it is. If I give you differential equation, you know, 96 derivative of
x
, plus 52 times the 37 derivative of
x
, blah blah blah adds up to 0; what makes it a linear equation is that throughout the equation, either you find the function
x
or its derivatives, but never the squares of cubes at higher powers of
x
or the derivatives. Okay? The function appears to first power, not to second power. For example, if this were the equation you were trying to solve, that is not a linear equation. That's called a non-linear equation. If you have a linear equation, there's a very, very profound consequence and I'm going to tell you what it is, and that lies at the heart of so many things we do.
So, let me write down two solutions. One of them will be
x1
double dot
+ ω0 2x1
= 0. Second one obeys
x2
double dot
+ ω02x2
= 0. Don't even have to look at these two solutions. Take a general problem where you have a linear equation that are two solutions. Add the two equations. On the left-hand side, I get a second derivative of
x1
plus a second derivative of
x2
, and remember that is, in fact, the second derivative. Now, I go back to the old notation of
x1 + x2
. This has to do with the fact the derivative of a sum is the sum of the derivatives, and the sum of the derivative is the derivative of the sum. Yep?
Student:
So, because you have these two linear solutions, does that mean you can generate an infinite number of [inaudible]
Professor Ramamurti Shankar
: Yes. I'm coming to that in a minute. I'm first doing a more modest goal of showing that their sum is also a solution. In the second term, I get
ω0
squared times
x1 + x2
= 0. You stare at this equation. Look, this plus this implies what I've written down simply by adding. But say in words what you found out. What you found out, is that if
x1
satisfies the equation,
x2
satisfies the equation
x1 + x2
, let's call it
x
plus, is
x1
+
x2
also satisfies the equation, and the proof is right in front of you. And the key was the derivative of a sum is the sum of the derivatives. Now, I'm going to generalize it more and say, suppose I multiplied all of the first equation by
A
, and all of the second equation by
B
. Well, that's certainly still true, right? You take something equal to 0, multiply both sides by A, it's still going to be 0. Now, imagine adding this to this [adding the two equations together]. Add this to this, and what do you get? You will find
d2/dt2
of
Ax1
+
Bx2
+
ω02
,
Ax
1 +
Bx2
is 0.
So, here is the punch line. If you give me two solutions to this equation, I can manufacture another one by taking the first one times any number I like, plus the second one times any other number I like. So, the story is a lot more complicated than it looked. It looked like there are two solutions; actually, there's infinite number of solutions because you can pick
A
and
B
any way you like. So, linear equations typically have infinite number of solutions and you build them up by taking a few building blocks. They're like unit vectors
I
and
J
. You can take any multiple of this unit, vector any multiple of that unit vector, and this combination will also solve the equation.
Just so you don't think this is going to happen all the time, let me remind you. You don't have to write this down but you guys follow what I'm saying. Suppose this quantity here was not
x1
but the square of
x1
and here. Okay. You don't have to write this because this is not a linear equation. We're not interested in this. But notice this is non-linear, and you guys should be able to pick it up. It's non-linear because I've got the square of the unknown. Now, can you see if I add these two equations, forget
A
and
B
, let them both be 1. I get
x1
squared plus
x2
squared, but that does not equal to
x1
+
x2
, the whole thing square. So, even though the second derivative of the sum is the sum of the second derivative, the sum of the squares is not the square of the sum. So, for a non-linear equation you cannot add solutions, but for linear equations you can combine solutions with arbitrary coefficients. That's the lesson you have learned today.
Chapter 3. Conditions for Solutions to Harmonic Equations [00:30:16]
So, harmonic oscillating equation is a linear equation, so feel free to combine them and get the following solution: x(t) is equal to Aeiω0 , plus B e-iω0t. A and B are whatever you like, but
ω0
is the original root of
k/m
. But if I gave you this solution, will you be happy to take it as a solution for the mass spring system, and if not, what is it you don't like? Yes? Anybody have a view? I mean, would you take that as a good solution? Yes?
Student:
Wouldn't you need to figure out how to choose the right
A
and
B
?
Professor Ramamurti Shankar:
In order to achieve what?
Student:
Because your system starts at some amplitude [inaudible]
Professor Ramamurti Shankar:
Well, he's raising a point. Let me repeat his point.
A
and
B
in general--they are arbitrary. For this mass and this spring you can pick any
A
and
B
you like. But on a given day, when you pull it by 9 centimeters and release it, the answer has to be chosen so that our
t
= 0,
x
becomes 9, and the velocity, let's say, was 0 when you released it, so when you take the derivative of this, the velocity should vanish at
t
= 0. Or maybe it will have some other velocity. But you can fit initial coordinate, initial velocity, the two numbers, by picking these two numbers. You understand that. But that's not enough. I've got another problem. Yes?
Student:
It has imaginary numbers in it?
Professor Ramamurti Shankar:
Yes. That should bother you. The answer is manifestly not real, okay, and we know
x
is the real function. That is not a mathematical requirement of the equation, but a physical requirement that when you pull a mass by 9 centimeters and you release it, it's going to oscillate with some real
x
and not a complex
x
, so you've got to fix that. So, to say that
x
is real really means the following. You remember that in a complex--world of complex numbers, a complex number
x + iy
has a complex conjugate
x - iy
and the property of real numbers, is that when you take the complex conjugate, nothing happens because
i
goes to minus
i
. If the number was purely real, it satisfies the condition
z
=
z
star. So, real numbers are their own complex conjugates. In general, a complex number is not its own conjugate, but if you wanted me to draw you a picture, that's where the
z
is, and that's where the
z
star is, but fellows on the
x
axis have the properties,
z
is the same as
z
star.
z
star is a reflection of the
x
axis of
z
, and therefore, if the number is real, it's its own reflection.
So, I'm going to demand that this solution, in addition to satisfying the basic equation, also is real. To do that, I'm going to find the complex conjugate. It's denoted by the
x
star of
t
. I want to conjugate everything in sight. The complex conjugate of
A
I'm going to call
A
star. Complex conjugate of eiωt is e-iω0t. Why? Because the
i
goes to minus
i
,
ω0
and
t
are real numbers. Nothing happens to them. And
B
becomes
B
star and this becomes
e
to the plus
iω0t
. And I demand that these two fellows are equal. If they are both equal, then I take this exponential and demand that those be the same. That means I demand that
A
be the same as
B
star, because if
A
is the same as
B
star, this will go into this, and then I will demand that
B
is the same as
A
star. If these conditions are satisfied,
x
star will become
x
.
So, the trick is to take the function, take its complex conjugate, equate it to itself, and look at the consequence. Now, I want to tell you that if
A = B
star, then you don't have to worry about this as an extra condition, because I'm your complex conjugate, you are my complex conjugate, but the way it works is if you took
A
and changed every
i
to minus
i
, right, or if you took
B
, whatever its complex form was, change
i
to minus
i
you get
A
. But if you do it one more time, you come back to where you are. In other words, for any complex number, if you star it and you star it one more time, you come back to where you are. Therefore, if
A = B
star, take the complex conjugate of the left-hand side, you'll find
A
star is equal to
B
star star which is
B
. So, you don't need these two conditions. You do need
A
=
B
star.
Okay, so you have to put that extra condition now. So, in the real world, for people who want a real answer, you want to write it as
Aeiω0t
+
A
star
e-iωt
. In other words,
B
is not an independent number.
B
has to be the complex conjugate of
A
. Then, all of you can see at a glance that this is now real, because whatever this animal is, this is the complex conjugate of that, which got all the
i
s turned into minus
i
. When you add them, all the
i
s will cancel; answer will be real. But
A
is not necessarily real. The complex number
A
, which is some complex number, has a length and it can have a phase, because every complex number can be written in this form. So, if you remember that, then you find x looks like absolute value of A
eiω0t
p+
φ
plus absolute value of A
e-iωt
+
φ
. Well, maybe that's too fast for you, so let me repeat what I did. In the place of
A
, write the absolute value times
eiφ
.
eiφ
will combine it
eiωt
and form this exponential. Second term will be just a conjugate of the whole thing. You don't even have to think. Now, what is this function I have? I want you to think about it. Do you recognize this creature here as something familiar? Yes? Do you have any idea? Yeah? Yep?
Student:
[inaudible]
Professor Ramamurti Shankar:
Without the
A
.
Student:
[inaudible]
Professor Ramamurti Shankar:
You remember this great identity. Where is it? Here? This one. eiθ +
e-iθ
is 2 times
cos θ
. So, this becomes 2 times absolute value of
A cos ωt + φ
, and if you want you can call 2
A
as another number
C cos ω0t + φ
.
Student:
[inaudible]
Professor Ramamurti Shankar
: Oh, but for any complex number. You can pull certainly this number out of both. You pull it out and you got
e
to the
i
something plus either the minus
i
something--
Student:
[inaudible]
Professor Ramamurti Shankar:
So, this is a long and difficult way to get back to the old answer. You got this by filling it out and guessing and arguing physically. But I want to show you that with an exponential function, you would have come to this answer anyway. So, your point of view is, you know, we don't need this. We've got enough problems in life; we're doing well with cosines, thank you. Why do you bring this exponential on us? Well, now I'm going to give you a problem where you cannot talk your way out of this by just turning it into a word problem. The word problem I meant, we asked a word question, find me a function where the second derivative looks like itself, and you can either start at exponentials and differentiate twice, or sines and cosines. So, you don't need exponentials.
Chapter 4. Exponential Functions as Generic Solutions [00:38:57]
But look at the following problem. This is a problem of a mass
m
, force constant
k
, moving on a surface with friction. The minute you got friction, you have an extra force. So you find
m
,
x
double dot equal to minus
kx
, which would be all the force due to the spring. Friction also exerts a force which has got some coefficient
b
, but it's multiplied by the velocity. We know that if you're moving to the right, the force of the left you are moving to the left the force is to the right, frictional force is velocity dependent. So, the equation you want to solve, when you've got friction, is really
mx
double dot plus
bx
dot plus
kx
equal to 0. I'm going to divide everything by
m
. Take the
m
, put it here, and put it here. Then, I'm going to rewrite for us the equation we want to solve with friction.
x
double dot, plus
γx
dot, plus
ω0
squared
x
= 0, where
γ
is just b over
x
. So, this is the equation you want to solve.
Can you solve this by your usual word problem? It's going to be difficult, because you want a function which, when I take two derivatives, it looks like the function plus some amount of its own derivative. If you take
cos ωt
, it won't do it. If you take
sin ωt
, it won't do it.
So, we can still solve it because even this equation, you solve by the same mindless approach, which is to say, let
x
look like
A
,
Ae
to the
αt
, and it'll work. Let's see how it'll work. It has to work. You can see why because when I take two derivatives of
x
, I'll get
α2
. Let me pull the
A
out of everything plus
αγ
plus
ω02
,
e
to the
αt
= 0.
So, what we learn is yes, there are solutions of this form to this equation. Once again,
A
can be whatever number you like, because if
A
vanishes you've killed the whole solution.
e
to the
αt
is not going to vanish at every instant in time, so the only way is for this to vanish. That means
α
that you put into this guess is not any old number, but the solution to this quadratic equation,
α2 + αγ + ω02
= 0. So, we want
α2 + αγ
not square is
ω02
= 0. So,
α
must be the root of this equation, and we all know a quadratic equation will have two roots, and we will get two solutions, and we can add them with any coefficient we like. That'll also be a solution.
So, let me write it down. So, in other words, I'm going to explicitly solve this quadratic equation. So, go back to the old days and remember that the solution of that equation will be
α
=
-γ
, plus or minus square root of
γ2
- 4
ω0
square over 2. I would like to rewrite this as minus
γ
over 2, plus or minus square root of
γ
over 2 square, minus
ω0
square. And let's call the two roots, one with a plus sign and one with a minus sign, as
α
plus and minus. This is a shorthand for this whole combination.
You understand that if I give you the mass and the spring constant, and I give you the coefficient of friction, the number
b
,
α
plus and
α
minus are uniquely known, so you'll get two precise numbers coming out of this whole game, and your answer then to this problem will be
x
of
t
is any number
A
times
e
to the minus
α
plus
t
with any number
B
times
e
to the minus
α
minus
t
, where
α
plus or minus are these two numbers. I want you to notice both numbers are falling exponentials. Very important, because now I'm talking about a mass where I pull the spring, there's a lot of friction, and I let it go, I don't want an exponentially growing answer. That makes no sense. The
x
should eventually vanish and that will, in fact, happen.
Let's make sure you understand that. Look at these two roots. Minus
γ
over 2, plus and minus, well, that is this solution minus
γ
over 2 square, minus
ω0
square. I'm going to assume in this calculation that
γ
over 2 is bigger than
ω0
. Let's do that first. Then, you can see that that's a negative number, that's a negative number, the whole thing is negative, so
α
minus is definitely, let me see how I wrote it. Oh, I'm sorry, I made a mistake here. I think these are called just plus and minus
α
,
α
has two roots and I have to write them as they are. Okay. I'm sorry. So please remove this, I put unwanted sign there. Because they are the two answers for
α
. So, I put
e
to the
α
plus
t
. So again, I should change my answer here. I'm really sorry about this one. Now, I'm going to write it below so you have a second chance. So, here is what it looks like.
Ae
to the minus
γ
over 2, plus square root of
γ
over 2 square, minus
ω0
square
t
, plus
Be
to the minus
γ
over 2 minus
γ
over 2 square minus
ω0
square
t
.
Student:
You forgot the minus.
Professor Ramamurti Shankar:
Pardon me?
Student
: You forgot the minus in.
Professor Ramamurti Shankar:
I think I did mean this. Or did I get it wrong? These are the two values of
α
. So, they both have the first number to be minus
γ
over 2, and the square root comes for the plus sign for one of them and minus sign for the other one. I probably have
A
and
B
mixed up. Let me check that. No, I think even that's okay. Yes? I'm willing to be corrected if I got
A
and
B
mixed up. I know these are correct. I want to make sure this is what I call
B
.
B
has a coefficient
α
minus, which would be this one.
Student:
[inaudible]
Professor Ramamurti Shankar:
Oh, yes. Yes. So, what should I do, call this
A
? Call this
B
? How is that now? Let's see if that works out. This should be
Be
to the
α
minus
t
.
B
over the minus
γ
over 2 minus that. Yes.
Student:
[inaudible]
Professor Ramamurti Shankar:
Pardon me?
Student:
[inaudible]
Professor Ramamurti Shankar:
Okay. The point of writing it this way is to show you that both these powers, this is clearly a positive number so it's
e
to the minus a negative number. I just want to show you that this object--that's all I wanted to emphasize. Inside the square brackets is also positive. Okay, this is
γ
over 2. You can see this is a number smaller than
γ
over 2 square. So, if you take the square root of that number, it'll be smaller than
γ
over 2, so this cannot overturn the sign of this. It'll still be a positive over all signs to be negative; so, if you draw the picture here, it's a sum of two exponentials, it'll just die down after a while.
And how do I find
A
and
B
? To find
A
and
B
, what I have to do is to take extra data, one of them may be initial position,
x
of 0 is given to me. If
x
of 0 is given to me as some number, I take the solution, I put
t
= 0 and have it match this. If I put
t
= 0, well all this exponential will vanish and I just get
A + B
, because
e
to the 0 is 1. So, I already have one condition on
A
and
B
. Their sum must be the initial position. How about their initial velocity? Go back to this
x
and take
dx/dt
. What do you get?
dx/dt
is
α
plus
A
,
e
to the
α
plus
t
, plus
α
minus
B
,
e
to the
α
minus
t
. The derivative of my answer is this. Evaluate it at
t
= 0. At
t
= 0, you put
t
= 0 here, you find
x
dot of 0, equal to
α
plus
A
, plus
α
minus
B
. So, here are the two equations you need to find
A
and
B
. Solve these two simultaneous equations. In other words, I will tell you the initial position and I will tell you the initial velocity. You will take then this number, known, and that number known. This is a linear simultaneous equation for
A
and
B
. You will fiddle around and solve for
A
. Yes?
Student:
Are
A
and
B
still complex numbers?
Professor Ramamurti Shankar:
Ah. Now, we have to ask the following question. In this problem, if everything is real--See previously, what happened is when I took the complex conjugate of this function, the conjugate turned into the other function, and the conjugate of that function turned back into this one. That's why
A
and
B
were related, by complex conjugation. Here, if I take the complex conjugate of
x
,
e
to the
α
plus
t
, if it's real, it remains itself. So,
A
just goes into
A
star,
B
goes into
B
star, and you want the answer to be unchanged. That requires
A
equal to
A
star and
B
equal to
B
star. Thanks for pointing out that here. We do want
A
equal to
A
star and
B
equal to
B
star. So, what I'm telling you is go take the solution, conjugate it and equate it to itself, and remember that now this exponential remains real to begin with so it doesn't go into anything. It remains itself, and I compare this exponential before and after its coefficient that went from
A
to
A
star, they have to be equal so
A
is
A
star and
B
is
B
star. Yes?
Student:
[inaudible]
Chapter 5. Undamped, Under-damped and Over-damped Oscillations [00:50:48]
Professor Ramamurti Shankar:
Well, look at these functions. There are no complex numbers here. That's why everything is real. So, what problems have I solved now? First, I put
γ
= 0. No friction. And I just re-derived the harmonic oscillator because when I got the
cos (ω0 t - φ)
--Then I took a problem with friction. Then, I got a solution that was just exponentially falling because even though it looks like
α
plus, that's a negative number, that's a negative number, in the end both are falling. It says you pull the mass and let it go, it'll relax to its initial position, it'll stop. But all of you must know that there's got to be something in between. In the one case, I have a mass that oscillates forever, the other case I have a mass when I pull it and let it go, it goes back to equilibrium and reaches 0 at infinite time. But we all know that the real situation you run into all the time when you pull something and let it go; it vibrates and it vibrates less and less and less and less and then eventually comes to rest. Where is that solution? It's got to come out of this thing. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
That's correct. So, you've got to go back to the roots I found. For
α
, it's minus
γ
over 2, plus or minus square root of
γ
over 2 square, minus
ω0
square. I've taken
γ
over 2 to be bigger than
ω0
. So, what I did was I turned on friction but I didn't turn on a small amount of friction. I turned on a rather hefty amount of friction so that the friction term was bigger than the
ω0
term. But if you imagine the other limit where you have no friction and you turn on a tiny amount of friction, then the tiny
γ
over 2 will be smaller than this
ω0
. Of course, then you've got the square root of a negative number, right? So, you should really write it. So, let's take γ over 2 less than
ω0
, then you will write this as minus
γ
over 2, plus or minus
i
times
ω0
square, minus
γ
over 2 square. In other words, write this stuff inside as minus of this number now, and take the square root of minus 1 and write it as
i
.
So now, what do the solutions look like? They look like
x
equal to
Ae
to the minus
γ
over 2. Let me write the exponentials if you like.
Ae
to the minus
γ
over 2,
t
plus
iω
′
t
, but I'm going to call this combination as
ω
′. That's why we have
ω0
and
ω
′. Plus
Be
to the minus
γ
over 2 minus
iω
′
t
. Now
e
to the minus
γ
over
γt
over 2 is common to both the factors. You can pull it out. Imagine pulling this factor out common to the whole expression. Then, you just got
A
to the
iω
′, plus
B
to the minus
iω
′. That's a very familiar problem. If you want that to be real, you want
A
to be equal to the complex conjugate of
B
. Then, you repeat everything I did before, so I don't want to do that one more time. You will get some number C, times
e
to the minus
γ
over 2
t
, times
cos ω
′
t
, plus, you can add a
φ
, if you like. There.
So, what does this look like? What does this graph look like? It looks like
cos ωt
but it's got this thing in the front. If
γ
vanishes, then forget the exponential completely. This is our oscillating mass. If
γ
is not 0, imagine it's one part in 10,000, then for the first one second this number will hardly change from 1. Meanwhile, this would have oscillated some number of times. But if you wait long enough this exponential will start coming into play and the way to think about it is, it's an oscillation whose amplitude itself falls with time. And if you draw a picture of that, I think you will not be surprised that if you draw the picture it will look like this. It's called a damped oscillation.
So, that's the method by which you describe the three cases. One is no friction and one is small friction or friction obeying this condition, when you have oscillatory motion whose amplitude is damped with time. Then you have the other case where the gammas has crossed some threshold when
ω0
is smaller than
γ
over 2, then you get two falling exponentials.
So, what do you imagine the mass is doing? There's no friction if you pull it and let it go; it vibrates forever. That's not very realistic. If you turn a tiny amount of friction, it will do this, which is very ubiquitous. We see it all the time. You pull a spring and you let it go. After a while, it comes to rest. This tells you it never quite comes to rest because as long as
t
is finite, this number is going to be non-0, but it'll be very small. At some point you just cannot see it. Third option is overdamped. Overdamped is when
γ
is bigger than
ω0
over 2, then the answer has nothing that oscillates. Nothing oscillates, everything falls exponentially with time. That is, you should imagine you pull something, let it go, it comes slowly and stops. When you buy your shocks in your car, the shock absorbers, they're supposed to damp the vibration of the car. It's got a spring suspending the tires, but it's immersed in some viscous medium. So that is, vibrations are damped. So, when you hit a bump, if your shocks are dead, you vibrate a lot of times and slowly settle down. That's when your shocks are in this regime. When you bought them, they were in this regime. When you bought them they were doing this. Once you hit a bump and you overshoot from your position, you come down to 0 and you stay there. That's the ideal situation for damping. All right. So, I'm going to the last topic in oscillation but is there anything that you need clarification? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
Ah, yes. So, when
γ
over 2 equals
ω0
, this thing vanishes, and you seem to have only one solution,
e
to the minus
γt
over 2. You don't have the plus or minus, right. And we sort of know in every problem there must be two solutions, because we should be able to pick the initial position and velocity at will. If a solution has only one free parameter, you cannot pick two numbers at will. Now, that's a piece of mathematics I don't want to do now, but what you can show is in that case, the second solution looks like this. It's a new function, not an exponential but
t
times an exponential will solve the equation. Those who want to see that this is true can put that into the equation and check. In other words, pick your
γ
carefully so that the square root vanishes. Only a
γ
is left, but that
γ
is not independent of
ω
. That
γ
is equal to 2
ω0
. For that problem you can check that that's a solution, so is that. There are nice ways to motivate that but I think I don't have time to do that. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
Why was
A
equal to
A
star here? You mean here? Okay, take this
x
. Demand that when you conjugate it nothing should happen, okay. In this particular example, when
α
plus an
α
minus real numbers,
e
to the
α
plus
t
, remains
e
to the
α
plus
t
when you take conjugate. So therefore,
A
has to remain
A
star, and
B
must also remain invariant when you take the conjugation. In other words, if this was an imaginary exponential like in the other problem, when you take the conjugate, this exponential becomes this guy and that exponential becomes that guy. Then, by matching the solution, you will be able to show this must be the conjugate of that; that must be the conjugate of this. But if no imaginary exponentials appear, each term must separately be real.
Now, this is something you will have to think about. I'm not saying my repeating it makes it any clearer, so what I want you to do is take the
x
, take the complex conjugate of
x
, equate the two sides. There's a rule among functions that if you got
e
to the plus
αt
, its coefficient should match on both sides and
e
to the minus
αt
should have matching coefficients. It's like saying when two vectors are equal, the coefficient of
I
should match and the coefficient of
J
should match. There's a similar theorem that if you take a sum of two independent functions, equate it to the sum of [same] two independent functions, the coefficient must separately match. If you impose that you will find what I told you.
Chapter 6. Driving Harmonic Force on Oscillator [01:00:28]
Okay, now for the really interesting problem. The really interesting problem is this. I got the mass, I got the spring, I got the friction, but I'm going to apply an extra force,
F0 cos ωt
. This is called a "driven oscillator." So far, the oscillator was not driven. In other words, no one is pushing and pulling it. Of course, you pulled it in the beginning and you released it, but once you released it, no one's touching the oscillator. The only forces on it are due to internal frictional forces or spring force. But now, I want to imagine a case where I am actively driving the oscillator by my hand, exerting
cos ωt
force. So
ω
here is the frequency of the driving force, okay. That's why there are so many
ω
s in this problem. The
ω
′ that you saw here is not going to appear too many times. It's a matter of convenience to call this
ω
′. But this
ω
will appear all the time. When I write an
ω
with no subscript, it's the frequency of the driving force, and the equation we want to solve is
x
double dot, plus
γ
plus dot, plus
ω0
square
x
equal to
F
over
m
, because I divided everything by
m
,
cos ωt
. So, we've got to solve this problem.
Now, this is really difficult because you cannot guess the answer to this by a word problem. Now, you can do the following. If the right-hand side had been
e
to the
iωt
instead of
cos ωt
, you would be fine because then you can pick an
x
that looks like
e
to the
iωt
, and when you take two derivatives that look like
e
to the
iωt
, one derivative would look like
e
to the
iωt
;
x
itself would look like
e
to the
iωt
, you can cancel it on both sides. But what you have is
cos ωt
.
So, here is what people do. It's a very clever trick. People say, let me manufacture a second problem. Nobody gave me this problem. Okay, this is a problem you gave me. I make up a new problem, the answer to which is called
u
. But
y
is the answer to the following problem. The driving force is
sin ωt
, but this is what you give me to solve. This is my artifact. I introduced a new problem you did not give me, but I want to look at this problem. Now, here is a trick. You multiply this equation by any number; it's still going to satisfy the equation. Let me multiply by
i
. Put an
i
here, put an
i
here, put an
i
here, put an
i
here. Multiply both sides by
i
and add them. Then I have got
x
plus
iy
, double dot, plus
γ
times
x
dot, plus
iy
dot is
ω0
square times
x
, plus
iy
.
Let's introduce a number
z
, which is
x
plus
iy
. It varies with time. Then this equation, by adding the two equations, look like
z
double dot, plus
γz
dot, plus
ω0
square
z
is
F
over
me
to the
Iωt
. So, I have manufactured a problem in which the thing that's vibrating is not a real number. The force driving it is also not a real number. It's a
cos ωt
plus
I sin ωt
. But if I can solve this problem by some trick, at the end what do I have to do? I have to take the real part of the answer, because the answer will look like a real part and an imaginary part; I'll have to dump the imaginary part. That'll be the answer to the question I posed. The imaginary part of it will be the answer to the fictitious question I posed.
Now, why am I doing this? The reason is the following. If the driving force is
e
to the i
ωt
, I can make the following
ansatz
, or a guess.
z
is some constant times
e
to the
iωt
. I will show you now solutions of this form do exist, because let me take that assumed form and put it into this equation. Then, what do I get? I get minus
ω
square,
Z0e
to the
iωt
because two derivatives of
e
to the
iωt
give me
iω
times
iω
. Then, one derivative gives me
iω
times
γ
, times
z0
e to the
iωt
, and no derivatives, just leaves it alone,
e
to the
iωt
equals
F0
over
m
,
e
to the
iωt
. So, let me rewrite this as follows. Let me rewrite this as minus
ω
square, plus
iωγ
, plus
ω0
square, times
z0e
to the
iωt
, is
F
over
m
,
e
to the
iωt
. This is what I want to be true. Well,
e
to the
iωt
, whatever it is, can be canceled on two sides because it is not 0. Anything that's not 0 you can always cancel, and here is the interesting result you learn. For this equation to be valid, the
z0
that you pick here in your guess satisfies the condition,
z0
equals
F
over
m
divided by
ω0
square minus
ω
square, plus
iωγ
.
Now, parts of it may be easy, parts of it may be difficult. The easy part is to take the guess I made and stick it into the equation, cancel exponentials and get the answer. What you should understand is,
x
was what I was looking for. I brought in a partner
y
, and I solved for
z
, which is
x
plus
iy
, and
z
was assumed to take this form with the amplitude, which itself could be complex, times
e
to the
iωt
. If
z0
looks like this, then
z
, which is
z0e
to the
iωt
, looks like
F
over
m
,
e
to the
iωt
divided by this number in the denominator, I'm going to call
I
for impedance.
I
is called impedance and there's the following complex number,
ω0
square, minus
ω
square, plus
iωγ
.
Okay, we're almost done now. The
z
looks like
F0
over
m
,
e
to the
Iωt
divided by this complex number
I
. Imagine this complex number
I
. What does it look like? It's a got a real part and an imaginary part. Imaginary part is
iωγ
, real part is
ω0
square minus
ω
square. This is the complex number
I
. So, we are told the answer to our problem is to find this number
z
, then take the real part. Does everybody agree that every complex number I can be written as an absolute value times
e
to the
iφ
.
φ
, which is going to be here. And I'm going to write it that way because now things become a lot simpler if you write it that way.
F0
over
m
, divided by absolute value of
i
,
e
to the
iφ
,
e
to the
iωt
. Now, this
e
to the
iφ
, I can delete it here and put it upstairs as minus
iφ
. So, let me write it in that form. Then it's very easy.
F0
over
m
, divided by the magnitude of this
I
, times
e
to the
Iωt
minus
φ
, where
φ
is this angle. Well, now that
I
got
z
, I know how to find
x
.
x
is the real part of
z
. Now, when I look at real part, all of these are real numbers so I will keep them as they are.
F0
over
m
divided by
i
, and the real part of this function, I hope you know by now, is
cos ωt
minus
φ
.
And that's the answer. The answer to the problem that was originally given to us is the following. You know the magnitude of the applied force, the amplitude of the applied force. You know the mass of the particle. You need to find the absolute value of
I
and
φ
. For that, you construct this complex number whose real part is this, whose imaginary part is
iωγ
. Then, the absolute value of
I
is just by Pythagoras' theorem,
ω0
square minus
ω
square square, plus
ω
square
γ
square. And the phase
φ
obeys the condition
tan
φ
is equal to
ωγ
divided by
ω0
square, minus
ω
square square is
ω
square
γ
square. I'm sorry. It's just the imaginary part over the real part.
So, this is the answer to the problem that was given to us. But there's one subtle point you should notice, which is the following. Where are the three parameters in this problem? Everything is determined in this problem.
φ
, absolute
I
, all these are known, but we know every equation should have two free numbers. You know what they are? Anybody know? Okay, let me tell you what the answer to that question is. I'm saying, I can add to this the solution I got earlier on without the driving force, because in this problem, when I had a right-hand side with a driving force, let me add a 0 to that. That's harmless, and by superposition principle, if that force will produce that displacement, 0 will produce what? Well, we have seen all morning that even when the right-hand side is 0, they are the solutions I got for you.
e
to the
γ
over 2
cos ω
′
t
etc., so you can always add to this, what you call a complementary function, which is the solution of the equation with no driving force, which is what we were studying earlier in the class. But usually, people don't bother with this because they all have in them
e
to the minus
γt
over 2. So, if you wait long enough, this will die out, and this is the only thing that will remain. So at earlier times, this is not the full answer. You should add to this the answer when there is no driving force and together they form the full answer, and the numbers
A
and
B
that you have there will be chosen to match some initial conditions, like initial position, initial velocity.
Okay now, time is up. I'm going to stop, so I have not been able to finish some parts of this, so I'm trying to see what I can do. I had asked for you to give this problem set to me on--what is this today? On Wednesday, right. So, you don't have enough time. I mean, I haven't taught you a few other things you need about five minutes more of work. I don't want to keep you back. So, here is what I will do. I will post on the website some notes on just the missing part here, so you can read it and you can do one or two problems you may not be able to do without that. Then, I will come on Wednesday, I will teach that to you again, but you will be able to hand in your problem set. Okay.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_17_110606.mp3) |
