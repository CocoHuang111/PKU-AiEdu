- Source: https://oyc.yale.edu/physics/phys-201/lecture-12
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 12 - LCR Circuits — DC Voltage

### Overview

Like capacitors, inductors act as energy storage devices in circuits. The relationship between voltage, inductance and current in a variety of circuits with DC voltages is described.

### Lecture Chapters

1. Review of Inductors
2. Inductive Circuits
3. LCR Circuits Driven by an Alternating Source

1. 0
2. 287
3. 3259

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics II
PHYS 201 - Lecture 12 - LCR Circuits — DC Voltage
Chapter 1: Review of Inductors [00:00:00]
Professor Ramamurti Shankar:
Okay, I left you guys thinking about inductors last time, so I should start there. An inductor is very different from the resistor when you start doing circuit theory, because when you have a resistor and you connect some voltage to it, the current is determined by this equation. This is what I call an algebraic equation. It's an equation in algebra, one unknown. You solve for it by dividing and you get
I
at time
t
is
V
at time
t
divided by
R
. And you can make the network more complicated, put a few more resistors, put a few more there, a few more here, resistors within resistors. It doesn't matter, because we can always in the end combine the ones in series then lump them with the stuff in parallel, till the whole thing to the right of this is one single effective resistor. Then you find the current coming out of the sources as
V
divided by that guy. Then every time it comes to a branch, we sort of know how to divide it.
So resistor circuits are very easy. But now when you bring inductors, things are different, so I'm just going to tell you a little more about them. Here is an inductor. That's the symbol for an inductor. It's got some inductance
L
measured in henries. And the implication of that is the following: if you have a current going through this inductor, there is going to be necessarily a voltage with this polarity if the current is increasing. And the voltage you need is
LdI/dt
. This is the bottom line. Even if you skip all the other stuff about conservative forces, this, that, this is something you need to know how to do problems. The difference you notice is that the relation between voltage and current is not an algebraic equation, but a differential equation. This is called a differential equation. Now you don't have to worry, because I will tell you how to solve it, because I don't know if it's a prerequisite or not for this course. I once had a kid in summer school who when I started using partial derivatives, got very upset and said, "It's not a prerequisite. Why are you using partial derivatives?" So I told him, "When you come to class, there's always a danger you'll learn something new. You just have to learn to live with that." So I'm not going to leave you in the cold. If I do something you've not done, I will tell you how to do it, but I cannot avoid using certain notions.
So this one, even though it's called a differential equation and so on, if
V
is a constant, we can easily find the integral. It will be
V
over
L
times
t
. Okay, but now we're going to be interested in cases where
V
is not simply constant; it could be varying with time in an arbitrary way. So you take this guy, the first thing you notice is that the relation between current and voltage is given by derivatives. Second thing is, when a current flows through a resistor, whatever energy you provide is gone in the form of heat. It has dissipated. The light bulb glows and that's the end. With an inductor, when you drive a current, you are building a magnetic field inside the inductor and there's an energy associated with the magnetic field. And that stored energy will be given back to you later on. So it's like a capacitor. It takes a lot of work to charge a capacitor, because you've got to take charges from this plate and keep on piling them in that plate. It's a lot of work, but then if you connect that to a bulb and you squeeze the trigger in your camera, this charge is giving you the energy back. So the inductor and capacitor are different from the resistor in two ways: one is, the voltage across the capacitor is the charge on the capacitor divided by
C
, which if youlike is the integral of the current up to that time divided by
C
. Again, calculus comes in. So these are the two differences, the relation between current and voltage and voltage is differentiating or integrating, and these are energy storing circuit elements compared to this one, where energy is dissipated.
Chapter 2: Inductive Circuits [00:04:47]
So let's start with a simple problem where I have a voltage source. I'm going to take a fixed voltage,
V0
. There is a switch, there is a resistor
R
, and there is this inductor
L
. I'm going to assume the current is flowing this way, in which case — I'm sorry. You know, this picture's wrong. What's wrong with this picture? What is wrong?
Student:
The switch is open.
Professor Ramamurti Shankar:
The switch is open, okay. That's what's wrong, so nothing is flowing yet. But when I close the switch, then it's fine. Now it's flowing. And the question is, what does it do? How does it flow? After all, the inductor is a resistance free wire, so you may think current =
V0/R
will start flowing immediately, but that's wrong, because if such a current were flowing, there'll be an energy ½
LI2
with that current in it. And that energy cannot come from 0 to all of that in no time. There's no way to do that. Or if you like, if the current really grows rapidly or instantaneously from 0 to some value, that's a current,
dI/dt
is infinite here.
dI/dt
is infinite,
LdI/dt
is infinite. There's an infinite voltage needed somewhere in the circuit and we don't have it, so that would not happen. So current will have to be continuous, start from 0 and it will have to start climbing. The minute the current starts climbing up it starts flowing through this guy. There is the resistance times current voltage drop across this.
Therefore the amount of voltage available to drive current through this one or to increase the current through this one is reduced from
V0
to
V0 - RI
. That =
LdI/dt
. So you can see, as the current increases, the motivation to increase the current decreases, because this resistor starts swallowing up more and more of this voltage. So the growth in current will be very, very slow, and we expect that after a very long time, it will settle down to some value. What is that value? We can find that value by saying, "Wait until the current has stopped growing." That means
dI/dt
=0, that current will be
V0
/
R
and I'm going to give it the name
Iinfinity
, because it will turn out that you will reach the value only after infinite time. But you can get very, very close to that by waiting some reasonable amount of time, and part of what we want to do is, how long should I wait? Suppose I'm settling for 90 percent of maximum. When does that happen? Is it after 1 second or 10 seconds or 10 hours? What's going to decide that?
Well, once you have the right equations, you can figure everything out. So we're going to do that. So basically we are going to solve the equation
LdI/dt
. So let me show you one more time how it is done, this equation. You should know how to write it. Start anywhere you like, go round this guy. You gain voltage
V0
. Then go around this guy, you drop by an amount
RI
. You drop by an amount
RI
. And here you jump from this end to this end. Remember, you never go into the inductor. That's a bad zone. That's a zone where the potential is not even defined, but I've told you multiple times that even though there are non conservative things going on inside this, once you come outside, you just find a regular electrostatic potential difference =
LdI/dt
. So you drop again, and you come back to where you start, the whole thing should add up to 0, which means the equation is
LdI/dt + RI = V0
. That's what we want to solve.
So when you have this thing, as I told you, solving differential equations is a matter of guess work. There is no algorithm. You rely on what you've seen before and you guess the answer. You put some free parameters, you fiddle with them till everything works. And in this kind of problem, we can make everything work. Some problems we cannot solve. We can write the equations but we cannot solve them. This is something you're not used to when you take an elementary course like this one. But there are situations, for example, you know inside the proton there are these quarks, and the quarks interact with each other with entities called gluons. They're called gluons because they glue the quarks and form the protons and neutrons. We know the equations governing the behavior of the gluons. We cannot solve them. It's really strange. You have an equation but you cannot solve it. It's completely possible, because certain equations — every equation has a solution, but it does not mean you can write it down analytically. So quite often, one may be on top of the right answer, but one may not know how to solve it, so one doesn't even know if the theory is right.
So suppose this was the equation you got, but you could not solve it. It happens to be the right equation. You don't know what the answer looks like, you can never be sure this is the right equation. Similarly when Mr. Schrödinger invented his quantum mechanics, he wrote an equation that will tell you the energy levels of hydrogen. But luckily, he was able to solve it. By solving it, he was able to show that his equation gives the energy levels iand the spectra you expect from the hydrogen atom. So you have to remember that not every interesting equation can be solved, and I gave you the equation for these gluons, which we can write down but cannot solve. There is no function whose derivative we cannot take. There are lots of functions whose integrals we cannot do. That's simply asymmetry between those two. Here's a very simple function:
e−x2dx
from 0 to 19, or some fixed number, 0 to some
xmax
. It has a definite value. It's area under the graph, but no one knows how to write a formula for this in terms of
xmax
, where it's in closed form.
But anyway, this guy we can trample to death as follows. First we say at very, very long times, the current, I told you, is
V0/R
. That's when
dI/dt
is 0. So we're going to write the actual current in our problem as the current at infinity + some difference I twiddle. Standard thing, you take out the part you know and solve for the rest of it. So let's take that assumed form and put it into the differential equation. So when I do
LdI/dt
, this is a number,
V
over
R
. It has no d by dt. So
dI/dt
becomes
dI˜/dt
+
R
times
I˜
+
R
times
Iinfinity
=
V0
. Now you can see why we did that. We did that because now these two guys cancel and you get
LdI/dt
+
RI
= 0. That means
dI˜/dt
is −
R/L
times
I
. So we are saying, get me a function whose time derivative looks like the function itself up to a constant, and that's something we know from high school, is an exponential function. So
I˜
looks like some constant,
I0e-Rt/L
. You can take the derivative of this guy and out will come
-R/L
times the function itself. And
I˜0
is completely arbitrary. It's not determined by this equation. There's another useful property to know.
This is a linear equation. It means if you multiply both sides by 19, you get another solution which is 19 times the old solution. So the solution's overall scale is not determined by the equation. If I give you one solution, you can multiply it by any number you like, it's also a solution, because if you multiply by a number, say 9, the 9 goes into the derivative, 9 comes here. You can see 9 times
I˜
satisfies the same equation. So we don't know this number just from the equation, but we go back to what we know, which is
I
of
t
, is
Iinfinity
, which is
V0/R
+
I˜0e−Rt/L
. But I know that at
t
= 0, this guy should vanish.
t
= 0, this guy should vanish, because there was no current when I just threw the switch. So that tells me that equals 0. That tells me
I˜0
=
-V0/R
and we get our final result, which is
I
of
t
=
V0/R
times 1 -
e-Rt/L
.
So at this level, you are really doing physics the way we like to do it. We like to study things, write down some equations and solve the equations. Then we get a very precise prediction on what will happen. Because now we don't have to guess when the current will come to 90 percent of its maximum value. We can pick any number you like, because we can now plot this graph. And let's plot this graph,
I(t)
versus
t
. At
t
= 0,
e-0
is 1. You get 1 - 1, you get nothing. At
t
= infinity,
t
to the minus infinity is 0. Yes?
Student:
Over on the right where it says
I˜
sub twiddle = negative
V0
over
R
, should that be 0?
Professor Ramamurti Shankar:
This one? Yeah, right. Thank you. Okay, so now this exponential has a full strength of 1 at time equals 0. Goes to 0 at time equals infinity. Therefore it takes away exponentially small stuff at very large times. And if you want to know roughly how long should I wait, the answer is, the time you should wait is roughly of order
L/R
. Because you can write this as
e-t/τ
, where τ is
L/R
. Whenever we have an exponential, it will always be e to the minus a physical quantity divided by some number that sets the scale for the physical quantity. Exponentials fall exponentially. We know that. But how long should I wait? Well, if you wait
t
= τ seconds, then it will be 1/
e
, which is roughly 1 over third of the starting value and 1 minus that will be roughly 2 thirds of its value. If you wait
t
= 3τ,
e
-3 is 1 over 20, then you'll be what, 95 percent. So you can calculate everything you need in this simple problem.
So now let's come to the same problem. The switch has been closed for a long time and the current has stabilized. So here is the switch. It has been closed. That's my
V0
, that's
R
. And the current, you remember, is
V0/R
. This is
L
. So now we want to do something else. Now I want to open that switch. So what do you think will happen if you open that switch? Yes?
Student:
The inductor will resist the changing current.
Professor Ramamurti Shankar:
But how can it resist?
Student:
By inducing the magnetic field.
Professor Ramamurti Shankar:
It can do what it wants, but how does it drive a current through the open circuit?
Student:
From energy stored in the magnetic field.
Professor Ramamurti Shankar:
But in what manner will the current flow, given that I've broken the circuit?
Student:
In the direction —
Professor Ramamurti Shankar:
No, but how will it manage to go around? It's like removing the bridge, right? How will it go around? I agree with everything you said, but how will it make the circuit? Yes?
Student:
There'll be a higher concentration of charges on one side than the other.
Professor Ramamurti Shankar:
Yes, but how will you really get rid of the current in a circuit that seems open? Have you ever done this? Okay, that's just fine. But we know it has to get rid of that current, because otherwise, what happened to the energy? It has to go through. So you know what, you guys don't know what will happen if I pull that switch. Yes?
Student:
Is the current an electric field? The change in the magnetic field will create an electric field which doesn't need the closed circuit.
Professor Ramamurti Shankar:
Right, no I agree, it will have an electric field. But how will the electrons flow when the wire has been interrupted, is all I'm asking you? Yes?
Student:
Will the current oscillate, go back and forth?
Professor Ramamurti Shankar:
No. Yes?
Student:
You will have a static discharge.
Professor Ramamurti Shankar:
You will have a discharge. You will have an arc. You will have a flash, and that's when you'll hear a zip, and then it will jump this gap. So whenever you remove the switch, you have to be careful that there is not stored energy somewhere. You might think, "Hey, I am pulling the plug on — " well, I won't say who. You're pulling the plug, okay, and what can it do to me? Well, it can zap you, because this is a very dangerous place to pull the plug. So you know what people do? They have another resistor. Let's call this guy
R1
. This is
R2
and
R2
is a huge number, 10,000 ohms let's say. So most of the time,
R2
doesn't do anything, because when the current comes here in any situation, it looks at the inductor and looks at 10,000 ohms and it says, "I'm going this way." So primarily, it will all go there, okay?
In the end, when the switch has been closed for a very long time in our old experiment, when the current is stabilized, you remember
LdI/dt
0 here. So there's 0 volts between these two. That's the same 0 volt across
R2
. No current will flow in
R2
. Everything will flow through
L
. That current in fact will be
V0
over
R
, because this guy has been cut out of the loop. This is how it's going. But now if you throw the switch open, you have given it a path to discharge. So the inductor will discharge through the resistor. The current will continue to flow in this direction. Of course, it cannot flow forever, because the resistor will burn up the energy, but you're giving it a path. You're avoiding — in a way, if you like, this is also a path with very, very high resistance. The air is a path with very high resistance. That means by and large, there are no free carriers in the air. But if the two tips get really charged, just like you said, there'll be an emf that will pile up charges. They're jumping, they're waiting to jump the gap. Eventually they'll polarize air, which is electrically neutral, into + and - parts. Then the - will go one way, the + will go the other way. You'll recognize that as a discharge. But you don't have to worry about that now, because
R2
will take up your current.
So now the equation we write is
LdI/dt
+
RI
= 0 because if you start anywhere and you go around a loop, you have no change in anything. There's no voltage. And the answer to this one,
R2
, there
I
=
I0e
to the −
R2/L
times
t
. So now the current will decay exponentially. Again, with the time constant,
R2
over
L
, which is the 1 over the time constant, or the time constant is
L
over
R2
. So you put
L
in henries,
R
in ohms, you'll get some time. That will give you an idea of how many times that time you have to wait before the inductor is completely discharged. Well, it's never going to be fully discharged. It's going to take forever, but if you say, "Look, 1 thousandth of the original current is safe enough. How long do I have to wait?" you put .001 here and see what time you get. So you want
e−t/τ
to be .001. So every big inductor you have in a circuit you will find has got a resistor in parallel with it to take up the energy it has.
So let's do a little energy calculation. The energy calculation will be, I had energy in the inductor in the beginning, which is ½
LI02
. What happened to it? Well, we know what happened. There's a current in the circuit, and when the current is flowing in the circuit, it is dissipating heat in the resistor. Therefore the power in the resistor will be
I2R2
.
I2
is
I02
due to the minus twice
R2t/L
times another
R2
. Now we integrate this power from 0 to infinity, you will get
I0
2
R2
. The integral of
e
to the minus something is
e
to the minus that divided by that infinity to 0. I can promise you that what you will get will be
L/2R2
. It will give you then 1 over 2
LI02
. So this is not a surprise, that the stored energy in the inductor is driving your current. So if you want, one way to store energy, it's a capacitor, you charge it and it discharge when you want the current to flow. Or you can have an inductor, in which a current has been set up. Then when the power shuts off in your house and somebody throws the switch, that inductor can keep the light bulb burning, in fact forever. It will be infinite time before the bulb shuts down, but you won't be able to see anything after a while, because this graph is exponentially falling. This is a very simple problem where we can do the math and we can understand what it's doing. Yes?
Student:
The graph, what is that triangle thing?
Professor Ramamurti Shankar:
This one here? This is called τ. You mean that symbol? Tau is a unit of time whose numerical value is
R2/L
and we can write I as
I0e−t/τ
. We always like to write it in this form, so that if τ = 100 seconds, you will have to make many multiples of 100 seconds before the current is negligible.
Student:
What are the units on the axis?
Professor Ramamurti Shankar:
Oh, in this graph here? This is time and this is the current in the loop. It starts out at some initial value.
Okay, now I'm going to do the next slightly more complicated circuit, and that is an LC circuit. If you have a circuit like that, it won't do anything. You can take these guys, hook them up and wait all day. Nothing will happen because it's got no energy. Why should it do anything? It's just going to sit there. But if you've charged up your capacitor like this, and there's an open switch that you then closed, then those + charges are going to leave and find their way around the other side and neutralize them and the capacitor will discharge. But you know that once it discharges, it's not the end of the story. So why is that? Why doesn't it stop when the capacitor is discharged? Yes?
Student:
It's kind of like the inductor has momentum and it keeps pulling.
Professor Ramamurti Shankar:
The inductor would have had a current by then, so the inductor is not going to suddenly stop having its current. So it's going to keep driving more current for a while, until the capacitor's charged up the opposite way to an extent that this fights that one, that voltage, and then it will go the other way. So it will go back and forth. So let's write down the equation that tells you how it goes back and forth. So in other words, you should draw pictures. Textbooks have nice pictures and I won't even try it. In the beginning, it may look like — I'm sorry, in my example, in the beginning, there's an electric field here, nothing in the capacitor. After a quarter cycle, there's nothing here, there's a magnetic field in the inductor. Another quarter cycle, it's back here, but with the opposite polarity, and it goes back and forth. So we can get all that, by writing the equation
LdI/dt
+
Q/C
= 0. So let's write everything in terms of
Q
. Then
dQ/dt
is
I
, because as the current flows this way, it builds up charge. That's my convention. So I can write it as
Ld2Q/dt2 + (1/C)Q
= 0.
Now we have seen exactly this equation before, right? We saw the equation for a mass coupled to a spring the equation
md2x/dt2 +kx
= 0. Now we know what it does. We know it oscillates back and forth. And
L
— this is an SAT question —
L
is to
m
what
1/C
is to
k
. It's very useful to bear in mind this analogy, because mathematically, this equation and this equation have exactly the same solution. It's no more difficult to solve this one than that one. This may involve electric charges; that may involve masses. You don't care. So mathematically, here's an equation: cow times
d2
dog over
dt2
+ let's say elephant times dog = 0, where dog is a function of time, has exactly the same solution. What does it matter what you call the unknown variables, right? But you've got to tell me that cow and elephant are time independent and dog is the only thing that depends on time, because otherwise the equation is not the same. So here m and k don't change, L and C don't change. So what's the answer to this one?
Once again, it's the differential equation. You write
dQ/dt
squared is − (
1/LC) Q
and you're asking yourself, give me a function which, when I differentiate twice, looks like itself. There's always the exponential. There's also sines and the cosines and you can take any combination you like. And the one acceptable solution is some constant
A
times cosine square root of 1 over
LC t.
Is that right? Yes. If you take two derivatives of
Q
, you'll pull one over root
LC
each time, then you'll get a - sine when cosine becomes - sine and one more derivative will bring it back to - cosine. So this is called the frequency, which is 1/√
LC
. That's the analog of square root of
k
over
m
. Anyway, this will oscillate. It's a mechanical analog — it's the electrical analog of the mechanical problem. So I don't want to do too much of this, because I think you should be quite familiar with this, at least, the oscillatory behavior of this. And the analogy is perfect. For example, to say that I pulled the mass by 1 meter is to say that
x
was given a non-zero value and
dx/dt
was 0. Analogous thing here will be
Q
was given a non-zero value and
dQ/dt
which is
I,
is 0. That means the capacitor was charged, the inductor was not carrying any current. Then I let it go. What happens? The problems are identical. Yes?
Student:
When you solve the differential equation, why did you omit the sine?
Professor Ramamurti Shankar:
Yes, I should explain to you. That's an important point.
Q(t)
can be one number, cosine
ω0t
.
ω0
is this guy + another number sine
ω0t
. And both are acceptable. And the property of this differential equation is, if I have one answer, cos
ωt,
and another possible answer, sine
ωt,
then any constant times cos + any constant times sine is also a solution. You can verify that. If you have one solution,
Q1
, a second solution,
Q2
, you can add the two equations and you can show
Q1 + Q2
obeys the same equation. Not only that, suppose there's one problem you solve,
dQ1/dt
squared is
-ω
on
R
squared
Q1
. There is some function of time and here's another function of time, obeying the same equation. Now you can multiply this by a number
A
and you can multiply this by a number
B,
take the
A
inside the derivative,
B
inside the derivative and add the two sides. On the left hand side you will find the second derivative of
AQ1 + BQ2
. Right hand side, you will find
ω02
times
AQ1 + BQ2
. That means
AQ1 + BQ2
obeys this same differential equation.
This is called superposing two solutions. You've got one solution, another one, you can multiply one by a constant. It's very important it's a constant, because that's what will let you take it inside the derivative. Therefore the correct answer here is really
A
cos
ωd
+ Bsin
ωt
and you can ask, why did you write
A
cos
ω0t
? First of all, that's not a good solution. I can put a Φ there which is arbitrary. And it's not hard to show — let me call that
C
if you like,
C
. This can be written as
C
cos
ω0t
- Φ. In other words, it's possible to take either a solution with a cosine and a sine, with no extra phases inside, to another one with one amplitude and one phase. The phase is the delay in the cosine. Anybody here has trouble, who does not know the details, I'll be happy to explain why that's correct.
If you don't know, you should tell me now. You can check that if you take this thing, make a right angled triangle with
A
,
B
and
C
and an angle Φ here, then
A
can be written as
C
cos
Φ
and
B
can be written as
C
sin
Φ
, and that just happens to be cos
ωt
Φ
, this one, some trigonometry. So the differential equation, with the second order in time, will always have two unknown parameters in it. You can choose them to be these numbers
A
and
B
, or this number
C
and
Φ
. And the equation won't tell you what they are, because once you tell me there's a mass coupled to a spring and I say, "Okay, this is the spring constant this is the mass?" and I ask you, "Where is the mass right now?" I don't know. It depends on when you started it and how you released it. So I need to know what's called initial conditions, which is the value of
Q
or the value of
x
at the initial time and the value of the velocity or the current at an initial time. With those two pieces of information, I can solve for
A
and
B
.
This I think you should know, this kind of stuff you should know, so I won't say too much about that. All right, so now we do another problem. We put an alternating voltage on these guys. So this is
V0
cos
ωt
and this is
C
and this is
L
. Now we ask, what's the current? This omega is not the natural frequency of oscillation. It is some externally given omega, like 60 hertz from your power supply, from your socket. So that's driving the circuit and you can ask, what happens now? The answer will be, you write the same equation. You can write
Ld2Q/dt2
+
(1/C)Q
=
V0
cos
ωt
. Now what are you going to do? You have to again guess the solution. So I want a function,
Q
of
t
, so that when I take two derivatives and add it to some multiple of itself, I get something, something times the cosine. So what should that function look like? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
No, no, what function
Q
of
t
do you think will satisfy this equation? I'm asking for a function of time which, when I put into this, has some chance of obeying the equation. What's the functional form? Yes?
Student:
Cosine times some constant.
Professor Ramamurti Shankar:
Right. In other words, I can take it to be some constant,
C
times cos
ωt
, period. Not even times Φ. Take this one, see what happens. Now when you take one derivative, you get -
ωLC
cos
ωt
. When you take another derivative, you get −
ω2L2
— I'm sorry, this becomes sine times cos
ωt
, and this one is just oh my god — this is my nightmare. You can see the nightmare now? How many people see the nightmare? Yes?
Student:
Constant
C
.
Professor Ramamurti Shankar:
Yes, so I picked that
C
to be the same as this
C
. So we'll put a hat on this guy so we can tell them about. So
C˜/C
times
C˜
is
V0
cos
ωt
. And what this tells you is, if you take two derivatives — I'm sorry, this is so sloppy. If you take two derivatives here, you will get +
ω2
. cos
ω
be also be with the - sign.
Q/C
. Okay. You guys buy that? There is no
L2
, just an
L
. That =
V0
cos
ωt
. Right? Every derivative brings an ω and there's a net - sign. So you find out that your guess,
C˜
cos
ωt
is going to work, provided this equation is satisfied. And the cos
ωt
can be canceled. That's the whole point of doing this thing. So then you get
C˜
=
V0 - V0
divided by
ω2L − 1/C
. Or if you like, -
V0/L
divided by
ω2 - ω02
. Don't worry about the numerator; look at the denominator. The denominator says that if your driving frequency is equal to the resonant frequency,
C˜
blows up. That means when a system has got a resonance — yes?
Student:
Where did the
ω2
come from?
Professor Ramamurti Shankar:
I took two derivatives — oh, here. Oh, I'm sorry. Yes, thank you. You know, it's good to do these things slowly and not rely on what you heard somewhere. So let me do it for you again. Sorry about that. So this time I take two derivatives. Each one brings an
ω
. There is an L, and the - sine comes because the cosine becomes - sine. Differentiate one more, you get - the cosine. This guy is nothing. It just says "divide my by
C
" and that's equal to that. And then I wrote 1/
LC
is
ω02
. Thank you very much. Okay? I was really hung up on the final result, which tells you, you'd better not drive this at the resonant frequency, because then current amplitude will build up indefinitely. That's also true in a swing. If you've got a swing and the kid's coming back and forth, and you're reading a newspaper just pushing the kid, you've got to push at the right time to get the best result. And that kid's not going to fly off, because there's one more term in the equation for the kid, which is friction. But if you have a frictionless swing and you're doing this, you've got to watch out, because soon there'll be nobody around, because the amplitude will keep growing.
Well, these are unrealistic problems, but I want you to notice one thing. Here's what I want you to notice. The voltage you were given looked like
V0
cos
ωt
and the current that you got, I can obtain by taking the derivative of this charge, which is like
dQ/dt
. That's going to be
C˜ω
sin
ωt
, and
C˜,
we can write as
V0/L
divided by
ω2 - ω02sinωt
. This is
I
. Here's what I want you to notice. It looks a lot like Ohm's law, because the current looks like voltage divided by some number, but that's a very big difference. The voltage is a cosine and the current is a sine. That's something I want you to think about. The current is not in step with the voltage, whereas in a resistor circuit, the current follows the voltage. It's the same profile as the voltage, except you divide by
R
. Here one is a cosine, one is a sine. That means when one guy is at maximum, other is at minimum. It's called out of phase, in fact out of phase by 90 degrees. Yes?
Student:
________ by the
C
that you got, where did the omega go?
Professor Ramamurti Shankar:
Here?
Student:
On the other side. When you multiply that through by the
C
—
Professor Ramamurti Shankar:
Oh,
ω
did not go, it's back. Right here. You're right. There's the
ω
. That came from... Okay, these problems, the only thing I'm focusing on right now, I would say of all the things I wrote there, to be the most important thing is number one, this is what I want you to bear in mind. That's why sometimes I'm not paying attention to some constants. What is important to notice is that this is an equation you can solve by inspection. Why was it easier to solve it by inspection? Because you are trying to get in the end a cosine to balance the right hand side, and you're trying to find a function who is itself a cosine, or whose second derivative is a cosine, and we know the answer to that is a cosine, so we can guess the answer. Once you guess the answer, you put it in and you analyze the solution, you notice also that the current and the voltage are not in step. One is a cosine. You know what a cosine does, it does that. Other is a sine, so they are out of step. When one is at maximum, the other is at minimum and so on.
That means a current as a function of time is not equal to the voltage as a function of time divided by anything. There is nothing you can divide a cosine by to turn it into a sine. Whereas with resistors, you just divide by R, you get the current. Now for the more realistic problem, the realistic problem has got a capacitor, an inductor and a resistor and no other power supply. The equation obeyed by this one will be
Ld2Q/dt2
(that stands for
LdI/dt
) +
RdQ/dt
+
Q/C
= 0. This is analogous to
md2x/dt2
+ (I don't know how you guys wrote this thing last semester. It doesn't matter) γ
dx/dt
+
kx
= 0. Notice that it's the same form. And I'm going to give this to you as a homework problem to analyze the answer to this one. So this describes a problem where you have a mass and a spring and some friction on the table. This means if you pull it and let it go, the oscillations will eventually get damped and it will die down. And the general solution for the case when it's oscillating will look like some number A
e
to the minus some number αt times cosine times some frequency
ω't
. Let me see. You can always add a phase
Φ
, but I'm not going to do that. If you want, you can put an extra Φ, but I'll choose my origin of time so that I don't have that. This is what the answer's going to look like, where
ω
' and
α
are going to be controlled by
L, R
and
C
. That's the thing I don't want to do in class. Have you seen this before? Professor Harris tells me you've seen this last time. And the hints in the homework will guide you on how to do this. You just assume the solution
x
at
t
looks like some
A e
to the - (I don't want to call it
α
now)
β
times
t
. You put it in the equation and solve for
β
and you'll find
β
will have a real part and an imaginary part. And you have to combine the two to get this answer.
Now that brings me to another thing, so I don't know how prepared you guys are for what's about to happen next, which is the use of complex numbers. So everybody familiar with complex numbers? Who doesn't know complex numbers? How do you do your taxes? You don't know imaginary numbers? So I will tell you. I'll give you a lightning review. I'm assuming everybody has seen them in high school. I will only tell you the part you need, but I'm going to assume that I can use them fluently. I don't want to stop every time and worry about you guys. So I really need a show of hands. Anybody never seen
x + iy
and
x - iy
? And how about
eiθ
? You know that guy? Okay, that's all you need. So I'm going to tell you what the deal is. So everyone knows what a complex number is. We know
i
is square root of -1. Then we know that we can write a complex number as
x + iy
and visualize it in a complex plane where you measure
x
this way and
iy
is measured that way. That's usually called a generic complex number
z
. But now let us find the length of that — the complex number is a single point in the complex plane. The length of that is square root of
x2 + y2
. So I can also write
z
as
x
divided by square root of
x2 + y2
+
i
times
y
divided by square root of
x2 + y2
times the square root of
x2 + y2
. Just done nothing, just rearranged stuff.
This is going to be called the modulus of
z
, and what is this? This angle is
θ
here. This is really cos
θ
+
i
sin
θ
times modulus of
z
. And that, thanks to this great identity by Euler, is
eiθ.
Now I don't know how much you know about this great formula that relates
eiθ
to cosine + sine. How many people know where it comes from? What does it mean to raise
e
to a complex power? You know where it really comes from? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar:
It comes from power series. It turns out you can write a power series for cosine. You can write a power series for sine, then, for example, cosine of
θ
= 1 −
θ2
over 2 factorial,
θ
to the 4 factorial, or 6 factorial, etc. And you can write a power series for
eθ
if you like, which is 1 + θ +
θ2/
2. This defines cos
θ
in the sense that if you put
θ
=
Π
/2 in this infinite series, you will get 0. And if you put
θ = Π,
you will get
Π
-1. In other words, in spite of this funny looking form, it really is the same guy. It will oscillate, it will have zeros, it will be periodic. None of it is obvious, but this power series is numerically equal to this one if you keep the infinite number of turns. Likewise,
eθ
is defined by this series. And similarly, there's a formula for sin
θ
. Now once a power series is defined, you can put e raised to anything you want there.
So you know what I'm going to put there.
e
raised to dog is 1 + dog + dog squared. This is not a joke. This is really true. This is the definition. If someone says, "How do I raise
e
to the power dog?" you do this. This will have all the properties of the exponential. It doesn't matter what's in the exponent. That's the key. People originally put real numbers, then they put complex numbers. Now they put matrices, operators, anything you want.
e
raised to anything, you formally define to be this infinite series, provided the infinite series converges and gives you a meaningful answer. In that sense, if you put
eiθ
here, and compare the result to cos
θ
+
i
sinθ, it matches, that's all. I'm just going to keep using that result. Then you should also know that for every complex number, there's a complex conjugate, which is
x - iy
. That means
i
goes to -
i
. That means
z
, the angle
θ
will change to -
θ
. And given any complex number, the real part of
z
, which is
x
, is
z + z*
over 2 and the imaginary part of
z
, which is
y
, is
z − z*
over 2
i
.
This is what you need to know. Every complex number has a real part and an imaginary part. In fact,
z*
looks like this. And if you add
z + z*,
the vertical parts cancel and you get double the horizontal part. That's why you divide by 2. You subtract and divide by 2
i,
you get
y
. Basically, that's all I want you to know, but I want you to be able to manipulate them rapidly enough. Here's something very useful about complex numbers. Let's take a complex number
z1
which is mod
z1eiθ1
, and another complex number,
z2
, which is mod
z2eiθ2
. So what do they look like? Well,
z1
looks like this, with some angle
θ1
, and
z2
may look like that. It's got some angle
θ2
. So every complex number has a length and an angle. You can think of it two ways. It's got an
x
part and a
y
part, and a real and an imaginary, or it's got a modulus and a phase. That's the Cartesian version of the number and the polar number of the number. And the connection between them comes from Euler's formula.
But now look what happens when I take the product
z1z2
. I get mod
z1
mod
z2 eiθ1 + θ2
, because exponentials add when you multiply them. Well, this allows you to immediately guess what the product is going to look like. The product is going to have a length equal to the length of
z1
times length of
z2
. It's going to have an angle, I've not done a good picture here, which is the sum of the two angles, because it's
θ1 + θ2
. So listen to this statement very carefully. When you take a complex number, say number 1, and you multiply it by a second complex number, you do two things to the first guy. You rescale it and you rotate it. So two operations are done in one shot when you use complex numbers. The mod
z2
rescale is the mod
z1
and
θ2
adds to
θ1
. Likewise, if you divide, if you take
z1
over
z2,
it is mod
z1
over mod
z2
times
eiθ1 - θ2
, because the exponential
θ2
is downstairs.
So multiplication by real numbers is very easy. You take a real number 4, you multiply by 8, you'll get something in the real axis 8 times longer. You multiply by -8, you'll get something back here. With complex numbers, you take a number, you multiply another number, you rescale and you rotate. That's what I want you to know. That's going to be very important for what I'm saying.
Chapter 3: LCR Circuits Driven by an Alternating Source [00:54:19]
Now I come to the problem I really want to solve, which is an LCR circuit driven by an alternating source,
V0
cos
ωt
. This is
R
, this is
C
and this is
L
. And the equation we have to solve is
L dI/dt
+
RI
+ 1
/C
integral
I
dt
=
V0
cos
ωt
. Because
Q
is the integral up to time t of the current, that's just
Q/C.
It's the same equation, but now, unlike in this problem, where I had no driving voltage, I have a driving voltage, and I've also written it in terms of current rather than in terms of charge. Because in electrical engineering, you don't really watch the charge in the capacitor. You look at the current flowing through the circuit.
So you have to solve this equation. The question is, can you guess the answer? That's the only way we know. You've got to guess. You're trying to find a function,
I
of
t
, so that when you differentiate it, you get a cosine
ωt
, when you integrate it, you get a cosine
ωt
. So far we can do it. Sine
ωt
will do it. But when you leave it alone, then also you get a cosine
ωt.
You cannot do that, because sine will become a cosine and sine will become a sine. In the LC circuit, when you didn't have this guy, we were okay, because if you pick a sine, this became a cosine and that also became a cosine and you can combine them to get a cosine. But you cannot have
dI/dt
, I and integral of I all in one equation and all satisfied by trigonometric function.
The only time we can guess the answer is if it looks like
V0eαt
. Suppose that was the voltage. Then can you guess the answer, what form the answer will have? It will also be
eαt
times some number, because then this will look
eαt,
that will look like
eαt
, that will look like
eαt
.
eαt
has a great property that whether you multiply it, whether you integrate it, differentiate it or leave it alone, it looks the same. Unfortunately, no one's interested in this voltage, because it's growing exponentially fast, or if you put a - sign, it's dying exponentially. What we really want is this. So the question is, how do we solve this problem with cos
ωt
? So we're going to use a certain trick. The trick I'm going to use is the following: let me take a general case where this is some function
V
of
t
, where I'm not even assuming
V
is real. I'm not assuming
I
is real, but
L
and
R
and
C
are real. Everything else can be complex numbers.
Now once you have an equation and you've found a solution, if you take the complex conjugate of both sides, they will still match. Do you understand that? If two things are equal, their complex conjugates are equal, because this thing is the real + imaginary that balances the real + imaginary on the other side. Complex conjugate just reverses the imaginary terms, so they will still match when you flip both sides. So it means if you take
L dI*
of
dt + R
times
I* + 1/C
integral
I* of t' dt'
t
= V*
of
t
. So star is the rule by which if
V
had a real and imaginary part, you flip the imaginary part. So that solution for
V
of
t
implies a second equation. In other words, if the voltage
V
drives a current
I
, the conjugate of the voltage drives the conjugate of the current. That simply follows from the equation. It comes from the fact that when I conjugated it,
L, R
and
C
are real.
Do you understand that? Suppose
L
were imaginary or had imaginary part, then I must also put a conjugate on
L
. Then
I*
obeys a different equation, because this had
L
in it, this had
L*
in it. But if everything is real,
I*
obeys the same equation when you have a
V*
driving it. I'm almost done now. I want you to add the left hand side to the left hand side and the right hand side to the right hand side, and what do I get? Well, if I write it here, you may not be able to see it. Let me put it here then. If you add these two, you'd get
L d/dt
of
I
+
I*
+
R
times
I
+
I* + 1/C
integral of
I + I* dt
=
V + V*.
This again comes because the equation is a linear equation. You can always add the left hand side and the right hand side to get another problem where the driving voltage is
V + V*
and the driving current is
I + I*,
etc. But
I + I*
is 2 times the real part of
I
and
V + V*
is 2 times the real part of
V
. Therefore this implies that
L d/dt
of the real part of
I
+
R
plus the real part of
I +
1/
C
times the integral of the real part of
I
= real part of
V
.
So let me say in words what the equation means. If you by luck solve an equation with a complex potential V, and you get a current, then the answer to the problem where the potential is only the real part of the actual potential you applied, the current will be the real part of the answer you got. That's all I want you to know. If you solve a complex problem with a driving voltage which is complex — which is just a mathematical fiction, in real life you don't have that — then the current that you get will also be complex. But its real part will be due to the real part of your voltage. And you can also show the imaginary part of the current will be due to the imaginary part of the voltage. This is just the principle of superposition.
So here is the trick we are going to use. We are going to go back to original equation,
LdI/dt + RI + 1/C
integral
I dt
= V0cos
ωt
, and we're going to solve a new problem. We're going to solve a problem where this is
V0eiωt
. And the current for that, I'm going to call some
I˜
. It's a complex current, because the driving voltage is a complex voltage. So think of
Veiωt
as the
V
in the previous problem.
The actual problem I was given had V0cos
ωt
, but you know that
V0eiωt
is
V0
cos
ωt
+
I
times
V0
sin
ωt
. Consequently, this potential has a real part which is a cosine, an imaginary part which is a sine, and the current will have a real and imaginary part. The answer to the original question is the real part of the answer to this question. This is what you should think about. This is what you should understand. So I've manufactured a problem with an unphysical complex voltage, and all I know is that at the end of the day, if I take the real part of the current, I'll get the answer to the real part of the potential, which happens to be the actual potential,
V0
cos
ωt
. So why would I do all this? Why would I take a problem that's bad enough with the cosine and turn it into a complex exponential? I think you can sort of guess what the reason is. The reason is that it may be complex, but it's still an exponential.
That means its derivative is going to look just the same. That means I can make a guess that the current
I˜
is proportional to
eiωt.
So you can make the assumption that
I˜
of
t
is some constant
I˜
times
eiωt.
Make that assumption and put it into this equation and see what you get. You will find you will get
IωL
times
I˜
+
R
times
I˜
+ 1
/IωC
times I˜ times eIωt is V0eiωt. This is because if you assume the current is an exponential, every derivative = an
iω
and every integral = 1/
iω,
and multiplying is just multiplying. So
d/dt
has got to be replaced by
ω
, and you get this equation for
I˜.
That means you will satisfy the equation, provided
I˜
times all of this =
V
. And I'm going to write this as
Z
times
I˜ = V
where
Z
is the name for all the guys multiplying
I˜
. So I'll start with that here.
Okay. So I wrote
iωL
+
R + 1
over
iωC I˜ eiωt
is
V0eiωt
. Everybody get that? That's because differentiating on an exponential is just multiplying by the exponent. So this is a complex number.
R + iωL − i/ωC
. I want you to know that
i
in the bottom is like -
i
in the top. And this is called the impedance
Z
, it's a complex number. You can visualize the complex number as follows: it's got a real part, which is
R
. It's got an imaginary part, which is
ωL − 1/ωC
, and the impedance
Z
is a complex number with some modulus and some phase. If you know the real and imaginary parts, you can construct the modulus in the phase like that. If you want, it's the modulus of
Z
. Therefore canceling this, I find
I˜ = V0/Z
. That becomes V0 over the modulus of Z times eiΦ, where Φ is this angle defined by tanΦ = ωL − 1/ωC divided by R. So don't worry too much about writing all of this down, because this you're going to find in every book. There's nothing novel or different.
So this is the formula for
I
twiddle. Now
I
itself, you remember, =
I˜
of 0. I'm sorry, this is
I˜
of 0. Did I define it that way? Yeah, I should write it — I'm sorry. I should write it as
I˜
of 0. There's a subscript 0 there, because the full I twiddle has got an
eiωt
in it. That looks like
V0
over mod
Z
times
eiωt -
Φ
. But this is not the physical current, because it's the result of a complex voltage. The physical current is a real part of this, without the twiddle, that we write as real part of
I˜.
Where do I get the real part?
V0
and absolute value of
Z
are both real. Real part of
e
to the
i
something is cosine of something and that's our answer. That's our answer, the final answer you get.
This tells you that the current has a magnitude which is
V0
over the absolute value of
Z
, and it's got a phase
Φ
by which it is behind the driving voltage. The magnitude of
Z
for as in any complex number, if someone says, "What's the magnitude of
Z
?" it is simply square root of real part squared + imaginary part squared.
So I want you to think about the magic of complex numbers. Your final answer has a current which is a cos
ωt
Φ
. Your driving voltage is a cos
ωt
. There is no way you can divide the voltage by anything to get that current. But in the complex language, the complex current is the complex voltage divided by the complex impedance. How does the happen? That happens because impendence
Z
has got a magnitude and a phase, therefore if you had a voltage
V0eiωt
and you divide by mod
Z ei
Φ
,
that becomes
e-i
Φ
upstairs. You're able to change the magnitude and you're able to change the phase by dividing.
So if you want to take the voltage and you want to rescale it and shift its phase, all in one shot, you can do it if you divide by a complex number, because a complex number will rescale it and also shift its phase. And then you take the real part. In other words, cos
ωt
divided by nothing will give you cos
ωt -
Φ
, but
eiωt
, when divided by
ei
Φ
, will in fact give you
eiωt - i
Φ
. So that phase shift we can produce only by dividing with a complex number. So I'll come back and explain to you a little bit more on how you do circuit problems using the complex impedance, but I think it will be helpful for those of you who don't know complex numbers to get use to this part of it.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/spring10/phys201/mp3/phys201_12_021710.mp3) |
