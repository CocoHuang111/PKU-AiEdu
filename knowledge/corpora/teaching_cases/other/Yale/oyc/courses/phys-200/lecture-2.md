> 检索摘要：Open Yale Courses「PHYS 200 Vectors in Multiple Dimensions」。主要内容：讨论多维运动，引入并讲解多维矢量及其大小和方向，说明零矢量、负矢量、单位矢量和速度矢量的性质，最后通过解题展示矢量相加与抛体运动。页内标题：Lecture 2 - Vectors in Multiple Dimensions；Overview；Lecture Chapters。分隔线后是英文原文，未翻译、未改写。

- Source: https://oyc.yale.edu/physics/phys-200/lecture-2
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 2 - Vectors in Multiple Dimensions

### Overview

In this lecture, Professor Shankar discusses motion in more than one dimension. Vectors are introduced and discussed in multiple dimensions. Vector magnitude and direction are also explained. Null vectors, minus vectors, unit and velocity vectors are discussed along with their properties. Finally, several specific problems are solved to demonstrate how vectors can be added, and problems of projectile motion are expounded.

### Lecture Chapters

1. Review of Motion at Constant Acceleration
2. Vector Motion 2D Space: Properties
3. Choice of Basis Axis and Vector Transformation
4. Velocity Vectors: Derivatives of Displacement Vectors
5. Derivatives of Vectors: Application to Circular Motion
6. Projectile Motion

