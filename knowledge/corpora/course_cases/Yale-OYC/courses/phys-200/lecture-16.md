- Source: https://oyc.yale.edu/physics/phys-200/lecture-16
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 16 - The Taylor Series and Other Mathematical Concepts

### Overview

The lecture covers a number of mathematical concepts. The Taylor series is introduced and its properties discussed, supplemented by various examples. Complex numbers are explained in some detail, especially in their polar form. The lecture ends with a discussion of simple harmonic motion.

### Lecture Chapters

1. Derive Taylor Series of a Function, f as[∑ (0,∞)fn xn/n!]
2. Examples of Functions with Invalid Taylor Series
3. Taylor Series for Popular Functions(cos x, ex, etc.)
4. Derive Trigonometric Functions from Exponential Functions
5. Properties of Complex Numbers
6. Polar Form of Complex Numbers
7. Simple Harmonic Motions
8. Law of Conservation of Energy and Harmonic Motion Due to Torque

1. 0
2. 861
3. 1050
4. 1411
5. 1901
6. 2560
7. 3004
8. 3787

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 16 - The Taylor Series and Other Mathematical Concepts
Chapter 1. Derive Taylor Series of a Function, f as [Σ (0, ∞)fnxn/n!] [00:00:00]
Professor Ramamurti Shankar:
Ok, so today, it's again a brand new topic, so if you like relativity you would be in grief and mourning. If it got to be really nasty, you'll be relieved that that's behind us now. And let me remind you one more time that the problem set for relativity was quite challenging because I had to make up most of the problems. And they're not from the book, so they're a little more difficult. The exam will be much more lenient compared to the homework. That's generally true, but particularly true in this case.
Okay. So, today I'm going to introduce you to some mathematical tricks. As you've probably noticed by now, a lot of physics has to do with mathematics, and if you're not good in one, you're not going to be good in the other. And I just thought I would spend some time introducing you to some tricks of the trade, and then we'll start using them. First important trick is to know what's called a Taylor series [laughter].Okay, I see this is greeted by boos and hissing sounds. I'm not sure what your past experience with Taylor series was, and why it leaves you so scarred and unhappy. My experience with Taylor series has been positively positive, and I don't think I can carry on any of my things without knowledge of Taylor series. But I'll tell it to you, Taylor series, as we guys in the Physics Department tend to use it.
The philosophy of the Taylor series is the following: That if some function
f(x
)--and I'm going to draw that function, something like this--but I'm going to imagine that you don't have access to the whole function. You cannot see the whole thing. You can only zero-in on a tiny region around here. And the question is, as you try to build a good approximation to the function, how will you set it up so that you can write an approximation for this whole function, valid near the point
x
= 0, where you know something. So, suppose I block out the whole function--you've got to imagine mentally. I don't show you anything except what's happening here. In other words, I show you only
f
(0). That's all you're told. The value of the function is 92. What should we do away from
x
= 0? Well, you've got no information about this function, you don't know if it's going up, if it's going down. All I tell you is one number, what it's doing now. It's clear the best approximation you can make is a flat line. There's no reason to tilt it one way or the other, given the information you have.
So, the first approximation of the function you will say is,
f(x)
equal to that [
f
(0)]. It's not equal to; you can put some symbol that means approximately equal to. It's like saying, "Temperature today is 92, now what's it going to be tomorrow?" Well, if you don't know anything else, you cannot tell what it's going to be tomorrow. But if you know that this is fall, that the temperature's always going down, and somebody tells you, "I know the rate of change of temperature. I know that as of today, the rate of change of temperature is something." Then you can use that information to make a prediction on what it will be tomorrow. That is to say, for values of
x
not equal to 0. And let's denote by this following symbol:
f
′ of 0 is the derivative, which is
df/dx
at
x
= 0. And you'll multiply it by
x
, and that's your best bet for what the function is, away from
x
= 0. What that does is to approximate the function by a straight line with the right intercept and the right slope. By "right" I mean, matches what you know about the exact function. And if it turns out the function really was a straight line, you are done. It's not even an approximation, it'll track the function all the way to eternity. But it can happen, of course, that the function decides to curve upwards, as I've shown in this example, and this will not work if you go too far. For a while, you'll be tangent to the function, but then it'll bend away from you. So, it's really good for a very small
x
and you can say, "Well, I want to do a little better when I go further out."
Well, what this doesn't tell you, this approximation, is that the rate of change itself has a rate of change. This assumes the rate of change is a fixed rate of change, which is the rate of change at the origin. And the rate of change of the rate of change is the second derivative. So, if somebody told you, "Look, here's one more piece of information." I know the second derivative of the function, which I'm going to write as
f
double′ at 0. Well, with that information, you can build a better approximation to the function, and you will put that in
x2
. But the key thing is you've got to divide by 2, but if you like 2 factorial. And the way you divide by the 2, because your goal is take this approximation and make sure that that's whatever you know about the function built into it. Right? Let's check this approximation and see if it satisfies those properties. First of all, at
x
= 0, let's compare the two sides. At
x
= 0, the left hand side is
f
(0). On the right hand side, when you put
x
= 0, you kill this and you kill this and it matches. So, you've certainly got the right value of the function. Then you say, "What if I take the derivative of the function at
x
= 0?" Let's take the derivative of this trial function, or the approximate function on both sides. When I take the derivative, that being a constant, does not contribute. This derivative of
x
is 1. In the next one, the derivative of
x2
is 2
x
, 2
x
cancels the 2, so I get
f
double′ of 0 times
x
. But now, evaluate the derivative at
x
= 0. That gets rid of this guy, and the derivative of my test function matches the derivative of the actual function, because this is the actual derivative of the actual function.
Now, it follows that if you want to say, "How about the second derivative of this function?" let's take the test function I have, or the approximation. Take a second derivative, and make sure that comes out right. I don't feel like writing this out, but try to do this in your head. Take two derivatives on the left-hand side and see what happens on the right hand side. Well, if you take one derivative, this guy's gone. If you take two derivatives, this guy's gone. And then, if you take the first derivative, you get 2
x
, you take the second derivative you get 2, the 2 cancels the 2. Now, if you put
x
= 0. If you do, you find that
f
(0) here matches the second derivative of the function on the left-hand side. So, this 2 factorial is there to make sure that the function you have cooked up has the right value of the function at the origin, has the right slope at the origin, has the right rate of change of the slope at the origin.
Well, it's very clear what we should do. If you had a whole bunch of derivatives, then the approximation we will write will look like,
f
n-th derivative. I cannot draw
n
′s there, so
n
means
n
such primes,
x
to the
n
over
n
factorial. And you go as far as you can. If you know 13 derivatives, put 13 derivatives here. That's an approximation. That's not called a Taylor series, that's the approximation to the function.
Now, it may happen that sometimes you hit the jackpot, and you know all the derivatives. Someone tells you all the derivatives of the function, then why stop? Add them all up. Then, you will get the sum going from the 0 derivative all the way up to infinity. And if you do the summation of every value of
x
, you will get a value, and if that summation is meaningful and gives you a finite number, that, in fact, is exactly the function you were given. That is the Taylor series. The Taylor series is a series of infinite number of terms which, if you sum up -- and sum up to something sensible -- will actually be as good as the left-hand side.
So, let me give you one example. Here's a famous example. 1 over 1 minus
x
is the real function. You and I know this function, we know how to put it in a calculator; we know how to plot it. You give me an
x
and I stick it in the denominator, subtract it from 1, invert it; that's the function. But instead, suppose this function was revealed to us in stages. We were told
f
(0)--what is
f
(0) here? Put the
x
equal to 0,
f
(0) is 1. Now, let's take the derivative of this function,
df/dx
.
df/dx
has a minus 1 because it's 1 minus
x
to the minus 1, times a square; then the derivative of what's inside this, that gives you a minus 1. This is simple calculus, how to take the derivative of this fellow here. Having taken the derivative, evaluate it at
x
= 0, this vanishes, that becomes 1, and you get 1.
If you now take the second derivative of this function, which I don't feel like doing, and I evaluate that at
x
= 0, then I'll find it is equal to 2 factorial. In fact, I'll find the
n
th derivative at the origin to be
n
factorial. Well, that's very nice. Because then, my approximation to the function begins as 1 plus
x
times the first derivative, which happens to be 1 plus
x2
over 2 factorial times the second derivative, which happens to be 2 factorial plus
x3
over 3 factorial times 3 factorial, so you can see where this guy is going. It looks like 1 + x + x2, et cetera. The Taylor series is its infinite sum. In practice, you may be happy to just keep a couple of terms.
So, let's get a feeling for what those couple of terms can do for us. So, let me take
x
= 0.1.
x
equal to point 1; the real answer is 1 over 1 minus point 1, which is 1 over point 9, which is 1.1111, etcetera. That's the target. What do you do with the series? The series starts at 1, times one-tenth, plus 1 over 100, plus 1 over 1000, and so on. And you can see, as I keep more and more terms, I keep just filling up these ones. If you stop at 1 over 1000, you stop right there. So, this is the exact answer, this is the approximation. But it's clear to you, perhaps in a simple example, that if you kept all the terms of the series, you really will get this infinite number of recurring 1's.
So, that is the function. That is the Taylor approximation. We'll just chop it off whenever you want, and it's a good approximation, and that's the Taylor series. The series means sum everything. Now, summing an infinite number of numbers is a delicate issue. I don't want to go there at all, I discuss that in this math book. But sometimes a sum makes no sense, then you've got to quit. For example, put
x
= 2. The correct function is 1 - 2, which is -1. Our approximation for
x
= 2 looks like 1 + 2 + 4 + 8. Fist of all, this sum is going to grow to infinity, because the numbers are getting bigger and bigger. This sum seems to be all positive; that is the correct answer is negative. Obviously, the series doesn't work.
So, the next lesson of our Taylor series is, you can write down the series, but it may not sum up to anything sensible beyond a certain range. So, if you're doing a Taylor series at
x
= 0, and you go to
x
= 2, it just doesn't work. So, you can ask, "How far can I go from the origin?" Well, in this simple example, we know that
x
= 1, the function just going to infinity, that's why you couldn't go there. And you cannot go to the right-hand side of that point. The function is well defined on the other side, but this series, this knowledge of the function here, is not enough to get you on the other side. So, this is a case where there are obvious problems at
x
= 1. But if I wrote a function like 1 over 1 plus x2, that's a nice function, got no troubles anywhere. And yet, if you took the Taylor series for it, you will find if you go beyond absolute value at
x
= 1, the series makes no sense.
So, I don't want to do that mathematical theory of series. I just want to tell you that functions can be approximated by series. And if you're lucky, you can do the whole sum if you know all the derivatives, and the whole sum may converge to give a finite answer. In which case, it's as good as the function. One guy can use 1over 1 minus
x
; the other one can use the infinite series, and they're morally and mathematically in every sense equal, as long as they don't stray outside the region of validity of the infinite series.
Chapter 2. Examples of Functions with Invalid Taylor Series [00:14:21]
Ok, so the most popular example that I've been using in the class, remember, is 1 +
xn
. That's a function we can do with Taylor series.
f
(0) is 1. What's the derivative of the function? It's
n
times 1 plus
xn
minus 1. The
x
is
n
times 1 plus
xn
minus 1; if I evaluate it at
x
= 0, it is just
n
. That's why we get this famous result we've been using all the time. If
x
is small enough you stop there, because the next time it's going to involve an
x2
and an
x3
, then if
x
is tiny, we have no respect for
x2
and
x3
, we just cut it off. But if you want the next term--one of you guys even asked me, "What happens next?" we'll take the second derivative. You can see it's n times n minus 1, times 1 plus xn minus 2. If you put
x
= 0, you'll get
n
times
n
minus 1,
x2
, and don't forget the 2 factorial. So, what I've been doing is I've been saying 1 plus
xn
, approximately equal to this. But even if you keep that, it's still approximate. But it's a good approximation; how many terms you want to keep depends on how tiny
x
is.
Ok, so it's good to know there's an infinite series, but it's also good to know you can chop it off and do business with a few terms. In fact, all of relativity we reduce as follows. The energy of a particle is this, which we can write as
mc2
times 1 minus
v2
over
c2
to the minus ½. If you expand this in a power series, you're going to get
mc2
+ ½
mv2
, plus stuff involving
v
to the 4th over
c
to the 4th times
c2
. We dropped all this, and for 300 years we did mechanics keeping just this term. We just kept that first non-trivial term, and all of our collisions and so on that we did, used only that up to that point. So, the approximations have really been useful, and they describe nature approximately.
If you say, "Well, I want to be exact," you can go back and use this. Unfortunately, generally somebody tells you, "That's not exactly. There in quantum mechanics, tells you the whole thing is wrong." At every stage, you will have to give up something. So, I have a lot of respect for approximations. If you could not describe the world approximately, you couldn't have come where you've come. Because no one knows the exact answer to a single question you can pose. Ask me a question, and the answer is, "I don't know." Second part of the answer is, "Nobody knows." Because if your question says give an answer to arbitrary precision, any question asked, we just don't know. Newtonian mechanics works for small velocities. All of relativistic mechanics works for any velocity, but not for really tiny objects. Then you've got to use quantum mechanics. So, always theories give way to new theories, and so approximations are very important. So, you have to learn this.
Chapter 3. Taylor Series for Popular Functions ( cos x, ex, etc. ) [00:17:30]
Okay. So now, I'm going to consider the following function:
ex
. Now ,this guy is something you all know and love, because it's one nice thing about the function, is every derivative is
ex
. Right? Every child knows
ex
has got
ex
as its derivative. Why do we like that here? That means all the derivatives are sitting in front of you. They're
ex
, and at
x
= 0,
e
to the 0 is 1, so every derivative is 1. And the function is very easy to write down. It is really 1 +
x
+
x2
over 2 factorial, plus
x
to the 3 over 3 factorial,
x
to the 4 over 4 factorial. You can go on like this, and if you like to use a compact notation, it's
xn
over
n
factorial, and going from 0 to infinity, that 0 factorial is defined to be 1. That's
ex
.
If you ever forget the value of
e
, and I need to know the value of
e
, because when I lock my suitcase and check it into the airport, I use either
e
or
π
, because they're the only two numbers I can remember--So, if I forget the value of
e
, I just say
e
is the same as
e
to the 1, so I've got 1 + 1 + 1 + 2 + 1 over 6, and pretty soon I'm telling the guy scanning my luggage, "That's my code." And it's much better than any other code because I cannot reconstruct, say, my grandfather's name. I may not get it right. I may not construct my house address, or my phone address. This doesn't change. I've been moving around all over the world, this is a very reliable number. Now,
π
is a good number, but rules for computing
π
are somewhat more difficult.
π
also can be computed as an infinite series, but this guy is very easy. There's 2 point in 7-7 something, that is
e
.
Okay. Now, here is the very nice property of this series. It is good for any
x
. You remember the series for 1 over 1 minus
x
crashed and burned at
x
= 1. This series -- always good. You put
x
= 37 million, you've got 37 million, 37 million cubed, 37 million at the 4th power; don't worry. These factorials downstairs will tame it down and make it converge, and will give you
e
to the whatever number I give. That's something I'm not proving, but the series for
ex
, no limits on validity. All right.
Then, we take the function,
cos x
. Now,
cos x
, we all know and love as this guy. That's got a period of 2
π
. But we can write a series for it because it's a function. And what do I need to know to write the series for it? I need to know the value of the function at the origin. So, we know cosine of 0 is 1. If you take the derivative you get minus sine, and its value at 0 is 0. You take one more derivative, you get minus cosine 0, which is minus 1, and I think by now you get the point. Every other derivative will vanish, and the remaining derivatives will alternate in sine from 1 to minus 1. That means, if you crank it out, you will get 1, you won't have anything linear in
x
because the coefficient of that is
sin
0 which vanishes; then you'll get
x2
over 2 factorial plus
x
to the 4 over 4 factorial, and so on. This is
cos x
.
If you cut it off after some number of terms, it's not going to work. In the beginning, 1 minus
x2
looks very good. This is 1 minus
x2
over 2, looks like this. But eventually, this approximation will go bad on you, because
x
to the 4th is just
x
to the 4th. It'll grow without limit. No one's telling you this approximation has a property that cosine is less than 1. It doesn't satisfy that, because you're not supposed to use it that far out. But if you keep all the terms, then in fact, even though
x
to the 4th is taking off,
x
to the minus 6 is saying hey, come down,
x
to the 8th is saying, go up. You add them all together, remarkably, you will reproduce this function. Very hard to imagine that the cosine that we know as oscillatory is really this function. And I hope all of you know enough to know how to find the series. You should know the derivative of cosine is minus sine, the derivative of sine is cosine. And evaluate them at the origin; I say you can build up the series. Then, if you do similar tricks for
sin x
, sin of 0 is 0, derivative of sin is cosine, and of course,
n
of 0 is 1. So, the first derivative is 1; that gives you this term. Next one won't give you anything, the one after that will give you this, and this guy will go on like this one. Okay. So, these are series for
ex
,
cos x
, and
sin x
, good for all
x
. So, there's no restriction on this.
One of the really interesting things to do when you are bored, or stranded somewhere in an airport, is to take cosine squared plus sine squared. Squared the whole thing, add the squared of the whole thing and add them up. You'll find, by miracle, you will get the one from squaring the one and every other power of
x
will keep on vanishing. Of course, you'll have to collect powers of
x
by expanding the bracket. But it will all cancel. That's what I meant by saying this series is as good as this function. It will obey all the identities known.
Chapter 4. Derive Trigonometric Functions from Exponential Functions [00:23:31]
Okay. Now, for the punch line. I think everyone--Some of you may know what the punch line is, the punch line is the following. Let us introduce, without any preamble right now, the number
i
, which is the squared root of minus 1. All I expect of
i
is that when I squared it, I get minus 1. If I cube it,
i3
is
i2
times
i
, so that's minus
i
, and
i
to the 4th is back to plus 1 because
i
to the 4th is
i2
times
i2
, and
i2
is minus 1. So, if you take powers of
i
, it'll keep jumping between these values. It'll be
i
, it'll become minus 1, it'll become minus
i
, then it'll become plus 1. That's the set of possible values for powers of
i
. It'll be one of these four values.
Well. Then we are told, if you now consider the following rather strange object,
eix
. Now,
eix
, you have to agree, is really bizarre.
e
is some number, you want to raise it to 2, that's fine. Number times number.
i
is a strange number, right? It's the squared root of minus 1, and you wanted me to raise
e
to a complex power. What does that even mean? Multiply
e
by itself
ix
times? Well, that definition of powers is no good. But the series for
ex
defines it for all
x
, then we boldly define
ex
for even complex values of
x
as simply this thing too, with
ix
plugged in place of
x
. And by that fashion, we define exponential. So, the exponential function is simply defined as, suppose you write
e
raised to
dog
.
e
raised to
dog
is 1 plus
dog
plus
dog2
over 2.
e
raised to anything is a code for this series. And now we raise
e
to various things. Real numbers, complex numbers, matrices, whatever you want. Your pet, you can put that up. Of course, you've got to be a little careful. You cannot raise
e
raised to
dog
, because the units don't match. But there's a
dog
here and
dog2
, so you should divide it by some standard
dog
, like President's dog [laughter]. Take some standard. Napoleon's dog, divide it, then you've got something dimensionless [laughter]. Then it will work. So, as long as it's some dimensionless object, this is what we mean by
e
raised to that. That's a fantastic leap of imagination. How to raise
e
to whatever power you like; take the series.
Let's do the series. So, I'm going to get 1 plus
ix
, plus
(ix)2
over 2 factorial, plus
(ix)3
over 3 factorial, and I'm going to stop after this last term,
(ix)4
over 4 factorial. Keep going, then what do you get? Let's take the 1 from here, leave this alone for a minute. You write
i
times
x
, go here,
i2
is minus 1, so I get minus
x2
over 2 factorial, then I come here. I cubed is minus
i
, so I write here, minus
x3
over 3 factorial. Then, I go back here and write
x
to the 4th over 4 factorial. By now, everybody knows what's going on. Everybody knows that this is just
cos x + i sin x
. Okay, this is a super duper formula. Life cannot go on without this. You want to draw a box around this one, draw it. Because without this formula, we cannot do so many things we do.
It says that the trigonometric functions and the exponential functions are actually very intimately connected. And if they're all defined by the power series, you're able to prove it. So, this is the formula proven by Euler. And it's considered a very beautiful formula, and here is the particularly beautiful special case of this formula. If you put
x = π
, I get the result
eiπ
equal the
cos π
, which is minus 1, plus
i sin π
, which is 0. I get the result
eiπ
+ 1 = 0. Now, everybody agrees this has got to be one of the most beautiful formulas you can imagine involving numbers or in mathematics. Why is it such a great formula? Look at this formula here.
π
, defined from the Egyptian times, is a ratio of circle to diameter.
i
is square root to minus 1. 1 is the basis for all integers.
e
is the basis for the logarithm. Here is a formula in which all the key numbers appear in one single compact formula. The fact that these numbers would have a relationship at all is staggering, and this is the nature of the relationship. This is voted the formula most likely to be remembered, this formula. Now, we are going to use not only the special case, but we are going to use this all the time.
So, how many people have seen this? Okay. If you have not seen this, then you've got more work than people who have seen this. You've got to go and you've got to do all the intermediate steps so you get used to this thing. Now, let's do the following two other variations, and then I'll move on. If I change
x
to minus
x
, then I get
e-ix
. Cosine of minus
x
is cosine
x
, and sin of minus
x
is minus
sin x
. So, I can get that relation. Then, I'm going to combine those two to do the following: I'm going to say that
cos x
=
eix
+
e-ix
over 2, you can check that. And
sin x
=
eix
e-ix
over 2
i
. You just add and subtract these two formulas and you get that.
Okay. So, what does this mean? It means that trigonometric functions, you don't need them. If you've got exponential functions, you can manufacture trigonometric functions out of them, provided you're not afraid to go to exponents with complex number
i
in them. And all the identities about sines and cosines will follow from this. For example, if you take cosine squared plus sine squared, you're supposed to get 1. Well, you can square the right hand side, you can square the left hand side, and you will get 1. To get the 1, you better remember the following:
eix
times
e-ix
is what? You know how you come by an exponent? You raise it to one power times the same thing raised to another power, is e raised to ix minus x, which is e raised to 0, which is 1.
So, when you raise the number to a power, you multiply it by the number times a different power, the product is a number to the sum of the two powers. Powers combine. 2 cubed times 2 to the 4th is 2 to the 6th. That's true for 2; it's true for e; it's true for everything. Exponents add when you multiply them, that's why
eix
and
e-ix
combine to give you 1. Once you know that, you can prove this. Okay.
Chapter 5. Properties of Complex Numbers [00:31:41]
Now, I'm going to do a little more of complex numbers, so maybe I'll leave this alone for now. I introduced you the number
i
by saying it's the square root of minus 1, and complex numbers entered our life, even though we didn't go looking for them. You can write down equations with real numbers with no intention of invoking anything fancy, like this, and you find there is no solution to this equation. Even though everything there is completely real. So, you can say, "Well,
x2
is minus 1," and you can manufacture a number
i
, with a property
i2
is minus 1; then, of course, you can have
x
equal to plus and minus
i
as your answer. So, complex numbers arose by trying to solve quadratic equations.
So, let me write you a slightly more interesting quadratic equation,
x2 + x
+ 1 = 0. So, there's no funny business, all real numbers. We want to solve this equation, so we go back to our good old sandbox days when we knew what the answer for this was--minus 3 over 2. And we already have a problem because we don't know what to do with square root of minus 3. So, we will write it as square root of minus 1 times square root of 3. Square root of minus 1 we will call
i
, and we will say this equation has two roots.
x
plus/minus (there are ) two roots, which are minus 1 plus or minus square root of 3
i
over 2. So, one root is 1 minus 1, plus root 3
i
over 2. And the other root is minus 1 minus root 3
i
over 2. These are solutions formerly to this equation in the following sense. Take this
x
that I'm giving you; put that into that equation, square the
x
and add the
x
to it, and add the 1, it'll in fact satisfy the equation. All you will have to know when you manipulate it is that
i2
is minus 1. Using the one property, you can now solve the quadratic equation. So, people realize if you enlarge numbers to include complex numbers, then you can solve any polynomial equation with that many number of roots. If it's quadratic, it'll have two roots, if it's cubic, it'll have three roots. They may not all be real; they may involve the complex number
i
.
Now, a very important point to notice is that this whole thing, minus 1 plus root 3
i
over 2, the whole thing is a single complex number. Don't think of it as the sum of two numbers; it's a single complex number. For example, if this had been plus instead of minus, you'd get something like 1 plus or minus root 3 over 2. Take the positive root, you don't think of it as two numbers. This is a single number. And that continues to be true even if it's a complex number. So, you should think of the whole combination as a single entity which you can add to others as entities and square, and so on.
Okay. So, that's what we are going to do now. We're going to generalize this particular case and introduce now a complex number
z
. And we're going to write every complex number
z
as a part that has no
i
in it, and a part that has an
i
in it. The example I had here,
x
is equal to--in this example,
x
was minus 1 over 2 and
y
was plus or minus root 3 over 2. And we're going to visualize that complex number as a point in the
xy
plane. We just measure
x
horizontally and
y
vertically, put a dot there, that's your complex number,
z
. Then, we say the new complex number called z star [*] and it's defined to be
x - iy
, is called the complex conjugate; complex conjugate of
z
. It's obtained by changing the sign of
i
. So, if you like, if
z
is sitting here,
z
star is sitting there, reflected around the
x
axis.
So, how does one work with complex numbers? You add them, you subtract them, and you multiply them, and you divide them. If you know how to do that, you can do with complex numbers everything you did with real numbers. So if
z1
is a complex number that is equal to
x1 + iy1
, and
z2
is a complex number that is
x2
+
iy2
, we will define
z1
+
z2
to be
x1
+
x2
times
i
times
y1
plus
y2
. If you draw pictures, then if
z1
is that number and
z2
is that number [pointing to the board], then
z1
+
z2
it really is like adding vectors. This number is
z1 + z2
. It's exactly like adding vectors. But you don't think of this plus that as two disjoined numbers, but as forming a single entity.
In a complex number
z
,
x
is called a real part of
z
, and is denoted by symbol "real
z
." If you want to get
z
, if you want to get the real part of a complex number
z
, you add to its complex conjugate and divide by 2. Because you are adding
x + iy
to
x - iy
, you get 2
x
and you divide by 2, you get that. If you want to get the
y
, which is called the imaginary part of
z
, you take z - z star and divide by 2
i
. It's like saying find the
x
component of a vector. It's whatever multiplies
i
.
y
component of a vector is whatever multiplies
j
. Similarly, a complex number can be broken down into the part which is real and the part that multiplies the
i
. To extract the real part, add to it the conjugate divided by 2, to extract the imaginary part, subtract the conjugate and divide by 2
i
. Again, if you have seen this, you don't need this. If you haven't seen it, it may look a little fast. But that's why I posted all the notes on the website, chapter 5 from this math book, which has got all this stuff. So, you can go home and you can read it.
Ok, the next question is what is
z1
times
z2
? Well, that's very easy to calculate.
x1 + iy1
times
x2
+
iy2
. Just open all the brackets and remember
i2
is minus 1. That's all you've got to do. So, that gives me
x1x2
; then, let me multiply the
iy1
times the
iy2
. And that gives me minus
y1y2
, because
i2
is minus 1 plus
i
times
x1y2
+
x2y1
. This is how you multiply two complex numbers.
That's something very nice that happens when you multiply a number
z
by its complex conjugate. What happens when you multiply
z
by its conjugate, you are saying, take
x + iy
, multiply it by
x
minus
iy
;
a + b
times
a - b = a2 - b2
. But remember,
b
is
iy
. So, when you take the square of that, you should keep track of all the signs and you will find it's
x2 + y2
. We denote that as this, and this thing is called the modulus of
z
[\|z\|]. It's the length of the complex number
z
, just given by Pythagoras' theorem.
You should know, whenever you take a complex number, multiply by each conjugate, by its complex conjugate, the result will be a real number equal to the square of the length of the complex number. Because I'm going to use that now to do the last of the manipulations, which is, what is
z1
divided by
z2
? How do you divide these crazy numbers? So, on the top I write
x1 + iy1
, the bottom, I write
x2 + iy2
. If I only had
x2
, I know how to divide. It's just a number. Divide that by
x2
and that by
x2
. But I've got the sum of these two numbers in the bottom, and you can ask, "How do you do the division?" So, the trick, always, when you run into this problem, is to multiply the top and bottom by the complex conjugate of the bottom. Multiply it by
x2 - iy2
, top and bottom. Then, something nice happens to the denominator, because the denominator then becomes
x22 + y22
, which is an ordinary real number, nothing complex about that. The numerator, you can open out the brackets. I don't know if I want to do that; it's just going to be
x1x2 + y1y2 + i
times
y1x2
y2x1
. Now, don't worry about all the details. All it means is, if you know how to multiply two complex numbers, you can also divide by a complex number. That's the key point. Why? Because if you've got a complex number denominator, you don't like it, multiply top and bottom by the complex conjugate of this guy, the denominator turns into a purely real number. So, this whole thing could be 36, for example. Well, we know how to divide the numerator by 36, right?
x1x2 + y1y2
some number, maybe 9; then you divide by 36. One-fourth. This could be
i
times 18. It would be 36, you get
i
over 2. So, this number could have been one fourth plus
i
over 2. So, dividing by a complex number is not a problem.
Chapter 6. Polar Form of Complex Numbers [00:42:40]
Now, why did I do all that stuff today about eix? You're going to see that now. The rationale for going through that math is the following. Let's take this complex number that goes from here to here, that is
x + iy
. And let's introduce, just like we would for an ordinary vector, this angle
θ
and that length
r
. Whenever you have a vector, you can talk about the Cartesian components
x
and
y
, or you can talk about the length of the vector and the angle it makes. Then, it's clear that
x = r cos θ
, and
y = r sin θ
, where
θ
is now an angle associated with a complex number which tells you at what angle it's located, and
r
is the length of the complex number. It's called the polar form of the complex number. Then, you can see that
z
, which is
x + iy
, is equal to
r
times
cos θ + i sin θ
which you can now write as
r
times ei
θ
.
That's why we did all that work, to tell you that a complex number can be written in this form. You can either write this
x + iy
, or else
reiθ
. They both talk about the same number. One talks about how much real part and how much imaginary part it has, other way of writing it talks about how long the vector is, and at what angle it is located. It contains the same information. So, that
r
is equal to-- the inverse of this formula is that
r
is square root of
x
squared plus
y
squared, and
θ
is
tan
inverse
y
over
x
. In other words,
tan θ
is
y
over
x
. This is
y
, and this is
x
.
Now, the advantage of writing a complex number in polar form is the following. Suppose I give you two complex numbers, z1 is r1
e
i
θ
1, and
z2
is
r2
e
i
θ
2. The product
z1z2
is very easy to calculate in this form because
r1r2
multiply to give you this, and the exponentials combine. It's a lot easier to multiply them in this form than when I multiplied them somewhere here. See, if I write it in this Cartesian form, it's a big mess. In polar form, it's very easy. So, the rule is, if you want to multiply two numbers, multiply the lengths to get the length of the new number and add the angles to get the angle of the product. So, what I'm telling you is that if
z1
looks like this guy with some angle
θ
1, and
z2
is that guy with an angle
θ
2, the number
z1z2
has a length equal to the product of these two lengths, and that angle equal the sum of these two angles, so it will look like that [writing graph on board]. To go from this to that, you multiply the lengths and you add the angles.
So, the polar form is very well suited for multiplying, and it's even better suited for dividing. If I say, "Give me
z1
over
z2
," well, you can all do that in your head. It's
r1
,
e
i
θ
1, divided by
r2
,
e
i
θ
2. The modulus of the new number is just
r1
over
r2
. And how about this?
e
i
θ
1 divided by
e
i
θ
2. Dividing by
e
i
θ
is the same as multiplying by
e
-i
θ
. So, this is really
e
i
θ
1 -
θ
2. So, I'm assuming you guys can figure this part out, 1 over
e
i
θ
is the same as
e
-i
θ
. Well, if you doubt me, multiply--cross multiply, and all I'm telling you is that 1 =
e
i
θ
times
e
-i
θ
, which you know is true when you combine the angles. When you've got
e
i
θ
downstairs, you can take it upstairs with the reverse angle. And that's a useful trick; I hope you will remember that useful trick.
So, there is one part of this thing that I want you to carry in your head, because it's very, very important. When you take a complex number, it's got a length and it's got a direction. Then, you multiply by a second complex number, you're able to do two things at the same time. You're able to rescale it, and you're able to rotate it. You rescale by the length of the second factor, and you rotate by the angle carried by the second factor. The fact that two operations are done in one shot is the reason complex numbers play an incredibly important role in physics, and certainly in engineering and mathematical physics.
I'm going to now change gears, but I want to stop a little bit and answer any questions any of you have. So, how many people have seen all of this before? So, if you saw something, you saw the whole thing. But look, that's not such a big number, so I am cognizant of the fact that not many of you have seen it. But you will have to go and learn this today. I'm going to post the problem set for this sometime in the day so you can start practicing. Don't wait, the problem set has nothing to do with next Wednesday, it has a lot to do with today. When I assign a problem today, I imagine you're going breathlessly to your room, not able to wait, jumping into the problem set and working it out. That's the only way you're going to find out what these things mean if you've never seen them. If you've seen them before in high school, or taken a math course and you've got lots of practice, then I'm not talking to you. But I'm going to use this at some point, so you should understand complex numbers. And I'm telling you, there are very few branches of any science where complex numbers will not be used. Now, you may not believe this now, but that is true. If an electrical engineer, it's an absolute must. If you solve any kind of differential equation which can occur in biology and chemistry, that's a must. So, it's very, very important.
All right. So now, I'm going back to physics. Going back from mathematics to physics, and the physics of this topic for today has to do with something very different from the past, so forget all the relativity now. You're going back to Newtonian days. Kinetic energy is ½
mv2
. It's a little difficult to go back and forget what you learned. On the other hand, for some of you, it may not be so hard if you didn't learn anything. Well then, you are that much ahead of the other guys. But remember now, the truth is the relativistic theory. We're going to go back to Newtonian days, and the reason we do it that way is to give you something interesting, hopefully, compared to what you normally do.
Chapter 7. Simple Harmonic Motions [00:50:04]
So, what we're going to study now is what's called small oscillations, or simple harmonic motion. It's a ubiquitous fact, that if you took any mechanical system which is in a state of equilibrium, and you give it a little kick, it vibrates. Now, if you've got a pillar, ceiling to floor, you hit it with a hammer, it vibrates. If you take a gong and hit it, it also vibrates. If you've got a rod hanging form the ceiling through a pivot -- it's hanging there -- if you pull it, it goes back and forth. The standard example everyone likes to use is if you've got a particle in a bowl, it's very happy sitting in the bottom. If you push it up a little bit, it'll go back and forth.
And the example that we're going to consider is the following. If you have a mass,
m
, connected to a spring, and the spring is not stretched or contracted, it's very happy to be there. That's what I mean by equilibrium. Equilibrium means the body has all the forces on it adding up to 0; it has no desire to move. The question is, if you give it a little kick, what'll happen? Well, there are two situations you can have. You can have a situation where the particle's on top of a hill. That's called unstable equilibrium because if you give that a kick, it's going to come down and never return to you. That's equilibrium, but unstable equilibrium. I'm talking about stable equilibrium. That's because there are restoring forces. If you stray away from the equilibrium, there are forces bringing you back. And in the case of the mass and spring system, the force,
md
2..
ma
, is equal to -
kx
. And what this equation tells you is if you stray to the right,
x
is positive, [I will apply a force to the left.] Remember, this is
ma
, and this is
F
.
F
is such that it always sends you back to your normal position.
So, we want to understand the behavior of such a problem. We want to solve this problem. How do you solve this problem? Well, I did it for you along back, when I gave you a typical paradigm for how you apply Newton's laws; I gave you this example. So, I'm going to go through it somewhat fast. Our job is to find the function
x
that satisfies this equation. And we would like to write it as follows:
d2x
over
dt2
is equal to minus
ω2 x
, where
ω
is the shorthand for squared root of
k
over
m
. By the way, I'm using big
X
and small
x
like crazy, so it's just small
x
. I don't mean anything significant between this and this. They're all the same. If you want, you can take this--pardon me? [inaudible question] This is
k
, and this guy is
k
. And the other equations you use to follow the lecture today is, [
x=X
] these are all the same. Okay? So, don't say what happened there, when you move from one to the other.
Alright, so what did I say we should do? You can make it a word problem and say, "I'm looking for a function which, when I take two derivatives, looks like minus itself, except for this number." And we just saw that today. Trigonometric functions have the property that you take two derivatives, they return to minus themselves. So, you can take a guess that
x
looks like
cos t
but it won't work, that I showed you before. So, I'm not going to go through that again. If you took this guess--but
x
is not a number,
x
is a function of time [
x(t)
]. If you took this function of time, it, in fact, will obey this equation, provided the
ω
that you put in is the
ω
that's in the equation. Why? Because, take two derivatives. First time you get -
ω
,
sin
ω
. The second time you get -
ω
2 cos
ωt
, which means it's minus
ω
2
, times your
x
itself, and it is whatever you like. Then I said, "Let's plot this guy." When you plot this guy it looks like this. And
A
is the amplitude. What is
ω
? Well,
ω
is related to the time of the frequency of oscillations as follows: If I start with
t
= 0 over the
x
=
A
, how long do I have to wait 'till I come back to
A
? I think everybody should know that I have to wait at time capital
T
so that
ω
times
T
is 2
π
. Because that's when the cosine returns to 1. That means the time that you have to wait is 2
π
over
ω
. Or you can say
ω
is 2
π
over
T
, or you can also write it a 2
π
times frequency, where frequency is what you and I would call frequency, how many oscillations it does per second. That's the inverse of the time period.
So, if you pull a mass and you let it go, it oscillates with a frequency which is connected to the force constant and the mass. If the spring is very stiff and
k
is very large, frequency is very high. If the mass is very big and the motion is very sluggish,
f
is diminished. So, all that stuff comes out of the equation. One really remarkable part of the equation is that you can pick any
A
you like. Think about what that means. What is the meaning of
A
?
A
is the amount by which you pulled it when you let it go. You are told whether you pull the spring by one inch or by ten inches, the time it takes to finish a full back and forth motion is independent of
A
. This frequency here is independent of
A
. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
This
t
here? Here?
Student
: [inaudible]
Professor Ramamurti Shankar:
Ah, very good. That's correct. So, let's be careful. This is the
t
axis [pointing at graph on board]; this is a particular time, capital
T
.
So, the remarkable property of simple harmonic motion is that the amplitude does not determine the time period. If you pull it by two inches, compared to one inch, it's got a long way to go. But because you pulled it by two inches, the spring is going to be that much more tense, and it's going to exert a bigger force so that it'll go faster for most of the time, that's very clear. But the fact that it goes faster in exactly the right way to complete the trip at the same time, is rather a miraculous property of the fact that this equation has this particular form. If you tamper with this, if you add to this a little bit, like 1 over 100 times
x3
, then all these bets are off. It's got to be that equation for that result to be true.
Okay. So, this is simple harmonic motion. Then, you can do the following variant of this solution, which I will write down now. Suppose I set my clock to 0, right there. You set your clock to 0 here, but I can say, "You know what? I just got up and I'm looking at the mass, I set my clock to 0." When it hits 0, it's not at the maximum. But it's the same physics, it's the same equation. And that really comes from the fact that we had one more latitude here of adding a certain number
φ
, which is called a "phase," to the oscillator. Whatever you pick for
φ
, it'll still work. And whatever you pick for capital
A
, it'll still work. So, whenever you have an oscillator, namely, a mass and spring system, and you want to know what
x
is going to be at all times, you need to somehow determine the amplitude and the phase. Once you know that, you can calculate
x
at all future times.
So, let me give you an example. Suppose an oscillator has
x
= 5 and velocity equal to 0, at t equal to 0. So what does that mean? I pulled it by 5 and I let it go. I tell you the spring constant
k
and I tell you the mass, and I say, "What's the future
x
?" You've got to come back to this equation. And you've got to say, 5 =
A
cosine of 0 +
φ
. And how about the velocity? Velocity is supposed to be 0; that is minus
ωA
sin ωt
+
φ
. But
t
is 0. So, that tells me 0 is minus
ω
a sin φ
.
ω
is not 0,
A
is not 0. Therefore sin
φ
is 0, that means
φ
is 0 if you get rid of that, so the subsequent motion is
x
= 5
cos ωt
. This is a problem where we did not need
φ
. But it could have been that when you joined the experiment, you were somewhere here; then, the mass is actually moving. Then I will say at
t
= 0, velocity was some other number. Maybe 6. Then, you've got to go back and write two equations. One for
x
: take the derivative which looks like this, and instead of putting 0, you put 6. You've got two unknowns,
A
and
φ
. You've got to juggle them around, and you've got to solve for
A
and
φ
, given these two numbers. It's a simple exercise to solve for them, and when you do, you have completely fit the problem.
In other words, simply to be told a mass is connected to a spring of known mass and force constant is not enough to determine the future of the spring. You have to be told--For example, if nobody pulled the mass, it's just going to sit there forever. If you pulled it by 10, it's going to go back and forth from 10 to minus 10. So, you have to be told further information to nail down these two numbers. They're called free parameters in the solution. On the other hand, no matter how much you pulled it and how you released it, this
ω
, and therefore the frequency, are not variable. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
If you start it at rest, indeed, it will be 0, because the velocity at
t
= 0 is minus
ωA sin φ
. If you want to kill that, the only way is
φ
= 0. You could put
φ = π
if you like, but if you put 0, that'll do.
Okay. So, this is the elementary parts of this thing. And I already told you the following things. If
x(t)
is equal to
A
cos ωt
--let's put
φ
= 0. In other words, we'll agree that since there's only one oscillator, it is perverse to set your clock to 0 at any time other than when the oscillator is at one extreme point. If there are two oscillators oscillating out of step, it's impossible to make
φ
= 0 for both of them. Because if you can sync your clock when one of them is at a maximum, that may not be when the other one's at a maximum. But with one oscillator, to choose
φ
other than 0 is perverse. It's like saying, "I'm doing a projectile problem. I'll pick the place where I launch the projectile to be x = y = 0." You can pick some other crazy origin, but it doesn't help. So, we'll assume
φ
is 0 in this problem. If that is
x
, what is velocity at time
t
? Take the derivative of this, you get minus
ω A
sin ωt
. That means the velocity is also oscillating sinusiodally but the amplitude for oscillation is
ω
times
A
. So, if
A
is the range of variation for
x
,
ω
times
A
is the range of variation for velocity. Velocity will go all the way from plus
ω A
to minus
ω A
. The acceleration, which is one more derivative, is minus
ω
2
A
,
cos ωt
. Which is really minus
ω
2 times
x
itself. So, the amplitude for oscillation for the acceleration is ω2 times
A
. So, I think you should understand if
ω
is very large; then, the velocity will have very big excursions and the acceleration will have even bigger excursions, because the range of, this
A
really means if you plot
x
, it's going to look like this, going from
A
to minus
A
. This says if you plot the velocity, it's going to look like this. The range will go from
ω A
to minus
ω A
. If you plot the acceleration, it'll go from
ω
2
A
to minus
ω
2
A
.
Chapter 8. Law of Conservation of Energy and Harmonic Motion Due to Torque [01:03:07]
Last thing you want to verify is the Law of Conservation of Energy. I think I mentioned this to you when I studied energy, but let me repeat one more time. If you take, in this problem, ½
mv2
+½
kx2
--I did that for you--You can also verify this. Okay? ½
kx2
is going to involve
A
2 cosine squared
ωt
. ½
mv2
is going to involve something, something, something
sin2 ωt
. And by magic,
sin2
and
cos2
will have the same coefficient, so you can use the identity to set them equal to 1, and get an answer that does not depend on time. That's the beauty. Even though position and velocity are constantly changing, this combination, if you crank it out, will not depend on time. And what can it possibly be? If it doesn't depend on time, I can calculate it whenever I like. So, let me go to the instant when the mass has reached one extremity and is about to swing back. At that instant it has no velocity; it only has an
x
, which is equal to amplitude, or motion. So, that's the energy of an oscillator, ½
kA2
. When
v
= 0,
x
will be plus or minus
A
, but any other intermediate point you can find the velocity, if you give me the
x
. We did that too.
So, this is all I want to say about the linear oscillator. But let me mention to you another kind of oscillation, which is very interesting. Suppose you suspend a rod from the ceiling like this. It's hanging there. If you give it a twist, then it'll go twisting back and forth, like that. That's also a simple harmonic motion, except what's varying with time is not the linear coordinate, but the angle
θ
by which the rod has been twisted. What's the equation in this case? The equation here is
I
,
d
2
θ
over
dt2
. You guys remember now, that's the analog of
ma
? That's going to be equal to the torque.
Now, what'll happen in the problems we consider is that
θ
is a small number, and the torque will be such that it brings you back to
θ
= 0. So, this number will be approximately equal to minus some number
κ
times
θ
. That's the analog of minus
kx
. Little
k
was the restoring force divided by the displacement, which produced the restoring force. Little
κ
is the restoring torque divided by the angle at which you twisted it to get that torque. So, this isn't always true. For small oscillations,
sin τ
vanishes at
θ
= 0; it will look like some number times
θ
. If you like, it's the Taylor series for
τ
for small angles. If you knew this
κ
you are done, because mathematically, this equation is the same as
md
2
x
over
dt2
is minus
kx
. Because the
ω
for this guy will be square root of
κ
over
I
. You can steal the whole answer, because mathematically, mathematicians don't care if you're talking about
θ
or if you're talking about
x
. Now, if you compare this equation to this equation,
md
2
x
over
dt2
equal to minus
kx
, if the
ω
there was the root of
k
over
m
, the
ω
here would be root of
κ
over
I
.
So, you may be thinking, "Give me an example where
τ
looks like
κ
times
θ
." I'm going to give you that example. So, that example is going to be the following simple pendulum. Take a pendulum like this. It's got a mass
m
. It's got some length
l
; it's hanging from the ceiling. It's a rigid rod, not a string, but a rigid, massless rod. And the mass
m
is at the bottom. So, it's happy to hang like this, but suppose you give it a kick, so you push it over there to an angle
θ
, which is whatever you like. What is the torque in this particular case? Let's find out. The force is
mg
, and the angle between the force--and you're trying to do rotations around this point--this angle here is the same
θ
. So, torque is really minus
mgl sin
θ
. That's the formula for torque. It's the force times the distance of the lever arm or the distance over which the force is from the rotation axis times the sine of the angle between the direction of the force and the direction of the separation.
So, the equation for the pendulum really is the following:
Id2 θ
over
dt2
is equal to minus
mgl sin
θ
. Now, we cannot do business with this equation. This equation is a famous equation, but you and I don't know how to solve it with what we know. But we have learned, even earlier today--look at the formula for
sin x
.
Sin x
begins with
x
minus
x3
over 3 factorial, and so on. So, if
θ
is small, then you may write
mglθ
. So, for small angles,
sin
θ
is
θ
, and the restoring torque, in fact, is linear in the angle of the coordinate. So, by comparison now, we know that this fellow is our
κ
. So,
κ
for the pendulum is
mgl
. So,
κ
may not be universal in every problem, in each problem you've got to find
κ
. You find that by moving the system off equilibrium, finding the restoring torque, and if you're doing it right, restoring torque will always look like something, something, something times
θ
. Everything multiplying
θ
is our
κ
.
So, let's now calculate
ω
for the simple pendulum. I've shown you this is
κ
over
I
, and
κ
was
mgl
. And what's
I
? It's equal to moment of inertia of this mass around this point. The rod is massless. For a single point mass, we know the moment of inertia is just
m
times
l2
. So, you find
ω
is equal to square root of
g
over
l
, and that is 2
π
over
T
. So, you get back the famous formula you learned,
T
is 2
π
square root of
l
over
g
. This is the origin of the formula you learned in school. It comes from small oscillations of a pendulum.
So, think about this problem. If you pulled a pendulum by an angle so large that
sin
θ
is no longer approximated by
θ
but you need a
θ3
over 6 term -- it can happen for large enough
θ
- then, the equation to solve is no longer this. What that means is, if you took a real pendulum with a massless rod and a bob at the end, the time it takes to finish an oscillation, in fact, will depend on the amplitude. But only for small oscillations, when
sin
θ
can be approximated by
θ
, you will find whether you do that the time is the same. But if you go too far, the other terms in
sin
θ
will kick in, and the result is no longer true. The period of a pendulum, in fact, is not just a function of
l
and
g
, but also a function of the amplitude. Only for small amplitudes, you get this marvelous result.
There's one problem I want you to think about. I may do it myself. I think you should try to read up on it, and I will try to explain it next time. I'll give the problem to you and I will do it for you next time. I want you to think about it. Here is a hoop, like a hula hoop. It's hanging on the wall with a nail. And it's very happy to be where it is. Now, I come and give it a little push. It'll start oscillating. It'll look like that, and some time later it'll look like that, it's going back and forth. Your job is to find the
ω
for that hoop. So, you move it a little bit, and you find the restoring torque. And you're done. But you've got to do two things right to get the right answer. You've got to find the moment of inertia for circular loop not around the center, but around the point and the circumference. So, you guys know the magic words you've got to use. Parallel Axis theorem. And to find the restoring torque, here is the part that blows everybody's mind. When the loop goes to that position, where is gravity acting? Gravity's acting at the center of mass. The center of mass is somewhere here in the middle of the loop, even though there is no matter there. So, center of mass of a body need not lie on the body. The ring is a perfect example. So, if you remember the center of mass of a loop is in the center of the loop and put the
mg
there, you will get the right torque, and everything will just follow.
By the way, my offer to you is always open. If there's something about the class you want to change, you find it's hard, this, that, you can always write to me. I want your feedback, because I just don't know which parts are easy, which parts are hard, which are slow, which are fast. But if you haven't had enough math and you need some help, send me some e-mail and I will try my best to answer them.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_16_110106.mp3) |
