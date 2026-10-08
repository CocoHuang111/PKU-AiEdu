> 检索摘要：Open Yale Courses「PHYS 201 LCR Circuits — AC Voltage」。主要内容：讨论交流 LCR 电路理论背后的数学，用复数把微分方程化为代数方程，引入阻抗，以收音机说明共振和可变电容，复习经典电磁学并引入位移电流以得到完整麦克斯韦方程组。页内标题：Lecture 13 - LCR Circuits — AC Voltage；Overview；Lecture Chapters。分隔线后是英文原文，未翻译、未改写。

- Source: https://oyc.yale.edu/physics/phys-201/lecture-13
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 13 - LCR Circuits — AC Voltage

### Overview

The mathematics underlying LCR circuit theory for AC currents is discussed. Complex numbers are used to convert differential equations to algebraic equations. The notion of impedance is introduced. The radio is used to illustrate the concepts of resonance and variable capacitance. The body of classical electromagnetism treated so far is reviewed and summarized. The displacement current is introduced, leading to the complete Maxwell equations.

### Lecture Chapters

1. Review of LCR Circuits
2. Impedance
3. Resonance and Variable Capacitance
4. Displacement Current

1. 0
2. 528
3. 1059
4. 4083

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics II
PHYS 201 - Lecture 13 - LCR Circuits — AC Voltage
Chapter 1: Review of LCR Circuits [00:00:00]
Professor Ramamurti Shankar:
I thought I would go back a little bit to LCR circuits. I think that's one of the more useful things you learn in this course. I want to do it carefully so everyone's on top of that. So remember that the problem you want to solve looks like this. That's an AC source. That is a resistor. There's an inductor and a capacitor. And that's the circuit. And this voltage we take to be
V0
cos
ωt
. That's the kind of voltage that will come out of any AC generator. The omega is controlled by how the turbine is spinning. That frequency is the same as this frequency. Our job is to find the current in the circuit. Now what makes it difficult is that, unlike DC circuits where you take a voltage and divide by some effective resistance, the equations here are not algebraic equations but differential equations. So we'll write it down then I'll tell you how we handle it. So the equation for this circuit, you begin as usual, you go around the whole loop and you add everything to 0, then you will find
V0
cos
ωt
=
R
times
I
+
L
times
dI/dt
+ 1 over integral of I up to time
t
times 1/
C
. That's the voltage. Everybody with me on that part?
That determines the condition, that determines the current at every instant in time. So if you can solve this equation, you solve for the current, but what's difficult is that it's not an algebraic equation. It's not like
V = IR
, where you divide by
R
, you've got the current. This has got integrals, it's got derivatives. But it turns out that if the voltage is
V0
cos
ωt
, there's a very clever way to solve this problem, which takes it back almost to the good old days of
V = IR
. No differentials, no integrals, nothing. That's the magic. That was invented by an engineer from GE called Steinmetz. He put to work some ideas that may seem esoteric, because they involve complex numbers, but it makes life tolerable for people doing circuit theory.
And here is the trick: I ignore this problem, and I solve the following problem, purely mathematical device. The problem I solve has a voltage
V0eIωt
. We all realize that you cannot get a source that does that, but it's pure mathematics. Then the solution to that problem, that voltage, I assume, will drive some current I call
I˜
. So
I˜
is the answer to the problem where the driving voltage is not real, but this, if you mathematically write the same equation. But now we realize that
I˜
can be complex.
I˜
is not real. It can be a complex number. Just because the voltage is a complex number, it's an equation, it's got imaginary and real parts on the left hand side, it will have imaginary and real parts on the right hand side, and so you'll need both to make it work. But if you have solved this problem, I claim you have also solved this problem. Why? Because if you take this equation, which is a complex equation, then the real part on the left hand side will match the real part on the right hand side. Imaginary part will match the imaginary part. That's because if you have two complex numbers,
z1
and you say they're equal, you mean
x1 + Iy1
is
x2 + Iy2
. And they can be equal only if these guys are equal, those guys are equal. The real part has to match, the imaginary part has to. You cannot borrow from the real part and give to the imaginary part. They're apples and they're oranges, so you've got to match them separately. The closest analog is a vector equation. If you have a vector equation and you equate two vectors, so you say vector
F
is
m
times vector
a
, then
Fx
will be
m
times
ax
and
Fy
will be
m
times
ay
. So there are two equations in one single vector equation, three in 3D and a complex equation, there are two equations.
So let's take the equivalent of the real part in the left hand side and the real part in the right hand side, and what do you get? The real part of this is the most important thing. The real part of this is cos
ωt
. that's because
eiωt
is cos
ωt
+
i
sin
ωt
. The real part is just cos
ωt
. On the right hand side, I should take R times the real part of
I˜
. Let me just call that guy
I
. Then I should take
L
times the derivative of the real part of
I˜
, which I want to call
I
. Then 1/
C
times the integral of the real part of
I˜
, the real part of
I˜
I want to call
I
. In other words, let the real part of
I˜
be called
I
. Then we notice that this
I
is exactly the
I
that we want. It satisfies exactly the equation we want to solve. So we have some good news and some bad news. The good news is that if you solve this equation, you've also solved this equation. The bad news is, if you cannot even solve the real equation, what makes you think you can solve this complex equation, right? I cooked up another problem that looks even more difficult and I say, "Hey, if you can do that, we can do this."
Well, it turns out this complex problem is actually easier to solve than this guy. I'll try to tell you why it's easier to solve. If you come to this equation, I've told you repeatedly, any equation involving derivatives and so on, you guess the answer and you put it in. You try to make a guess. I'm trying to guess, what kind of function
I(t)
has the property that when I multiply it by
R
, I should get a cos
ωt
, when I differentiate, I should get something like cos
ωt
, when I integrate, I should get cos
ωt
? That's the only way left and right will match, and neither cosine nor sine will do the trick. If you pick the sine, then when you differentiate it, you will get a cosine that matches. This one integrated, you will get a cosine that matches this, but this will contain a sine. On the other hand here, since this exponential, if you make the choice
I˜(t)
, it's
I˜0eiωt
, it is going to work. It is going to work because if you take
R
times that, you get
R
times
I0eiωt
. If you take the derivative of this guy, that's
Iω
times the same current. Integral is 1 over
Iω
times the same thing.
That's the beautiful property of the exponential, that when you differentiate it, just like multiplying by
iω
. When you integrate it, it's like dividing by
iω
, and when you multiply by
R
, it's like multiplying by
R
. So if you take this assumed solution and put it into that equation, let's see what we get. We get
e0
eiωt
= (now allow me to jump one or two steps, because I did it last time. Try to do this in your head.)
R
times
I˜
is going to contain
R
times
I˜0eiωt
. How about
L
times
dI˜/dt
, then I come with the
d/dt
, this guy is a constant. This brings me an
Iω
, so I write
IωL
times the same thing. When I integrate, I get 1 over
Iω
times the 1/
C
that looks like that. So the time dependence, this is a time dependent problem, but miraculously, time dependence matches on the two sides.
Chapter 2: Impedance [00:08:48]
And now we get this equation,
V0 = R + iωL + 1/iωC
times
I˜0
. And our goal was to find
I˜0
, so
I˜0 = V0
divided by this complex number
Z
. This complex number
Z
is called the impedance, and it =
R + iωL + 1/iωC
, for this problem. I'm not telling you the answer for every problem, but for this problem, life is very simple. You find that current as a voltage divided by a number, just like dividing by
R
. The only trick is, there are two catches now. First catch is, this number is not real, so you've got to get used to the fact that you will work with complex numbers. If you're willing to work with them, you get this. Second thing is, this is not the current we were supposed to find. What's the current we were supposed to find? The current that I wanted was the real part of this
I˜
. That means it's the real part of
I˜0eiωt
divided by — sorry. That's correct. That's what I want. And that's going to be then the real part of
V0
over
Z eiωt
. We always pick
V0
to be a real number. The amplitude on the voltage you can take it to be a real number. Then you write it as a real part of
V0
divided by
Z ei
Φ
. So I should tell you what this is. I'm saying, imagine the complex number Z, plotted this way. This is R, this is
iωL − 1/i − i/ωC
, and this is the complex number
Z
. This is the angle
Φ
. Then you write the same complex number in polar form as a modulus and
ei
Φ
.
So now you find
I
of
t
is the real part of
V0
over mod
Z eiωt -
Φ
, and that we know is
V0
over mod Z cos
(ωt −
Φ)
.
So that's the final result. That's the answer to the original question. Now you know trigonometry well enough to know that cos
(ωt −
Φ)
is really cos
ωt
cos
Φ
+ sin
ωt
sin
Φ
. So the answer cannot be just a cos and cannot be a sine. It's a suitably chosen admixture of sines and cosines that does the trick.
So if you want to, if you say, "I don't want to deal with complex numbers" you can take a guess like this and put it in the equation, and after a lot of manipulation, you will find there is a
Φ
satisfying this condition. What's the property of
Φ
? Tan of
Φ
is
ωL − 1/ωC
divided by
R
. But the beauty of the complex numbers is, it just comes out in one package as the phase of a complex number. I also told you to think about how you could do this with real numbers. It's not going to be easy to take a voltage, which is cos
ωt
, divided by anything, to get a current which is cos
(ωt −
Φ)
. There's nothing you can do to a cosine which will shift its phase. But if you're working with complex numbers, you can take
eiωt
divided by
ei
Φ
and turn it into
eiωt -
Φ
. So in the imaginary world, it's very easy to shift the phase, because a complex number, when it multiplies or divides another number, rescales and rotates it. So in the complex plane, it's very easy to attach the phi, and at the end of the day, you take the real part.
So you can imagine doing any realistic problem. Suppose I tell you
R
is 10 ohms, where
ω
is some 100
Π
.
L
is 3 henries and the capacitance is 2 microfarads, you can find
Z.
Z
for this circuit will be 100 — I'm sorry
Z
will be 10 +
ωL
, will be 100Π times 3 henries − 1/
ωC
, is 100
Π
times 2×10-6. That's some complex number. I forgot the i here. That is a complex number. I don't want to calculate it. It's whatever it is. Then it's got a real part which is 10, an imaginary part, which is this algebraic sum of these two. You can actually plot the real values you get here in this problem. I'm just going to show you the 10. The other guy's whatever it is, and you can get the phase. That tells you that in this problem, the current will have an amplitude which is the volts you apply, maybe you applied 100 volts, and you divide by this absolute value of
Z
. So if you want, I'll complete the last part. The absolute value of
Z
, like for any complex number, is
R2 + ωL -
1 over
ωC
squared, right?
Any complex number, the absolute value is real squared + imaginary squared under root. So let's write in all its glory the current that we want.
I(t)
is
V0/R2 + ωL
- 1 over
ωC
squared cosine of
ωt -
Φ
where tan
Φ
=
ωL − 1/ωC
divided by
R
. Here is the picture, here's
R
.
ωL
minus
1/ωC
. There's
Φ
. There's a complex number
Z.
Okay. So you can imagine now putting numbers and getting what you want. Notice that the current lags the applied voltage. For example, if cos
ωt
is a maximum of
t
= 0 and
Φ
was 45 degrees, you'll have to wait till
ωt
is 45 degrees before the current reaches a maximum, so it will be lagging the voltage. But sometimes Φ can come out negative. Can you see how
Φ
could come out negative? This angle
Φ
need not be positive, do you understand that? What would make it negative? Look at the formula there,
ωL − 1/ωC
. Yes?
Student:
If 1/
ωC
is bigger than
ωL
.
Professor Ramamurti Shankar:
Right. If 1 over
ωC
is bigger than
ωL
, this will be more negative than positive. The complex number may end up like that. So I've written it for one possible sign. If that flips sign, the
Φ
itself will change sign. It will become
ωt
+ 32 degrees. It can go either way. It depends on who is dominating it, whether the inductor or the capacitor is dominating it. So let's look at the answer for one other interesting feature.
I want you to know two things. This trick works only if the voltage is a pure oscillatory function like cos
ωt
. But then you can write it as a real part of
eiωt
and do this. Secondly, the impedance is not a constant. Whereas the resistance is just 10 ohms, impedance varies with frequency. It's a frequency dependent number that you divide the voltage by to get the current. So the consequence of this is the following.
Chapter 3: Resonance and Variable Capacitance [00:17:39]
Suppose you plot here the magnitude of the current, let's call it
I0
. This whole thing, let me call it
I0
. That's the amplitude of the current, as a function of frequency for a given applied voltage
V0
. So
V0
is fixed, but when
ω
varies, these numbers are varying. When
ω
goes to 0, you've got a 1 over 0 in the denominator. That's going to beat everything. And 1 over 0 squared in the denominator means the whole thing vanishes. The current starts out as 0. That corresponds to the fact that if your voltage had been a DC source instead of an AC source — that's what
ω
= 0 means — the capacitor will charge to some point and then stop the current. That's it. Then it will go up, then come down, because at very large
ω
, the
ωL
is going to dominate. You get 1 over
ωL
squared under root, that looks like 1/
ωL
. It will fall like 1/
ω
at very large frequencies. And it will be the maximum when these two guys cancel each other. So you've got
R2
. If you're trying to get the maximum current, there's nothing you can do about
R2
. It is what it is. But you can play these two guys against each other and find a frequency
ω
and
R
so that this is true and that
ω0
is just related to the resonant frequency of the LC combination. So at that frequency, the current amplitude will be simply —
I0
maximum, will be simply
V0/R
. It's as if
L
and
C
are not there. You've got them there but they're not there. They're not doing anything. They neutralize each other. So you can ask, why put something in that doesn't do anything? Well, first of all, it does something on other frequencies. Only at one magical frequency, they go away. But what is interesting is the very sharp response you have. So do you know where that comes into play?
Student:
Resonance?
Professor Ramamurti Shankar:
Resonance, yeah, but which part of your life? Pardon me?
Student:
Radio.
Professor Ramamurti Shankar:
Radio. You guys know what that is, because I don't. You're always carrying some recorded medium. But if you listen to radio, like in the old days, you have this room full of radio signals. Everyone wants your attention. All the radio stations are all sending signals right now in this room, and you want to pick just one station that you like. So what happens if that station sends that information at a certain
ω0
? And if that's all you want, you go to the store, buy an LCR circuit, with
L
and
C
chosen so that
LC
is
1/ω02
, then you will get a huge response when you get the signal from that station. Now there's another station with a different frequency. You don't want to listen to them, but you have to listen to some of them, because if their frequency is here, your response to that station is not 0. It's a lot smaller than this, but it's not 0, and there may be yet another station you can hear in the background.
If you don't want to hear them, you would like to get 0 signal from them, but you cannot kill this function except at one frequency, but you can make it very sharp. If
R
is very, very small, this function will be very large at resonance, because
V0/R
will be a huge number. It will also be very narrow, so you can make this thing very sharp. And that's really controlled by the ratio of
R
to
L
. So other stations do give you weak signal, but you can make them weaker and weaker by picking a very finely tuned oscillator. Now the question is, what if you changed your mind and you want to listen to these guys? What should you do? Can you go and buy one radio for this station, one radio for that station? You know you do something, right? You fiddle with the dial, but what do you think it does? Yes?
Student:
Changes the capacitance.
Professor Ramamurti Shankar:
Changes the capacitance. It's not easy to change the inductance, but it changes the capacitance. Nowadays if you open a radio, I don't know what you will see. It's all glued on to something. But in the old days, when all the parts were big, you can open the radio and look inside and you have a capacitor which is called a variable capacitor. You show that with an arrow. You can also have variable inductors, I suppose, but this is very common. Now how do you vary the capacitance? Capacitance you know is
ε0A/d
. Yes?
Student:
Can you change the surface area?
Professor Ramamurti Shankar:
You can change the surface area, but how do you think you can go change the surface area?
Student:
Having two half circles and then the current rotates around.
Professor Ramamurti Shankar:
That's right. You've got these interlocking plates and you can have them fully overlapped or not overlapped. If you draw the plates like this, it's got many things. And these plates can be either really overlapping with the other plates or pulled out. When you turn the dial, the two things move in and out, and that varies the capacitance. That will give you a range of frequencies and that's the range you can hear.
That's one thing. Another thing I want to mention is, this solution I wrote down,
I(t)
is
V0
over mod
Z
cos
(ωt −
Φ)
has no free parameters in it. You tell me the time, I tell you the current. Whatever the voltage is, you take that, shift the phase by
Φ
and divide by mod
Z
. But you know that a second order equation in time must have two free parameters, so where are those free parameters going to come from? Have you seen this before in your math whatever? No? Okay, I'm going to give you a clue and you have to think about this clue and see what you get out of that.
V0
cos
ωt
=
V0
cos
ωt
+ 0. That's your clue. What can you do with that clue? Yes?
Student:
Set the original equation equal to 0 to find the complementary solution.
Professor Ramamurti Shankar:
Yes, so I will translate. If you have a problem where you apply one voltage,
V1
and you get a current
I1
, and a second voltage
V2
and you get a current
I2
, just by adding the two equations, left hand side to left hand side and right hand side to right hand side, you can check that
V1 + V2
drives a current
I1 + I2
. If you don't see that, you should do that. Take that equation, but any
V
of
t
, get an answer due to
V1
, call it
I1
, another due to
V2
, call it
I2
and add them up. Left hand side is clearly
V1 + V2
and the right hand side,
R
times
I1 + R
times
I2
is
R
times
I1 + I2
and so on. So
I1 + I2
will satisfy the equation when the driving voltage is the sum of the two voltages. It all comes because there's nothing nonlinear. For example, for the right hand side at
R
times
I
2, then the first equation will have
R
times
I1
2, second will have
R
times
I2
2. When you add them, you'll get
R
times
I1
2 +
I2
2, but what you want is really
R
times
I1 + I2
, the whole thing squared. So if you have nonlinear terms, you cannot add solutions, but if you have linear terms, you can add solutions.
Therefore 0 is a hint. It says, add the solution for 0 voltage. You might say, "There is no solution for 0 voltage," but I will have to remind you that we did solve the problem the other day of an LCR circuit connected to nothing that had a current flowing for a while. But it won't do it if it's completely inert. But if you have put some charge on this guy to begin with, then you saw that the current and the charge, everything starts and oscillates exponentially like
e
to the - some number
t
times some cos
ω't
- some other phase, call it
χ
. And this thing had two free parameters. There's an area here and a
χ
here. Or you can write it as
e-
γ
t
times
A
cos
ω't
+
B
sin
ω't
. No matter how we write it, this function, this solution to 0 external voltage is called a complementary solution, and the final solution for
I
is really what I wrote,
V
over mod
Z
cos
(ωt −
Φ)
, + this complementary function.
Because if you take this complementary function and add it to the equation, you might think it will mess up the equation, but it won't, because the I that I wrote down will give me V0cosωt. The complementary function, when you take
RI
+
LdI/dt
+ 1 over
C I dt
for the complementary part, you will get 0, because the complementary guy obeys the following equation: it obeys the equation
L dI/dt + R
times
IC
+ 1 over
C
integral
IC dt
is 0, is the equation satisfied in that loop. If it has a non-zero solution, you can add it to your equation. See, in elementary calculus, you learn that if you solve an equation, say
dF/dx
=
x2
, the answer is
x2
/2 +[
x3
/3] a constant, because when you add a constant, you don't screw up the solution, because the d/dx kills the constant. Question is, what can you add to this differential equation? You can add anything, any function, that's annihilated by that differential equation. If you put the function in, you get 0 from all the derivatives and integrals, you can add that to anything.
Therefore the true answer is this + complementary function. It will contain these two parameters A and B and you pick them depending on initial conditions. In other words, if you took an LCR circuit and took a generator and you hooked it up, from the instant you hooked it up, it won't immediately assume this form that I have here, because for example, at
t
= 0, maybe the current is 0 in the real problem. This current doesn't vanish, but you should add to this, this function. Choose A and B so that the current vanishes at the = 0. You can fit the actual experiment to the solution by choosing A and B to match the initial current and say the initial charge in the capacitor. But we don't usually care about this guy. Do you know why we don't talk about this too much? Yes?
Student:
It dies off.
Professor Ramamurti Shankar:
It dies off exponentially, so in real life, it doesn't matter. If you really want to know what's happening, in other words, take an LCR circuit, take an AC source. Put a switch, keep the switch open. The minute you close it, the current will be 0 by continuity. Current cannot jump. So this function obviously is not the whole answer. It doesn't vanish at
t
= 0. But this extra part you add in with suitably chosen A and B will fit those initial conditions. But after oscillating for a while,
e
to the - something
t
for a long
t
will just go away. Then it will settle down only to this function. This is called a steady state current and this is called a transient current. So transients are important; you cannot ignore them. Maybe a transient will burn your circuit, but it doesn't matter after a long time. If you survive the early time, it doesn't matter for the long time. It's a lot like this course.
Okay, all right, so I want to take a minute to tell you a little more about the use of these complex numbers. I do it for a lot of reasons. Now I don't know what field you guys are in. You could be in art history. You just don't know when complex numbers are going to be relevant to what you do, you just don't know. But I'm serious, if you're doing engineering, electrical engineering, mechanical engineering, it's all about complex numbers, because everybody writes a differential equation. If it's a linear differential equation, you solve it with complex numbers. And I like to also show you why sometimes we should not resist the mathematics so much, because you might think in this circuit I don't need complex numbers. After all, in the end, the answer was a cos
(ωt −
Φ)
and that is cos times some number + sine times some number. I can put the combination and fiddle with it till it works, that's true. But suppose I gave you a more complicated circuit.
Here's a more complicated circuit. I have maybe a resistor, an inductor. Then I come here, I have a capacitor, maybe another inductor. Go like that, let's call it
R1, L1, C2, L3
and this is some
V0
cos
ωt
. How are you going to solve this problem by guessing? You have no idea how to guess. You cannot solve this problem by guesswork. But I claim that if you replace this fellow by
V0eiωt
, you'll be able to guess the answer, you'll be able to solve the problem. So I want to take a minute to tell you why that works. So do you know what I'm trying to do now? I'm trying to tell you that an arbitrarily complex AC circuit built of resistors, inductors, capacitors, connected any way you like, add whatever you want, if you go back to the differential equation, it will drive you insane, because there is a derivative of this current, derivative of that current, integral of that current, all coupled in some way. How are you going to solve it? You cannot guess anything cosine and anything sine. It's going to be a madness. But I will show you that if you use complex numbers, you can reduce the problem to something that looks like a DC circuit. That's all I want to do.
So I'm going to give you the idea, but I don't want to do the whole thing, because I don't want to spend too much time on algebra. For those of you who want to know where it comes from, I want to give you a chance. Those of you who don't want to know exactly where everything comes from, in the end, I will give you the so called bottom line, stuff you must know, then you'll forget all this. So let's take that problem. Let me take an easier one that this one, because it's got too many wrinkles in it. But the point I'm making, I can illustrate just as easily with this guy. So what did I call it?
R1, L1, C2, L3
. Let the current here be
I1
. Let the current here be
I2
, current here is
I3
. And this is
V0
cos
ωt
. Our job is to find those currents if they're all oscillatory functions of time, in magnitude and in phase. If you do that, you're done. So how do we do it normally? What are the fundamental equations for a circuit? The fundamental equations are that at every branch, the incoming current should be equal to the outgoing current, which for us means
I1 = I2 + I3
. So
I2
and
I3
come down here and they join and become
I1
again, so I'm going to assume that and write
I1
there.
So I've got two unknown currents,
I2
and
I3
. That's the first thing to understand, how many free, independent currents there are. Generally, if it's a simple problem, it's equal to the number of loops you have. That's a loop here, that's a loop there. You can draw many other loops, like that one and that one, but they will not give you any new results. So you've got to write voltage equations that say if you go around a loop, and you come to where you start, the change is 0. The equation I would write would be
V0
cos
ωt
= (I'm going to take this loop)
R1
I1
+
L1 dI1/dt
+ 1 over
C
integral
I2 dt'.
Back to here is 0. That's one equation. For the second loop, I can go around the other way if you like, going round this inductor, or I can take a loop like this. I just want to write that to show you what it may look like. That equation will say
L3 dI3/dt
- 1 over
C2
integral
I2 dt
= 0. The - sign comes because if the current is assumed to flow this way, and your loop goes counter to the current, you're going uphill, so everything should be subtracted, but if you go down, you can write it going down this way. So these are the three equations to solve.
They're complicated because there are differentials, integrals and you know what. But if I solve the following problem:
V0eiωt
— so don't bother to write all of this, because you're not responsible for this detail. I just want you to know what's going on. So I scrap this problem and I solve this problem, and the current for that I take to be the twiddle, okay? I say, let the
I˜
's be the answer to this problem with
eiωt
. Can you see that if I took the real part of the first equation, I get the correct equation for the physical currents; that if I took the real part of the second equation, everywhere I replace
I˜
by the real part which I call
I
, and this becomes
V0
cos
ωt
, I get a second voltage equation. And here again you drop the twiddles by taking the real part, that's the equation satisfied by the physical currents,
I2
and
I3
. So it is still true, even in this complicated problem, that once you've solved it, you may take the real part of the voltage and take the real part of the current anywhere, that's the answer to the primordial problem.
So why does this make life easy for you? Because now you may take the current. I'll just take one of these as an example. Let the current be current
I˜1
, let it be
I˜1,0eiωt
, and
I˜2 = I˜2,0eiωt
, and
I˜3
is
I˜3,0eiωt
. Make that guess, and what does this mean? Think about it? Go to the first equation. Equate these twiddle guys and all the
eiωt's
cancel on all the three terms, so you get an equation that says
I˜1,0 = I˜2,0 + I˜3,0
. No time dependence anywhere. It looks like a DC equation. And let's go to this equation here. You will find
V0 = R
times
I˜1
+
iωL1I˜1
+
1/iωC
(I should have called this
C2
)
ωC2
times
I˜2
.
eiωt's
have been canceled everywhere. So what do you find? This again looks like an Ohm's law problem where R1 is the impedance of this guy,
iωL1
is the impedance of that guy, so the whole thing looks like some
Z1
times
I˜1
+
Z2
times
I˜2
. In other words, let me just write it below this here.
The equation we get is,
V0
=
Z1
times
I˜1
+
Z2
times
I˜2
. So the problem will look like this: just put some black box here,
Z1
, another black box,
Z2
, another black box,
Z3
, join them, bring them out. Call the current here as
I˜1,0
, the current here is
I˜2,0
, the current here is
I˜3,0
. And these constant numbers, they have no time dependence, obey the same equations as the real currents did in the real problem. So it's like a DC problem. The only subtlety is, the impedances are complex, and the rule for impedance is very simple. If you open the box and you find a resistor + an inductor, the impedance for that is
R1 + iωL1
. That's it. Apart from that variation, it is just like DC circuits. Yes?
Student:
Is there any physical significance to the imaginary part of the solution?
Professor Ramamurti Shankar:
No. If you want, the imaginary part of the solution is the answer to a person whose voltage was
V0
sin
ωt
. So you are solving two problems, but we believe that it's nothing new. If you can do cos
ωt
, the answer to sin
ωt
is the same, except you shift by
Π
/2. Everything looks the same. But it answers that question.
Okay, so this is what I want you to know. Given an AC circuit, here's what you do. You make this rule: whenever you see this guy, it is
R
. Whenever you see this guy, it is
iωL
and whenever you see this guy, it's 1/
iωC
. Then you can combine impedances in series by adding them, or in parallel by doing the reciprocals and adding them, then taking the inverse of that. It's all like DC circuits. What will you have at the end? At the end, you will have found out every current
I˜0,α
.
α
is 1, 2 or 3 in this problem. You solve these DC like equations and you will find these DC like currents, but they'll be complex. What is the relation of this guy to the actual current flowing through the actual circuit element?
The answer is
Iα(t)
will be
I˜α
times
eiωt
, then take the real part. That's the algorithm. That's the relation between these time independent functions, because what did you do? You stripped their time dependence. You wrote every current as
eiωt
times a number that doesn't depend on time. It's those numbers that we have solved for. But to go back to the original current, first you've got to reinstate the exponential you canceled everywhere and remember to take the real part because that was the deal. It's called the real deal, real deal. You take the real part of your answer.
How about following? You've solved a very complicated circuit. I don't even know what's going on. Here's one guy. It's part of a big mess. Its impedance is
Z
. There is a current,
I˜0
going through it, meaning it's the complex amplitude of that. If I ask you, what is the actual voltage across this? If I put a volt meter here, what will I measure? Answer will be, again,
I˜0
times
Z
. That's in the fake Ohm's law calculation, but you've got to remember that these all had time dependence, which I removed. Then you've got to remember that I should take the real part of the answer.
That will be the actual instantaneous voltage across that circuit element at that time t. But remember,
I˜0
could be a complex number. The
Z
inside the box could be a complex number. When you multiply them, you've got lots of complex numbers. You add on to get this guy and take the real part. I would recommend, when you come to such problems, that every complex number like
Z
, you write as an absolute value times e to the i times some phase. That makes your life easier, because then the whole thing will be the absolute value of this times the absolute value of that, times
eiωt
+ the phase of this + the phase of that. And the real part of it is the cosine of
ωt
+ these two phases. You understand? So if you wrote it as mod times
ei
Φ
1
, absolutely value of
Z ei
Φ
2
, times
eiωt
, what is the real part of this crazy number? These are all real numbers? You pull them out, combine the exponentials, you'll get
eiωt + i
Φ
1
from this one,
i
Φ
2
from that one. So the full current will be cos(
ωt +
Φ
1
+
Φ
2
). So the answer will be mod
I0
mod
Z
cos(
ωt
+
Φ
1
+
Φ
2
). So I don't mind waiting to give you some time to digest this. You should be able to at least solve simple DC circuits with more than one loop. If you've got only one loop, just do what we did earlier, V over Z and all that. But if you've got two loops, you should learn how to handle that problem, because it's very useful. You're going to deal with circuits no matter what you do. Yes?
Student:
In the initial problem, if you were just trying to find the total current through the system, impedances add, like —
Professor Ramamurti Shankar:
That's what I said. That's correct. So let us ask the following question. His question was, what if I'd like to know the current coming out of this guy? Right? Everybody with me? That was his question? So we do it as if everything were real. First we combine these two guys into a single impedance, which will be
Z2 Z3
divided by
Z2 + Z3
, just like you combine resistors in parallel. To that guy, I will add
Z1
. That whole thing is the impedance seen by this thing. Divide the voltage by this total effective impedance, that will give you the current coming here. Yes? Take that current, multiply by
Z1
times
eiωt
, take the real part. That's the instantaneous voltage on this one. Here's one more thing: when that current comes here, how is it going to branch between these two? In DC circuits, if this was
R2
, this is
R1
, and the current comes here, its propensity to go on this side is proportional to that resistor, because if that is more resistive, it's more likely to go here. So the fraction going to this side will be
R2
divided by
R1 + R2
. The fraction going to this branch will be
R1
divided by
R1 + R2
. You replace all of the
R
's with
Z
's and you get the same result.
So you can do everything like before, except you've got to get used to complex numbers. Here's the problem: take the circuit assigned to each element, these impedances. Add them like in the old days, combine them like in the old days, solve for the current. To get the physical current, multiply by
eiωt
and take the real part. To find the drop against any entry, any element, take the current there times the impedance, times
eiωt
, then take the real part. That's it. I cannot say it anymore because I don't know another way to say it. You've just got to do problems so you get a feeling for how it's done. I wanted you to understand, sometimes you take a problem, you embed it in a bigger family of problems that looks more difficult, but is actually easier. It's even true, there are many integrals you try to do which are very difficult. But if you think of it as an integral in the complex plane, sometimes that problem's easier to solve than the real integral, so this happens a lot. You take a problem, you generalize it. Sometimes the generalized problem is easier than the original one.
Now I'm going to give you one counter-example, let me see where to pick it, where this rule about taking the real part at the end of the day fails. So far the rule was, do everything with a complex thing. At the end of the day when you've found something, you take the real part. Here is a place where it does not work, so let me tell you where it is. Take the LCR circuit, where we found that the voltage was
V0
cos
ωt
, and the current was
V0
over absolute value of
Z
cos
(ωt -
Φ)
, where
Φ
is all that stuff. I don't want to repeat it. What is the instantaneous power generated by the power supply? The instantaneous power for any voltage source equals the voltage at that instant times the current at that instant. And all of these are real voltages and real currents. I'm not doing any games right now. This is the real thing. So what do you get here? You get
V02
over mod
Z
cos
ωt
times cos
(ωt -
Φ)
. That's what it is, right? One voltage going like cos and the current is going like cos
(ωt -
Φ)
. So I want to write this out for you as follows: this is cos2
ωt
cos
Φ
+ sin
ωt
cos
ωt
cos
Φ
. This is just some high school trig identities. Cos of
A
+
B
is cos
A
+ cos
B
+ sine
A
sine
B
. So what do you notice? Cos
Φ
and sin
Φ
are some constants, but these are functions of time and they're all oscillating. The reason they are oscillating is that when you drive a current in these circuits, sometimes the
L
and
C
are drawing energy from the source, sometimes they're giving it back. So sometimes it's not monotonic, it's not always drawing energy. Sometimes it's taking it, sometimes it's giving it back. That's all the oscillatory terms. So what one likes to study is called the average power over a full cycle.
That means you take this time dependent function, you integrate it over time, over a full cycle at frequency ω and you divide by the time. And I ask what you get. So let me write the obvious parts,
V02
over mod Z. Cosine square is a positive definite number. Its average over a cycle is 1 half. I don't know how you want me to show this. One is to say cos2
θ
is 1 + cos2
θ
/2. And if you integrate that guy over a full cycle, the cosine 2
θ
is periodic. It gives you 0, you get 1 half. Sin
ωt
cos
ωt
, if you put a 2 and divide by 2, is proportional to sin2
ωt
. That guy completes 2 cycles in one period. Its average is definitely 0. So the only thing that survives then from all of this is the cosine
Φ
term and the 1 over 2, because average of cosine squared is half. So the average power in the circuit looks like
V2
/2 mod
Z
cos
Φ
. That's the correct result. In fact, we can see it in another way. Let's write it as
V0
over mod
Z
squared times mod
Z
cosine
Φ
over 2. What is mod
Z
cos
Φ
? Can you tell from some picture I drew of
Z
? I don't know if I have any picture. I've hidden all of them. But here is what
Z
looks like. That is
Z
, that's
Φ
, this is
R
, this is
ωL
− 1/
ωC
. What is mod
Z
cos
Φ
? Yes?
Student:
Shouldn't it just be R?
Professor Ramamurti Shankar:
It is just the resistance. So this is a fancy way for
R
. So this is just 1 over 2. If you want, it's just the amplitude of the current squared times
R
. That means the real energy loss is taking place only in the resistor. You can write that as mod
Z
cosine
Φ
if you like. The 1 half is new to AC circuits. In a DC circuit, it's just
I2R
, because it's constant. Here it's oscillating like a cosine squared and the average of that is 1 half. So what people sometimes like to do is to find something called the RMS current, which is
I0
/√2, and to define the RMS voltage, which is
V0
/√2. Then the whole thing looks like
I0Irms2R
, or if you like,
Vrms
times
Irms
, period. Now RMS means root mean squared. There's a reason why for a trigonometric function, it's got a number which is 1 over root 2 times the amplitude, but I don't want to go into that, because we don't use it again. The main thing to know is that, if you want, you can redefine a new quantity,
V0
/√2 and
I0
/√2, so that these factors of 2 disappear, and things look like the good old days of resistive circuits.
So very often when they say this is a 110 volt power supply, they really mean the RMS value 110 volts. That means
V0
/√2 is 110.
V0
itself is 110 √2. So the actual voltage goes up and down from +110 √2 to -110 √2. Because for computation of power, the peak amplitude doesn't control it. It's this RMS value that controls the average power consumption. Now there is a way to get the power using the complex numbers, if you like. I'm going to assign that as a homework problem, rather than do it here. But I want you to think about why does it fail here? Why is it that when you come to the power, this is not simply — in other words, what I'm telling you is the power is not simply the real part of
I˜t
and
V˜t
.
V˜
is a 1 with
V0eiωt
. Why is it that taking the real part of this guy doesn't work? Everywhere else, we took the real part of the current, we got the right answer, real part of the voltage, we got the right answer, but not when you take the real part of this. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
Yes, he's saying you're multiplying but not adding. So let me say the following: suppose you had a complex number
Z1
, it's
x1 + Iy1
, and another complex number
Z2
, which is
x2 + Iy2
. If you take the real part of
Z1
you get
x1
. You take the real part of
Z2
you get
x2
. But suppose you wanted
x1x2
for some reason. That is the real part of
Z1
times the real part of
Z2
. That does not = the real part of
Z1Z2
. Because the real part of
Z1Z2
has got
x1x2
, that's pretty obvious, but it's always got -
y1 y2
, because when these two imaginaries multiply, they can contribute a real part. But what you wanted is the analog of this one. So you can fix that. I mean, it's not that you can never extract
x1x2
. The correct solution is
x1
is
Z + Z*
over 2 x2
Z2
+
Z2*
over 2, and you can multiply it all out and see what happens. Then you can write the answer in terms of these guys, if you like, but I'd rather just leave it this way, because it's not going to be used extensively. I just want you to be careful. This is an example of something that is quadratic in the interesting quantities. You cannot take the real part at the end of the calculation, only for things which are linear.
Every time, the real and imaginary parts do not talk to each other throughout the whole calculation. You can follow them through and at the end take the real part as what's interesting. But if you're going to multiply two things, where you have added on a complex part to this guy and a complex part to this guy, in the product, you've added on something real, and that was not your intention, so you've got to take that out. That's what makes it complicated. Therefore I tell you that when you do these AC circuits, when it comes to power, forget any of the gimmicks you learned. You will be usually asked to find the power only for LCR circuit, the single loop like that, then just go back to this one. It's just
I2R
written in this language. And cosine
Φ
is called the power factor.
Okay, so this completes one chunk of the course. I'm really going to the finishing line for electromagnetic theory. There's only one big stuff left, then we'll do optics and then we'll do quantum mechanics. Now the nice thing about quantum mechanics is that you don't have to worry about whether you will get it, because nobody gets it. My idea is to take a class where only I don't get it, and turn it into a class where everybody don't get it. That's the plan. When I say "get it," I think I talked to one of you guys who called me and said something which is quite true. They said, "In the first part of the course, we could visualize what you were doing. There were masses rolling down and things colliding. With electricity and magnetism, we're not afraid of the math, but we don't have an intuitive feeling for these things." So I agree. But if you work long enough with electricity and magnetism, you get used to them. The only things born with the knowledge of electricity and magnetism are some creatures, like ducks.
Apparently, ducks can feel the earth's magnetic field and they are just going through and they know which way to go. They don't solve Maxwell's equation, but they know how to travel. And some bees are sensitive to the polarization of light, so they do respond to certain things in an intrinsic way people don't. So you have to get used to it only by doing more problems. But in quantum theory, any intuitive feeling you have is actually a detriment. It will get you in trouble, because nothing is the way you imagine it. So no one has an advantage over anybody else. So it's better not to be well informed. So you may be saying, "Hey, here is the course for me," right? So the less you know, the better off you are in quantum mechanics. So don't worry about that. It's a very strange world and I want to give you an introduction to that. Anyway, they are the two things. So what's left now is just electromagnetic waves, and we're sort of building up to electromagnetic waves.
So I'm going to start by writing here the equations that we know about electromagnetism as of now. So the surface integral of the electric field on any surface is the charge enclosed divided by
ε0
. That's called Gauss's law. The line integral of the electric field on a closed loop used to be 0 when things are static. But when things are changing with time, it's the rate of change of the magnetic flux. The surface integral of the magnetic field,
B⋅dA
is just 0 all the time, because there are no magnetic monopoles. There's nothing from which lines come out. So if you integrate any configuration, the lines don't start and end anywhere, so whatever enters the surface leaves the surface. The surface integral of
B
is always 0.
B⋅dA
is 0. The line integral of
B⋅dA
—
b⋅dl
is
μ0I
. That's the old Ampere's law. These are the four equations we have. Now it turns out this is not still the end. It's not the end. There's one more fiddling you have to do. That's the last part I want to talk about.
Remember, this itself came from new experiments where you started moving magnets and so on, found a current whenever there's a changing magnetic flux. That's the induced electric field due to changing flux. So here is the thought process that led Mr. Maxwell to a little paradox. So here is some circuit. We don't know where it begins or ends; we don't care. Here's the circuit. There's a current flowing through a capacitor. When I say flowing through a capacitor, I hope you know what it means. I want you to be very clear about this. Suppose you connect it to some AC source. I want you all to know what's going on. Nothing really flows through the gap in the capacitor. It's not possible. What happens is, for a while, + charges rush here and - charges rush the other plate, because that's the polarity of my AC source. Later on it's reversed, then - charges go here and + charges go there. So there is an alternating current in the circuit, but there is no current flowing right through in one sense. But there's nothing to keep it from going this way and that way and this way and that way, because they don't have to jump the gap to do that. Yes?
Student:
It's sort of a random question, but you know how we were talking about jumping the gap. When would it actually jump the gap?
Professor Ramamurti Shankar:
It will jump the gap if the — here is what happens. It depends on what's in the medium. If you put air, for example, the air molecules are all neutral, so there is no way for the + charges to ride them and go to the - charge, to the - terminal. But if the electric fields, this certainly will produce electric field, they're so strong that they rip out the + and - charges, that suddenly you've got a bunch of free carriers, then the - charges can immediately go and neutralize this one, + can go and neutralize that one. That's like a lightning strike inside the little world. That's what happens to us during lightning. We are in a capacitor. The lower plate is the earth, upper plate is the clouds. And after a while, there's a heavy charging. At some point, they cannot take it anymore, and they ionize the air and they create a little path and the current flows through that, and the clouds are discharged.
Okay, so here is a problem that Maxwell had. He says, let's look at this equation,
B⋅dl
in a closed loop =
μ0I
, where I is the current passing through any surface with that loop as the boundary. Remember that? So if you draw a loop here like that, then some current is crossing that shaded surface. And the line integral of
B
, you know
B
fields go around the current and the line integral of
B
around a loop will be the current crossing that shaded surface. That's how we get Ampere's law. But now you say, that's not the only surface with that loop as the boundary. I should be able to draw any surface with the loop as the boundary. So you say let me take that surface. You are still okay, because whatever current passes this phase also passes through that phase. The law is still good. So giddy with success, you say, why not this? That's my new surface. It goes all the way around one of the plates of the capacitor and comes back. Now I have a problem.
I have a problem because there is no current passing that surface. Nothing going on between the plates in terms of current. If I draw an even bigger one like this one, I am again okay, because now that same current is passing through this one. It's this surface in between that things don't work. You follow that? We have a crisis where if you say it's
μ0I
and you say it's on any surface with this loop as the boundary, it's the boundary of the surface, then this kind of surface, half in and half out, has a problem. So what will you do? You realize you have to modify your equations. It's quite often how people modify equations. Sometimes they do experiments, sometimes they do thought experiments. Einstein loved doing these experiments, which are called Gedanken experiments. You don't really do the experiment, but you say, "If I did this, what will happen?" There's a little paradox, and you have to modify your theory. So there are two reasons to modify the theory. One is experiments tell you is wrong; other is, theory tells you there's a problem.
So you have to add something to this. That something I add should not have any contribution from this surface, but on this surface, it should make exactly the same contribution as the physical current made on this surface, so that no matter which surface I take, I get the same answer. And I'm going to do that by the — there are many ways to do this. If you know more math, there are more ways to get this, but this is one that's good enough. I'm going to do the following? I'm going to rewrite this as follows. You see in the region between the plates, I have no current, I agree. I gave up. I do have something between the plates I don't have in the wire. You know what that is? Pardon me?
Student:
Electric field.
Professor Ramamurti Shankar:
You have an electric field. There's something non 0 in between the plates. So I'm going to write this
μ0I
somehow in terms of electric field between the plates and let's see how it goes. So I'm rewriting the very same term,
I
is
dQ/dt
.
Q
is the charge of the capacitor. And let me write it as
Q/ε0 d
by
dt
. Now let me write it as
μ0ε0A
d by dt of
Q/A
divided by
ε0
. That =
μ0ε0A
times
d
by
dt
of the electric field between the plates. Why is that? Because the electric field is
σ/ε0
and
σ
is just
Q/A
. Now bring that
A
in here and you get
μ0ε0 d
by
dt
of electric field times
A
. But that we can write as
μ0ε0
, the surface integral of the electric field over the surface, and that's what we call
μ0ε0
electric flux,
d
by
dt
. Therefore my modified law is going to be
B⋅dl
=
μ0I + μ0ε0 d
by
dt
of
Φ
electric
.
Chapter 4: Displacement Current [01:08:03]
That's the bottom line. You can fill in these blanks if you have trouble writing and listening. I'm just saying, go to the region between the plates. Once you start with
dQ/dt
, turn
Q
into the
σ
, the charge density on the plates. That's simply the electric field, then you'll find, this is simply the electric flux, rate of change times
μ0ε0
. This extra term is called the displacement current. I don't know why it's called that name, but you know that you have to put that extra term. But now look at this equation with that extra term. Notice it works everywhere. If you took a surface like the first one I took, that slices through the wire here, there's no electric field anywhere, inside a perfect conductor or anything, there's going to be no electric field. Then
μ0I
is going to contribute. If I go to the region between the plates, there is no
I
there, but there's the rate of change of electric flux. Therefore the last Maxwell equation, the Ampere's law, is going to be modified with an extra term,
μ0ε0 d
Φ
electric
/dt
. And it has a nice symmetry now, that the line integral of the electric field is the rate of change of magnetic flux. The line integral of the magnetic field contains a rate of change of electric flux. It's got other stuff, but it's got that extra term. So I'm going to come next time and start looking at these equations. And remarkably, these equations imply there are electromagnetic waves. Without the benefit of any charge, without the benefit of any current, there'll be electric and magnetic fields. That's the interesting part. We know electric fields can be produced by charges, and magnetic fields can be produced by currents, but I'm saying go light years from everything. No ρ, no charge density, no current density. There'll be non-zero
E
and
B
just moving on their own, and you want to understand how that happens.
First of all, it's amazing it's predicted by this stuff. So basically, this is a very important day in your life, because now you know, all of electromagnetism is that equation + that equation. This is it. There is no more stuff any of us knows, at least in classical theory. In quantum theory, there's new stuff. Classical electromagnetism is only that. So you don't have to pack your head with all kinds of results. You can derive everything from these. Okay, so let's do that on Wednesday.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/spring10/phys201/mp3/phys201_13_022210.mp3) |