1. 0
2. 285
3. 1377
4. 2300
5. 2620
6. 3240

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 2 - Vectors in Multiple Dimensions
Chapter 1. Review of Motion at Constant Acceleration [00:00:00]
Professor Ramamurti Shankar:
Everything I told you last time, you can summarize in these two equations. Remember what we did. We said, "Let's take, for the simplest case that we can possibly imagine, namely a particle moving in one dimension along the x-axis with a constant acceleration
a
. What is the fate of this particle?" The answer was: at any time
t
, the location of the particle is given by this formula.
x(t)
=
x0
+
v0t
+ ½
at2
. You can easily check by taking two derivatives that this particle does have the acceleration
a
. So what are these two other numbers--
x0
and
v0
and
x
-not and
v
-not? I think we know now what they mean. They tell you the initial location and initial velocity of the object. For example, suppose you use vertical motion and you use
y
instead of
x
; and
a
would be
-g
; that's a particle falling down under the affect of gravity. If all you know is the particle is falling under the affect of gravity, that's not enough to say where the particle is, right? Suppose we all go to a tall building and start throwing things at various times and various speeds. We're all throwing objects whose acceleration is
-g
. But the objects are at different locations at a given time. That's because they could have been released from different heights with different initial velocities.
Therefore, it's not simply enough to say what the acceleration is. You have to give these two numbers. Then once you've got those two numbers, they're no longer free parameters; they're concrete numbers, maybe 5 and 9. Then for any time
t
, you plug in the time
t
and you will get the location. If you took the derivative of this, you will get the velocity at time
t
, it would be:
v(t)
=
v0
+
at
. Again, you should not memorize the formula. I hope you know why it makes sense, right? You want to know how fast the guy is moving. This is the starting speed, that's the rate at which it is gaining velocity, and that's how long it's been gaining it. So you add the two. This also means the following. It is true that if you give me the time, I can tell you the velocity. Conversely, if I knew the velocity of this object, I also know what time it is, provided I knew the initial velocity.
Therefore, mathematically at a given time
t
, we can trade
t
for
v
and put it into this formula. Banish
t
everywhere. By doing it, I got this formula:
v2
=
v02
+ 2
a
(
x-x0
). This is a matter of simple algebra, of taking this and putting it here. But I showed you in the end how we can use calculus to derive that. I got the feeling, when I was talking to some of you guys, that maybe you should brush up on your calculus. You have done it before, but when you say, "I know calculus," sometimes it means you know it, sometimes it means you know of some fellow who does or you met somebody who knows. That's not good enough. You really have to know calculus. This is a constant problem. It's nothing to do with you guys. It is just that you have done it at various times.
It's a problem we have dealt with in the Physics Department year after year. One solution for that is to get a copy of a textbook I wrote called
Basic Training in Mathematics
. It's of a paperback for $30. I've given the name of the book on the class' website. If I hadn't written it, I would prescribe it, but that is a little awkward moment. You don't want to sell your own book. On the other hand, you don't have to withhold information that may be useful to the class. I think that book will give you all the basic principles you need in calculus of one variable, more variables, elementary complex numbers, maybe solving some problems with vectors and so on, which you're going to get into. Whether you are going into physics or not is irrelevant. If you're going into any science that uses mathematics -- chemistry, or engineering, or even economics -- you should find the contents of that useful. I think it'll be in your interest to get that any way you like. You can go to Amazon or you can go to our bookstore. The bookstore has some copies, but they are really for another course. So you should look at it and order it on your own.
Chapter 2. Vector Motion 2D Space: Properties [00:04:45]
Okay, so I will now proceed to the actual subject matter for today. I told you, the way I'm going to teach any subject is going to start with the easiest example and lull you into some kind of security and then slowly increase the difficulty. What's the next difficult thing? The next difficult thing is to consider motion in higher dimensions. How high do you want to go? For most of us, we can go up to three dimensions because we know we live in a three-dimensional world. Everything moves around in 3D. That'll be enough for this course. In fact, I'm going to use only two dimensions for most of the time because the difference between one dimension and two is very great. Between two and three and four and so on is not very different. There's only one occasion where it helps to go to three dimensions because there are certain things you can do in 3D you cannot do in less than 3D. But that's later, so we don't have to worry about that. We'll stop at two. If you talk to string theorists, they will tell you there are really, how many dimensions? Do you know? There are actually ten, including space and time. There are nine spatial dimensions. That's why I call them string guys. Mathematicians have luckily told us how to analyze the mathematics in any number of dimensions. We don't pay attention to them when they are going beyond three, but now we know we need that. We're going to do two.
Our picture now is going to be some particle that's traveling in the
xy
plane. The guy is just moving around like this. This is not an
x
versus time plot or
y
versus time. It's the actual motion of the particle. If you say, "Where is time?" one way to mark time is to imagine it carries a clock as it moves, and put markers every second. That may be
t
= 0,
t
= 1,
t
= 2 and so on. So, time is measured as a parameter along the motion of the particle. It is not explicitly shown. You can sort of tell the particles moving slowly or rapidly by looking at the space in between these tick marks. For example, here, in one second it went from here to here. Here, in one second, it seems to have gone much further, so it's probably traveling faster. If you want to describe this particle, what's the kinematics? You can pick a point and say, "I'm at the point
xy
." So, when you go to two dimensions, you need a pair of numbers. Instead of
x
, you need
x
and
y
. But what we will find is, it's more convenient to lump these two numbers into a single entity, which is called a vector.
That's what we're going to talk about a little bit, talk a little bit about vectors. You guys have also seen vectors, I'm pretty sure, but it is worth going over some properties and some may be new and some may be old. For the simplest context in which one can motivate a vector and also motivate the rules for dealing with vectors, is when you look at real space, the coordinates
x
and
x
. And let's imagine that I went on a camping trip. On the first day, here is where I was. Then, I tell you I went for 5 km on the second day and another 5 km on the third day. Then I ask you, "Where am I? How far am I from camp?" You realize that you cannot answer that. You cannot answer that, even if I promised to move only along the
x
-axis, because I think--I don't want to pose this as a question, because I think the answer is fairly obvious to everybody. It's not enough to say I went 5 km. I've got to tell you whether I went to the right or whether I went to the left. So I could be 10 km from home, I could be 0 km from home, or I could be -10, if I'd gone two steps to the left. You can deal with this by saying not just 5 km, but plus or minus 5 km. If you give a sign, on top of the number, that takes care of all ambiguity in one dimension. So the sign of the number is adequate to keep track of my motion.
But in 2D, the options are not just left and right or north and south, but infinity of possible directions in which I could go those 5 km. What I could do on the first day is to come here. On the second day, could be to go there. These two guys are 5 km long. For that purpose, to describe that displacement, we use a vector. This is called a vector; we are going to give it the name
A
. It starts from the origin and goes to this point. That is a description of what I did on the first day. The second day, I did this and that is the description of what I did on the second day. The proper way to draw a vector is to draw an arrow that's got a beginning and it's got an end. This is the reason behind saying a vector has a magnitude and a direction. A magnitude is how long this guy is and direction is at what angle it is. This is
A
and this is
B
. Now, you realize that--By the way, when you draw a vector like
A
, you're supposed to put a little arrow on top. If you don't put an arrow on top, it means you're talking about just a number
A
. It could be positive or negative or complex, but it's just an ordinary number. If you want to talk about an arrow of any kind, you've got to put a little arrow on top of it. In the textbook, they use boldface arrows. In the classroom, you use this symbol.
This is
A
and this is
B
. There's a very natural quantity that you can call
A
+
B
. If you want to call something as
A
+
B
, it means that I did
A
and then I did
B
. But if I want to do it all in one shot, what is the equivalent step I should take? It's obvious that the bottom line of my two-day trip is this object
C
. We will call that
A
+
B
. It does represent the sum, in the sense that if I gave you four bucks and I gave you five bucks, I gave you effectively nine. Here, we are not talking about a single number, but a displacement in the plane.
C
indeed represents an effective displacement. This is the rule for adding vectors. It has an origin in this simple example. Okay, so the rule for adding the two vectors is, you draw the first one and at the end of that first one, you begin the second one. The sum starts at the beginning of the first and ends at the end of the second. Okay, so that tells you how to add two vectors and get a sum. You can verify, in this simple example, that
A
+
B
is the same as
B
+
A
.
B
+
A
would be--First draw
B
and from there you draw
A
. You will end up with the same point. You say this is a commutative law. It doesn't matter the sequence in which you add the two vectors. You know that's true for ordinary numbers, right? 3 + 4 and 4 + 3 are the same. It's also true for vectors. But the law of composition is not always commutative. There are certain occasions in which you first do
A
and then do
B
; that's not the same as first doing
B
and then doing
A
. We'll come to that later. Right now, this is the simple law.
Alright, next thing I want to do is to define the vector that plays the role of the number 0. The number 0 has a property. When you add it to any number, it doesn't make a difference. I want a vector that I want to call the 0 vector. It should have the property that when I add it to anybody, I get the same vector. So you can guess who the 0 vector is. The 0 vector is a vector of no length. If this is
A
, I'm going to draw a vector here. I cannot show you the 0 vector. The minute you can see it, I'm doing something wrong. If you can see it, it's wrong, because it's not supposed to have any length. But it has a property that when you add it to anything, you get the same vector. So that vector is called a "null vector." How about this guy? I draw
A
, then I draw another
A
. This is
A
+
A
. You have to agree that if there's any vector that deserves to be called 2
A
, it is this guy. This is
A
+
A
. We're going to call it 2
A
. The beauty of that is now we have discovered a notion of what it means to multiply a vector by a number. If you multiply it by 2, you get a vector two times as long. Then you're able to generalize that and say, if you multiply it by 2.6, I mean a vector 2.6 as long as
A
. So multiplying a vector by a number means stretch it by that factor.
Then, I want to think of a vector that I can call
-A
. What do I expect of
-A
? I expect that if I add
-A
to
A
, I should get the guy who plays the role of 0 in this world, which is the vector of no length. It's very clear that if you want to take
A
and ask, "What should I add to
A
so I get the null vector?" it's clear that you want to add a vector that looks like that, because then you go from the start of this to the finish of that, you end up at the same point and you get this invisible 0 vector. So the minus vector is the same vector flipped over, pointing the opposite way. That's like -1 times a vector. Once you've got that, you can do minus 7 times a vector or -5
π
times a vector. Just take the vector, multiply it by 5
π
and flip it over. That's -5π times a vector. This is how you get the rules for adding a vector to another vector, then taking a vector and multiplying it by some constant. Then, of course, you can do more complicated things. You can take this vector, multiply it by one number, take that vector, multiply it by another number, add the two of them. We know what all those operations mean now. You don't have to memorize all this. The only rule is, "do what comes naturally." Do what you normally do with ordinary numbers. This seems to work for vectors. You should know what multiplying a vector by a number means. So this is the notion of what vectors are. Now, we are going to come to some important concept, which is the following.
You go back to the same
xy
plane; here is some vector
A
. I'm going to introduce two very special vectors. They are called unit vectors. This guy is
I
, that is
J
. If I had a third axis,
I
would draw a
K
, but we don't need that. So
I
and
J
are vectors of length one, pointing along
x
and
y
. The claim is, I can write any vector you give me as a real scale
I
plus a real scale
J
. There's nothing you can throw at me that I cannot handle with some multiple of
I
and some multiple of
J
. It's intuitively clear, but I will just prove it beyond any doubt. Here is the vector
A
. It is clear that that vector is the sum of that vector and that vector, by the rules of vector addition, because that plus that is equal to the
A
. But how about this part? This part, being parallel to
I
, has to be a multiple of
I
. We know that because you can stretch
I
by whatever factor you like. So whatever number it takes,
Ax
times
I
is this part. This part, being parallel to
J
, has to be some multiple of
J
. I'm going to call it
Ay
. Therefore, the vector
A
that you gave me, I have managed to write as (
I
times
Ax
) + (
J
times
Ay
).
You can ask yourself, "If you gave me a particular vector, what do I use for
Ax
and
Ay
?" You can see from trigonometry that if this angle was
θ
here and the length of the vector I'm going to call by
A
.
A
is the length of
A
. If you drop the arrow, it's the usual convention, if you're talking about the length of the vector A. First of all, it's clear from the Pythagoras' theorem that
A
is the square root of
Ax2
+
Ay2
. The angle
θ
that it makes with the
x
-axis satisfies the condition tan (
θ
) is
Ay
over
Ax
.. What this means--Now here's the main point. If you give me a pair of numbers,
Ax
and
Ay
, that's as good as giving me this arrow, because I can find the length of the arrow by Pythagoras' theorem. And I can find the orientation of the arrow by saying the angle
θ
that satisfies tan (
θ
) is
Ay
over
Ax
. You have the option of either working with the two components of
A
or with the arrow. In practice, most of the time we work with these two numbers,
Ax
and
Ay
. If you are describing a particle with location
r
, the vector we use typically to locate a particle
r
, then
r
is just (
I
times
x
) + (
J
times
y
), because you all know that's
x
and that's
y
.
I've not given you any other example besides the displacement vector, but at the moment, we'll define a vector to be any object which looks like some multiple of
I
plus some multiple of
J
. Suppose I tell you to add two vectors,
A
and
B
equal to
C
, and I say, "What's the result of adding
A
and
B
?" You've got two options. You can draw the arrow corresponding to
A
. Then, you make an arrow corresponding to
B
and lay it on the end of this one. Then add them, as shown here. But you can also do something without drawing any pictures. That would come by saying, "I'm taking (
I
times
Ax
) + (
J
times
Ay
) + (
I
times
Bx
) + (
J
times
By
)," and I'm trying to add all these guys. But then, I combine (
I
times
Ax
) with (
I
times
Bx
), because that's the vector parallel to
I
, with the length
Ax
. That's the vector parallel to
I
, with length
Bx
. That's clear. If I add them, I'll get a vector parallel to
I
with lengths
Ax
+
Bx
. Then
Cy
=
Ay
+
By
. I have to be really careful when I said, "Add the lengths." I'm assuming all the components are positive. If the
Ax
and
Ay
, some are positive and some are negative, this is the way by which we have learned we should combine multiples of
I
. When I give you multiple of
I
and another multiple of
I
, there's some has got as its coefficient the sum of the two coefficients. This says, when you add two vectors, you just add the components, so that if this vector is called (
I
times
Cx
) + (
J
times
Cy
), then it's worth knowing that
Cx
is (
Ax
+
Bx
) and
Cy
is (
Ay
+
By
). Most of the time, when we deal with vectors, we don't draw these arrows anymore. We just keep a pair of numbers. If you give me another vector, there's another pair of numbers. If you say, "Add the vectors," I would just add the
x
to the
x
and the
y
to the
y
and I'm keeping track of what the sum is.
A very important result is that if two vectors are equal, if
A
=
B
, the only way it can happen is if separately
Ax
is equal to
Bx
and
Ay
is equal to
By
. That's the very important difference. You cannot have two vectors equal without exactly the same
x
component, exactly the same
y
component. That's pretty obvious. If two arrows are equal, you cannot be longer in the
x
direction and correspondingly short in the
y
direction. Everything has to completely match. Vector equation
A
=
B
is actually a shorthand for two equations. The
x
parts match and the
y
parts match.
Chapter 3. Choice of Basis Axis and Vector Transformation [00:22:57]
Now, when you work with components,
Ax
and
Ay
, if I didn't mention it, they are the components of the vector, you can do all your bookkeeping in terms of
Ax
and
Ay
. But you've got to be aware of one fact. If I just come and say to you, "Here's the vector whose components are 3 and 5. Can you draw the vector for me?" Can you draw it or not? Does anybody have a view? Yes? No? Yes? Pardon me? Yeah, if you immediately said, "Well, if the vector is 3, 4, then the vector looks like this," you're making the assumption that I am writing the vector in terms of
I
and
J
. You see,
I
and
J
is very natural direction. For most of us, gravity acts this way, defines a vertical direction very naturally and the blackboard is oriented this way, so very natural to call that x and call that y and line up our axes. But you agree that there is no reason why somebody else couldn't come along and say, "You know what, I want to use a different set of axes. Those directions are more natural for me."
In fact, just because the world is round, you can already see if this is the Earth, to somebody that's the natural direction. If you go to another neighboring country, that's what they think is naturally
x
and
y
. There is no reason why
x
and
y
are nailed in absolute space. It's very important that
x
and
y
are human constructs and we're not wedded to any of them. Quite often, it's natural to pick
x
and
y
in a certain way, because starting a projectile near the Earth, it makes sense to pick the horizontal as
x
and vertical as
y
. Mathematically, you don't have to.
Very important point that comes up is the following. What if somebody comes along and has got a new axis? Here is the unit vector
I
′, that's unit vector
J
′ and here is this vector
A
. And the angle between my axis, let's say, and your axis is some angle
φ
. The same vector
A
can be written either in terms of
I
and
J
or in terms of
I
′ and
J
′. Let's take a minute to just play this game of asking. How do the components of
A
in the new rotated coordinate system relate to the components of the old coordinate system? It's a simple problem, but I just want to do it so you get used to working with vectors. The point is the arrow
A
, somebody has chosen to write in terms of
I
′ and
J
′ as
Ax
′ and
Ay
′. Do you guys follow that?
I
′ and
J
′ are now rotated unit vectors. And somebody wants to think in terms of those. In other words, the person wants to ask, "How much
I
′ and how much
J
′ do I need to build up the vector
A
?" That person will get a different answer. You're asking, "How much
I
and how much
J
do I need to build the same object?" The same entity written in two different ways. If she's got a pair of numbers and you got a pair of numbers, the new numbers are called the primed numbers and you want to write them in terms of yours. For that, what do you need? You need to know what
I
′ is in terms of
I
and
J
.
Let's draw a little picture on the side here. This is
I
′. It's got a length 1, it's at an angle
φ
. I'm going to write something and I'll wait until you guys tell me you're comfortable with this. I′ is
I
cos
φ
+
J
sin
φ
. There should not be anybody in this room who is mystified by this statement. This vector
I
′ has got a horizontal part, which is its length, which is 1 times cos
φ
, and a vertical part which is 1 times sin
φ
. This kind of trigonometry you should know all the time. It's not something you're going to go back and remember it's an opposite side, it's an adjacent side. You've got to know that really well. You've got to be very used to the notion of taking a vector in some oblique direction and writing it in terms of
I
and
J
. How about
J
′ ?
J
′ is pointing in that direction. It's at an angle
φ
. So
J
′ will be -
I
sin
φ
+
J
cos
φ
. If it's not obvious, I think this is the kind of thing you should fill in the blanks when you go home. Leave a line there and think about it and fill in the blanks later. It's very important to know if these two axes are at angle
φ
, those two axes are also at angle
φ
. That's the result you use all the time in mechanics. Once you do that, I think it's fairly clear that it has got a
y
component that's given by cosine and an
x
component that's given by sin
φ
; the
x
component is negative. This vector has a little bit of negative
I
in it.
Here is what I'd say you should do. This is the kind of thing I don't want to do in classroom. It takes time and I'm probably going to screw up. Imagine taking
I
′ and
J
′ and stick them here and here. Do this in your head and ask, "What can I possibly get?
I
′ and
J
′ have been banished. Everywhere they're replaced by
I
and
J
. You can now collect the whole expression as something something
I
plus something something
J
. What you will get for
I
will be
Ax
cos
φ
Ay
sin
φ
. Then, here you will get
Ay
cos
φ
+
Ax
sin
φ
. This is the only part I don't want to do explicitly. I'm just saying, "Take this and put it there and combine
I
and
J
." But this is the same vector we are calling (
I
times
Ax
) + (
J
times
Ay
). I've told you, if two vectors are equal, the components must match. I may then--I'm sorry. I'm making a mistake here.
This should be prime. By the way, when you guys do this, did anybody notice prime? If you noticed it, you got to stop. You cannot let me write anything that's incorrect. You got to follow it in some detail. I know you couldn't do the details, but you should at least know that it's
I
′ and
J
′ that have been replaced by
I
and
J
. But
Ax
′ and
Ay
′ will continue to be the coefficients. So if I make a comparison, I find
Ax
=
Ax
′ cos
φ
Ay
′ sin
φ
and
Ay
= -
Ax
′ sin
φ
+
Ay
′ cos
φ
.
What's the purpose of the exercise? The purpose of the exercise is to make the following precise remark. You can pick your unit vectors, or what are called basis vectors, any way you like. Pick any two perpendicular directions which may be related to the ones I picked by an angle
φ
. Then the same entity, the same arrow which has an existence of its own, independent of axes, can be described by you and me using different numbers. There's a precise connection between the numbers you use and the numbers I use. Your numbers with the primes on them are related to mine by this relation. Now, you can ask the opposite question. How do I get your numbers in terms of my numbers? What should I do? They won't invert the relation. Anybody have an idea of what I should do now? No one has a clue on how I can go back from these to that? Let me take a second to ask. Do you have any idea what you should do? Okay, maybe you are--yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
Negative of
φ
? Yes. Okay. His idea was, the formula written for the opposite one will have the opposite angle; he replaces
φ
by minus of that. That turns out to be the correct answer. But I want you guys to think about why it was difficult to do it another way, which is more pedestrian. If I told you 3
x
+ 2
y
= 9 and 4
x
+ 6
y
= 6, you certainly know how to solve for
x
and
y
, right? This is something you've seen in your high school. You've got to juggle the two equations, multiply that by 4, multiply that by 3, add and subtract and so on. Why is it when you saw this, you didn't realize it's the same problem? It's the same problem;
φ
is the angle, sine and cosine are definite numbers. If I pick an angle of 60%, these are some numbers like half and root 3 over 2. I'm trying to write these two unknowns in terms of these two knowns and you can solve for them. Here though, what you multiply by would be sine
φ
s and cos
φ
s, so you can eliminate. For example, if you multiply this by sin φ and multiply this by cosφ and add them, the
Ax
′ will drop off. That's the kind of thing you should do.
Maybe I will add this on as a problem you should do in your homework. Do you realize that this is a pair of simultaneous equations in which you can solve for these two unknowns, if you like, in terms of these two knowns and these coefficients, which are like these numbers, 3, 2, 4, and 6? You can do that, but we like to get the answer the way this gentleman described it, because we like to get an answer more readily than by doing the mundane work. The idea that he had was, if you go from me to you, with a clockwise rotation, you go from you to me by a counterclockwise rotation. Therefore, if I go by
φ
to you, then you must go by -
φ
to come to me. That's correct. You will find then the result is
Ax
cos
φ
+
Ay
sin
φ
. I'm using the fact that when you take a cosine and change the angle inside the cosine, it doesn't care; whereas, if you go to the sine and change the angle inside the sine, it becomes minus sine. In other words, sine of minus
φ
is minus sin
φ
and cosine of minus
θ
is cos
φ
. This, by the way, is another property I expect people to know in this course. You cannot say, "I never heard of it. I don't know where it came from." You should think about why that is true. If you do that, you will find this result. So, there is a way to go from the unprimed coordinates to the′ coordinate by rotating your axis and actually calculating the components.
Now, here is a very important message, which is the following. When you go from one set of axes to another set of axes, the numbers change. The components of the vector are not the same. You might think it's all along
x
and somebody can tell me it's all along my new
y
axis. So the components of vector are not invariant. They depend on who is looking at the vector. There's one quantity that's going to come out the same, no matter who is looking at the vector. Anybody have a guess? Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
The length of the vector is the length of the vector. Perhaps it's clear to you that no matter how your axes are oriented, when you ask, "How long is this arrow?" you are going to get the same answer. That means
Ax2
+
Ay2
=
Ax
′ squared +
Ay
′ squared. That's a property of this expression. You can square this guy and add it to the square of this guy and you will find, using the magic of trigonometry, that this is true. I'm going over these points, because they're very, very important. When we do relativity, we'll be dealing with vectors in space-time and we'll find that different observers disagree on what is this and what is this. But they will agree on certain things. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
Here?
Student
: [inaudible]
Professor Ramamurti Shankar:
Here?
Student
: [inaudible]
Professor Ramamurti Shankar:
This has a minus and that doesn't have a minus.
Student
: [inaudible]
Professor Ramamurti Shankar:
Oh, here?
Student
: [inaudible]
Professor Ramamurti Shankar:
No, here both are plus, but this one has a minus.
Student
: [inaudible]
Professor Ramamurti Shankar:
Oh, I'm so sorry. Yes. That is correct. Thank you. That's right. The minus is only up there. Very good. Certain things are called invariants. This is an example of an invariant. By the way, I want to conclude with one important point. We learned that a vector is a quantity that has a magnitude and a direction. Actually, the view of vectors we take nowadays is that vectors are associated with a pair of numbers which, on the rotation of axes, transform like this. Anything that transforms this way is called a vector. Now, I want to ask the following question. Can I manufacture new vectors? We've got one vector which is
r
. How about more vectors? More position vectors? I want to look at that. That turns out to be a very nice way to produce vectors, given one vector, the position vector. And that's the following.
Chapter 4. Velocity Vectors: Derivatives of Displacement Vectors [00:38:20]
Let's take a particle that is moving in the
xy
plane, so that at one instance--sorry, let me change this graph-- is here--oh, this is bad. Let's see. It's moving like this. I'm here now. A little later, I am there. That's what I meant. This is called
r
. This is called
Δr
, this is called
r
+
Δr
. The particle is moving along this arc. Initially, its location as a function of time is equal to
I
times
x(t)
+
J
times
y(t)
. You wait a short amount of time, it goes to a new location, which I'm going to call
r(t)
+
Δt
. What can that be? It can be
x(t)
plus some change in
x
plus
J
times
y(t)
plus a change in
y
. That, we recognize to be
r(t)
plus everything else, which is
I
times
Δx
+
J
times
Δ
y. I'm going to call this guy a tiny vector
Δr
.
In other words, when you move on a line, you wait a small time
Δt
. You move by an unknown
Δx
. When you move in the plane, your change is, itself, a vector. You start with a vector, you change by this vector
Δr
. It gives you the new location.
Δr
has got two components. It's got a change in
x
and it's got a change in
y
. Therefore, we will define what's called the velocity vector, which is, if you want the limit as
Δt
goes to 0 of
Δr
over
Δt
, and you can see that is going to be
I
times
dx
over
dt
+
J
times
dy
over
dt
, you can actually take derivatives of a vector with time. That's also a vector.
Why is the derivative of a vector also a vector? Because the difference in the vector between two times is its vector. Dividing by
Δt
is like multiplying by 1 over
Δt
. But I know when I multiply a vector by a number, I get a vector in the same direction. What this really means is that if you take the limit as
Δt
goes to 0, I cannot draw it that well, but imagine bringing the second point closer and closer to the first one.
Δr
is getting very small;
Δt
is very small. But by the miracle of calculus, the ratio will approach a definite limit. That limit will be some arrow we can call the velocity at the time and it will always be tangent to the curve. The tangent's pointing towards the direction you are headed at that instant. If I gave you the location of a particle as a function of time, you can find the velocity by taking derivatives.
For example, if I say a particle's location is
I
times
t2
+
J
times 9
t3
, for every value of time, you can put the numbers in and you can find the velocity by just taking derivatives. The derivative of this guy will be 2
t
times
I
plus what? 27
t2
times
J
. Rule for taking derivatives, if you want to do this mindless application of calculus, you can do it.
I
and
J
are constant; ignore them when you take derivatives;
x
and
y
are dependent on time. Just take the derivatives and that's the velocity vector. You can take a derivative of the derivative and you can get the acceleration vector, will be
d2r
over
dt2
, and you can also write it as
dv
over
dt
.
Anybody have a question with what I've done now or what we're doing here? Let me summarize what I'm saying. Particle's moving in a plane. At every instant, it's got a location given by the vector
r
;
r
itself is contained in a pair of numbers,
x
and
y
, and they vary with time. When you vary time a little bit and ask, "How does
r
change?" and you take the quotient of
Δr
to
Δt
, you get the velocity vector. Mathematically, it's done by taking the expression for
r
and differentiating everything in sight that can be differentiated as vector
t
. Even though we started with a single vector, which is the position vector, we're now finding out that its derivative has to be a vector and the derivative of the derivative is also a vector. Again, when you learn the relativity, you will find out there's one vector that's staring at you. I'll come to what that is. That's the analog of the position vector. But more and more vectors can be manufactured by taking derivatives.
Chapter 5. Derivatives of Vectors: Application to Circular Motion [00:43:40]
Now, I want to do one concrete problem where you will see how to use these derivatives. I'm going to write the particular case of
r(t)
and take derivatives. We'll get a feeling for what's going on. The problem I have in mind looks like this.
r(t)
is going to be a fixed number
r
times
I
times cos>
ωt
+
J
times
ωt
.
ω
is a new creature. You don't know what it is right now. I'm going to just put that in.
ω
times
t
is some number and it's the cosine of the number times
I
plus sine of the number times
J
times
r
. What is going on as a function of time? What's this particle doing? First thing you can tell is that if you find the length of this vector, you'll find the square of the
x
and the square of the
y
. But since sine square plus cosine square is 1, you'll find this vector has a fixed length
r
. That means, it can only be rattling around in a circle of radius
r
. In fact, what the guy is doing looks like this. At any given time
t
, draw an angle
ω
t
and a radius
r
and that's where your particle is. Do you see that? Because the
x
component of this one is
r
cos
ω t
and the
y
part is
r
sin
ωt
.
ω
is a fixed number. As
t
increases, this angle increases and the particle goes round and round. We're describing the motion of a particle in a circle. Let's understand what
ω
is. Let's get a feeling for
ω
. As time increases, the angle increases and we can ask, "How long does it take for the particle to come back to the starting point?" Suppose the starting point was here. As I increase
t
,
ωt
will increase, and I want to come back to where I start. You've got to ask yourself, let the time it takes to do a full circle, that's the time period, do a full circle. What can you say about
ωt
? What should be the value of
ωt
?
Student
: [inaudible]
Professor Ramamurti Shankar:
Very good. You can say it's 360 degrees, that's fine. But we like to measure angle in radians. How many people know about radians? Okay. For those who have not seen a radian, it's just another way to measure angle with the understanding that a full circle, which we used to think is 360 degrees, is equal to 2
π
radians. 2
π
is roughly 6. So a radian is roughly 60 degrees. It's 58 and a fraction. Why do you like to measure angle in the peculiar way? You will see the advantages of that later. We'll adapt the convention that we'll measure angle in a radian. So that a half circle, instead of calling it 180 degrees, we will call it just
π
. And a quarter circle, instead of 90, we will call it
π
over 2 and call it as
π
over 4 and so on. It's good to know certain famous angles. This is
π
over 2, this is
π
, this is 3
π
over 2, and this is back to 2
π
. Therefore,
ωt
= 2
π
tells you that
ω
is 2
π
divided by the time it takes to complete a revolution. One over the time period is what we call the frequency, so you can write it as--f is just the usual frequency. 60 Hertz means you do 60 revolutions per second. Alright. How fast is this particle moving? It's going around a circle. The angle is increasing at a steady rate, so we know it's going at a steady speed. I'm asking what's the tangential speed as it moves along the circle? Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
How do you reach that conclusion?
Student
: [inaudible]
Professor Ramamurti Shankar:
I agree, but I want the speed in meters per second.
ω
will be in radians per second. Yes?
Student
: [inaudible]
Professor Ramamurti Shankar:
And how did you get that?
Student
: [inaudible]
Professor Ramamurti Shankar:
Okay. That's correct. But let me deduce that in another way. Your answer is completely correct. It is
ωr
. I want to say how you get it. One way is to say, if I do a full revolution, I think of the speed as a distance over time. I'm going to go one full revolution. The distance I travel is 2
πr
. But 2
π
over
t
was identified as
ω
. So the tangential velocity at any point is equal to
ω
times
r
. That's a useful quantity to know. Now, you can take this velocity, you can take this
r
. Let me find
V(t)
.
V(t)
is obtained by taking derivative of this expression. I think you guys know enough calculus for me to write is equal to
r
times
I
times minus
ω
sin
ωt
, plus
J
times
ω
cos
ωt
. That is the velocity of this guy. I invite you to try this formula whenever you want. Pick a time. Let's say, if I go a quarter of a circle, I expect to be moving to the left. A quarter of a circle means
ωt
is
π
over 2. Cosine of
π
over 2 is 0, because cos 90 is 0; sin of
π
over 2 is 1 and I get a speed of
ωr
in the negative
I
direction.
ωr
was the speed. That's indeed the correct answer. You can satisfy yourself at various times as going like this.
Let's sneak in one more derivative here, which is to take the derivative of the derivative. That's a very important result. To do that, let's take one more derivative. Let's try to do part of it in the head, so I can just write down the answer. If you take one more derivative, the sine is going to become a cosine and yield another
ω
. This cosine is going to become a minus sine and give me another
ω
. If you do that, you will find the whole answer is equal to
-ω2
times just the vector
r
itself. That's a very interesting result. It tells you when a particle moves in a circle, it has an acceleration in a negative
r
direction, namely directed towards the center. What's the magnitude of that acceleration? I write it without an arrow here. That's equal to
ω2
times a magnitude of this vector, which is just
r
.
But now, I can also write it as
v2
over
r
. Here, ready? This is a very important formula. I don't know how many kids, generation after generation, get in trouble because they do not remember the following fact. I'm going to say it once more with feeling. When a particle moves in a circle, it has an acceleration towards the center of this size,
v2
over
r
. Very simple. It comes from the fact that velocity is a vector and you can change your velocity vector by changing your direction. This particle is constantly changing its direction, but it therefore has an acceleration and the acceleration, we have shown here, is pointing towards the center. The size of that is
v2
over
r
. For example, if a car is going on a racetrack and you're seeing it from the top, if the speedometer says 60 miles per hour, you might say it's not accelerating. That's the layperson's view. If it's going in a circle, you will say from now on, that it, indeed, has an acceleration, even though no one's stepping on the accelerator, of amount
v2
over
r
. That's a very important thing. That's what you're learning in this course. The fact that when you step on your gas you accelerate, everybody knows. The fact that when you go in a circle, you accelerate is what we're learning here, coming from the fact that velocity is a vector and its change can be due to change in the magnitude or change in direction. This was a problem, but the magnitude of velocity was nailed down and fixed at
ωr
, but the direction is constantly changing.
So I'm going to now do a second class of problems. We will return to this issue later. By the way, one thing I should mention to you. Suppose the particle is not moving in a circle, but does this. Let's take a circle and just keep a quarter of the circle. During this part, when you're doing a quarter of a circle, this is supposed to be a quarter of a circle. You have the same acceleration directed towards the center. In other words, you don't have to be moving actually in a circle to have the acceleration. At any instant, your motion, if it follows any curve, locally can be approximated as being part of some circle. You can take circles of different size and place them against your trajectory and see which one fits. That's the
r
.
v2
over
r
is the acceleration directed towards the center of that circle.
Chapter 6. Projectile Motion [00:54:00]
One miscellaneous result, which we don't use very much now, but which I should mention to you is the following. Suppose this is the ground with some origin here. That's the plane with some origin here. And in the plane there is some other object. What's the location of the object? Let us say
P
for plane,
G
for ground,
O
for object. I think it's clear, the position of the object with respect to the ground, this vector is the same as the position of the object with respect to the plane, plus the position of the plane with respect to the ground. Agreed? Okay. This is the picture here. We can start taking derivatives of this with respect to time. That'll say the velocity of the object with respect to the ground, the velocity of the object with respect to the plane, the velocity of the plane with respect to the ground. That means, if you are going in a plane and you throw something up in the air, it seems to be going up and down to you. But if I see you through the glass, the object is going on some trajectory, which has got both up and down and horizontal motion. This is the rule for adding velocities. When you have a velocity in the moving plane frame and you want to find the velocity on the ground, you should add to every object in the plane the velocity of the plane with respect to the ground. That's intuitively clear. You use it all the time, but maybe along one dimension. But this is the way to do it in two dimensions. There may be some simple problem involving this in the problem I assigned, so I am just going over this.
The problem we want to do today, a whole family of problems, looks like this. I want to consider a particle which has definite acceleration
a
, a constant one, but
a
is now a vector. The question I have is, "What is its location at all future times?" I think you can tell by analogy with what I did in one dimension that the position of that object at any time
t
is going to be the initial position plus velocity times
t
plus ½
at2
. Everything is the same as in 1D, except everybody's a vector now. Initial position is a pair of numbers. Initial velocity is a pair of numbers. Once you know those, you can find the position of the object at all future times. Let's take one simple example. There is somebody in a car and decided to fly off. We want to know, as you can tell--our concern is where does the car hit the ground? When does the car hit the ground? That's the problem in two dimensions. How do we solve this problem? We pick our origin to be this point here. Let the height of the building be
h
. Car is traveling with some initial speed
v0
in the horizontal direction. This equation is a pair of equations. One along
x
and one along
y
. For the
x
part, I'm going to write
x
=
x0
+
v0t
.
x0
I'm going to reduce to 0 by choice of my origin being here. The
x
coordinate of the car is the 0, because this is my origin.
How about the
y
coordinate? The equation for the
y
coordinate is the height of the building. The velocity has no vertical component. There is no
vy
. But it has an acceleration of
-g
. So this is the fate of this person at any given time
t
. Our
t
= 0, you have him right on top of this edge. At all future times,
x
proceeds as if nothing happened and then
y
, you are falling. If you want to know something like when do you hit the ground, I think it's fairly clear what you have to do. For example, if
t*
is the time you hit the ground, then
t*
satisfies the equation
h
- ½
gt*2
= 0. You solve for the
t*
from this one and you put it there. That tells you where you land. I don't think I have to actually do that step. I'm assuming you can fill in the blanks. Solve this equation for
t*
, put it there and that's where you land. That's one class of problems. Here's the second class.
The second class is the most popular application of what I'm doing now. I want you not to memorize every formula the book gives you for this problem. That's a problem of projectile motion. Projectile motion. You start here and you fire a projectile with some velocity
v0
at some angle
θ
. It's going to go up and it's going to come down. One question is: Where is it going to land? Another question is: At what angle should you fire your projectile so it will go the furthest? You can find the equation, but you've got to think a little bit before you solve everything. It's good to have an idea of what's coming. Imagine you got this monster cannon to fire things. It's got a fixed speed
v0
. How do you want to aim it so you can be most effective? Go as far as you can? There are two schools of thought. One says, aim at your enemy and fire like this. Then it lands on your foot, because assuming the cannon is at zero height, the cannonball certainly comes out towards the enemy, but has no time of flight. Other one says, maximize the time of flight and you point a cannon like this. It goes up, stays in the air for a very long time, but it falls on your head. We know the truth is somewhere between 0 and 90. Now, the naïve guess may be 45, but it turns out the naïve guess is actually correct. I just want to show you how that comes out. I don't want you to cram this formula. This is the kind of thing you should be able to deduce. Let's go back to the same thing I wrote earlier.
x
= 0 plus-- What's the horizontal velocity? Horizontal velocity is
v0
cos
θ
. So
x
is
v0
cos
θ
times
t
. And
y
is
v0
sin
θ
times
t
minus ½
gt2
. Now we know everything about this particle. I told you once you know the free parameters,
r0
and
v0
, you know everything about the future of the object.
Let's ask, what's the range? Range is that distance. What's the strategy for range? You see how long you are in the air and the whole time you are in the air, you are traveling horizontally at this speed. Again, let
t*
be the time when you hit the ground. You said 0 = (
v0
sin
θ
- ½
gt*
) times
t*
. I just pulled out a common key. It says you are on the ground on two occasions. One is initially. We are not interested in that. If the time you are interested in is not zero, you're allowed to cancel it and get the time from here. That time is
t*
= 2
v0
sin
θ
over
g
. That's how long you are in the air. This says, if you want to be in the air for a long time, maximize sin
θ
, so you may think that 90 degrees is the best angle. But that's not the goal. The goal is to get the biggest range. Go back to
x
and put your value for
t*
, which is 2
v0
sin
θ
/
g
. That becomes
v02/g
times 2 sin
θ
cos
θ
. If you go back to your trigonometry, you should find that is really the formula for sin 2
θ
. That's another example where knowing the trigonometry is very helpful. This tells you exactly what you want. It says, make sin 2
θ
as big as you want. That tells you 2
θ
is going to be 90 and
θ
is going to be 45. It's not from a naïve guess that it's halfway between 0 and 90. It turns out to be-- there's a fairly complicated balance between the time of flight and the range. Some people memorize this. I would say, don't do that. After a while, you won't have room in your head for anything. Just go back as often as possible to this formula and work your way from there. There are more variations, but it's always the same thing.
Here's another variation. In my days, they would say, "Find out when you want an object to go through that point." I tell you the initial velocity
v0
, I tell you at what angle I fire it. I want you to find the speed so it will land here. How do you do that problem? You do that problem by saying, suppose this actually happens at some time
t
. At that time
t
, the
x
coordinate must have a certain value. Then go to the
x
equation and demand that this be equal to the desired
x
value and find the time. I take the time and put it in the
y
equation and demand that the
y
I get, agrees with this
y
. If you do that, you will find there is one unknown, which is
v0
, and we can solve for
v0
. This is the most general problem you can have.
In the textbook, of course, people make them interesting. Suddenly there's a mountain. There's a physicist hiking on this mountain. See, you're already laughing. It's not a very credible problem. We don't hike and when we get stuck, we don't want food, we want our table of integrals. That's what we want somebody to send to us. These problems are embellished in many ways to make you all feel involved. For example, instead of a stone dropping, nowadays there's a monkey that's falling down. The people in life sciences feel, "Hey, we are represented in this subject." All those creatures, which are very interesting, in the end, you are told, "There's a horse inside a railway carriage." You cannot see the horse, but the horse is moving. You can deduce it because the carriage is moving the other way. There's a picture of a horse, a picture of the carriage, all glossy stuff. Then it says, "Treat the horse as a point particle." See? That's what we learned in the old days. But nowadays, it's a horse, but in the end, if you're going to treat it as a point particle, it seems to me to be a real waste.
If you're the Godfather, right? You want to get the contract for Johnny Fontaine, you don't tell your consiglieri, "Hey Tom, put a point particle on Jack's bed." When you want a horse, use a horse. When you want a point particle, if you wake up and find a point particle on your bed, what's your reaction? I think these extra pictures sometimes they're helpful, sometimes they just make the book cost a lot more. There are problem in that a horse must be treated when we study rigid bodies. Even there, a horse is not really a rigid body, unless it's been dead for a long time. The fact is not a point particle is important. I think the reason books are bigger and bigger but still carry the same information is that examples are more and more interesting. Sometimes they serve a purpose. Sometimes they are distracting. I haven't written a book in this field, so I will not say anything more.
Alright, so I think I should stop now. Next week, we're going to get a clock that you guys can see in the back. I know you're very anxious to know the time like I am. But then you can just look back or maybe they'll put one up here.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_02_091106.mp3) |
