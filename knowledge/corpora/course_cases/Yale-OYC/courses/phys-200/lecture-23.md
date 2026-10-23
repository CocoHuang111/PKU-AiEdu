- Source: https://oyc.yale.edu/physics/phys-200/lecture-23
- source_format: html
- capture_date: 2026-10-08

---
## Lecture 23 - The Second Law of Thermodynamics and Carnot's Engine

### Overview

Why does a dropped egg that spatters on the floor not rise back to your hands even though no laws prohibit it? The answer to such irreversibility resides the Second Law of Thermodynamics which explained in this and the next lecture. The Carnot heat engine is discussed in detail to show how there is an upper limit to the efficiency of heat engines and how the concept of entropy arises from macroscopic considerations.

### Lecture Chapters

1. Recap of First Law of Thermodynamics and Macroscopic State Properties
2. Defining Specific Heats at Constant Pressure and Volume
3. Adiabatic Processes
4. The Second Law of Thermodynamics and the Concept of Entropy
5. The Carnot Engine

1. 0
2. 802
3. 1561
4. 2637
5. 3542

| Transcript | Audio |
| --- | --- |
| html
Fundamentals of Physics I
PHYS 200 - Lecture 23 - The Second Law of Thermodynamics and Carnot's Engine
Chapter 1: Recap of First Law of Thermodynamics and Macroscopic State Properties [00:00:00]
Professor Ramamurti Shankar:
What I did yesterday, or Monday, was to describe to you the First Law of thermodynamics. So, let me remind you what the context was. We're going to study a system, that's our thermodynamic system, and for all our purposes you can imagine that to be some amount of ideal gas trapped inside this piston and cylinder combination. We put some weights or maybe some sand on top to keep the piston where we want it. The gas has a certain pressure and a certain volume and we represent that by a point in this diagram. That defines the state. That's called the state of the gas.
On a microscopic level, the state is very complicated, right? There are 1023 atoms or molecules zipping around. We're not interested in such detailed properties. We want to look at bulk macroscopic properties of which pressure and volume is a complete pair. That's all you need. I think I reminded you that you don't need a third axis for temperature because we have this equation
PV = nRT
. So, if you know P and V, you don't need temperature as another variable. That's called the equation of state. You can use this all the time. Whenever the gas has got a pressure and volume, feel free to use
PV = nRT
.
Alright, so here's the gas. And then I want to change its state, and I explained to you that unlike particles whose state can change as fast as you like, you cannot change the state of a gas abruptly because if you take half the weight off the top, the piston will fly off; there will be a period when the gas is not in equilibrium. Different parts of it will have different densities, different pressure. You cannot represent that complicated state as a point in this plane. So, what we want to do is to make changes which are slow enough for us to follow. So, one way to do that is to take one grain of sand. Take one grain of sand, then you lower the pressure a little bit, the piston will move up a little bit. Move up means what? Bigger volume, lower pressure, the gas will come there and then you can take off another grain and by making the grain smaller and smaller, you can make these dots closer and closer. It's going to take you a long time but in principle you can make the gas move on some path. That is a thermodynamic process.
This process is always near equilibrium. You never deviate too much from equilibrium, and it's called a quasi-static; that means not quite static, but as slow as you like, and it is called reversible. Reversible means that you can also go right back to where you came. If you took a grain out, piston expands. You put the grain back, piston contracts. So, you can go down this way or you can go up this way. I've just chosen to, let's say, go down like this.
When that happens, we want to say the following thing about the state of the gas before and after. At every point in the
PV
diagram, the gas has something called the internal energy. The characteristic of internal energy is it's called a state variable. And this is a very important concept. A sate variable depends on where you are in the
PV
diagram, what your state is. It does not depend on the history; it does not depend on all the things the gas has gone through in its life. If you tell me you are here, then we may associate with that point an energy that doesn't look into the history of that gas. That energy is nothing other than the kinetic energy. You'll remember that it's 3/2
kT
per atom,
N
atoms, that's the internal energy. You can also write this as 3/2
nRT
. If you count the molecules then use Boltzmann constant, or you count the number of moles then use the gas constant. It's the same thing. But
nRT
is
PV
, so if you like, you can also write it this way. That shows you very clearly the internal energy is uniquely determined by
PV
, and
P
and
V
determine the product
PV
. So, at each point in this diagram, the gas is a certain energy. But energy is simply that ½
mv2
for each molecule. You add it all up, that's the total energy. Okay, so we can write it many different ways.
Now, the First Law of Thermodynamics asks the following question. If I want to change the energy of this gas, how can I do it? There are two ways to change the energy of the gas, and the total change in
U
, meaning
U
at the end minus
U
at the beginning, where these are two nearby points, is either the heat input minus the work done by the gas--Let me write it as capital
PdV
. Sometimes you write it as
ΔQ - ΔW
. That's the First Law. So, you have to take some time to understand what it says.
Notice from this formula here, the energy of an ideal gas, and only an ideal gas because that's the only thing we are going to talk about, is a function only of temperature. If you know the temperature of the gas, you know the kinetic energy of the molecule, so if the number is constant, the energy is determined. The energy depends only on the temperature for an ideal gas. So basically, when I say how can I change the energy of the gas, I'm asking how can I raise the temperature?
One obvious way is this. Put it on a hotplate which is slightly hotter than the gas. Then the heat will flow from the hotplate to the gas. That's called heating up the gas. There you don't see anything happening, right? It's occurring at a molecular level. The molecules in the hotplate are, on average, moving faster than the molecules in the gas and during the collision; kinetic energy will be transferred from the hotplate to the gas. That invisible flow people used to think of as the caloric fluid, but now we know it's just molecular kinetic energy transferred from the molecules in the plate to molecules in the gas. That's this guy. This
ΔW
, the plus sign of the
W
is the work done by the gas, and minus of that is the work done on the gas. And that means if you want to increase the temperature of the gas, you're also told you can do the following. Push down on the piston. If you push down on the piston, you are reducing the volume.
ΔV
is negative, minus
PΔV
is positive, and that'll also increase the energy of the gas. Or, if you take a grain of sand out, and the piston moves upwards, the gas works against the environment and it pays for it through its internal energy because then
PΔV
will be positive and this thing will be a negative contribution of the internal energy. So, there are two ways to change the energy of the gas. One is a way you can actually see by moving up and down the piston. You can see somebody moving it. It's a macroscopic motion of something you can see. That's called the work done on the gas. Other one is energy transferred at a molecular or microscopic level, which is what we call heat.
And the First Law says the total change in the internal energy is the sum of two numbers. First one is the heat input and the second one is the work done. So, what I did for you last time was a practice calculation in which I took a gas here, went along an isotherm. That means temperature is a constant. That's the meaning of the isotherm. And I want to go from some initial point to some final point. So, this volume
V1
and pressure
P1
. This is
P2
and
V2
, and I want to find the work done by the gas during this expansion. Well,
P
times
ΔV
, you can see, is really that shaded area here because it's a rectangle of height
P
and width
ΔV
. So,
PΔV
is just the area under the graph that you follow. So, the work done, the sum of all the infinitesimal works, is the pressure as a function of volume times
dV
from the starting volume for the ending volume. What is
P
as a function of
V
at a constant temperature is
nRT
over
V
? Now, I'm using the factor at every point
PV
is
nRT
, so
P
is
nRT
over
V
, and this is a logarithm and we all know how to do the integral, as log of the upper limit minus log of the lower limit. So, that's the first successful calculation of work done.
You can take the gas on any path you like, you know. As long as you knew the pressure at each volume, you integrated the function from the left limit to the right limit; that's the work done. For isothermal process, it's particularly easy because the pressure is inversely proportional to volume, and you do that integral. This is the work done. For example, if the gas expands to double the volume at temperature 300 Kelvin, the work done is number of moles, gas constant, 300 log of 2. Multiply all those things; that's the work done by the gas.
If that is the work done by the gas, we can also say the following. The internal energy change is zero. Right? That's the trick question I told you to watch out for. If you're going at constant temperature, you don't change the internal energy. So, if the change in internal energy is zero, it follows at every step,
ΔQ =ΔW
. This quantity we call
ΔW
. Therefore, the work done by the gas is also equal to the total heat input of the gas. We indicate that by drawing a little arrow like this; it's just the way we like to show that heat flows into the gas.
Do you understand physically what's happening? You take this gas, you keep it on a reservoir at temperature
T1
[
T1
is just
T
]. It's stuck at that temperature. If you take a grain of sand, gas is expanding. Normally, when the gas expands, it does work and if energy will go down, it'll cool down. But you're not letting it cool down because you're pumping in heat from below, maintaining at that temperature. So, this process you should visualize as a piston with some weights sitting on a plate at temperature
T1
. You take off a grain of sand, it moves up a little bit but you don't let it cool down because you send in heat from below, maintaining it at that temperature.
For example, you got this computer air, right? You blow air on your keyboard to blow off the dust. You know, when you blow the air out, the can cools down. It cools down because the compressed air is working against the atmosphere as it comes out and, therefore, it loses internal energy and it cools down. That's because you're not giving it enough time to absorb heat from the room. If you let the air out slow enough so that in the process of expansion it tries to cool down but the room pumps some more heat, then, of course, the can will not cool down. But, you know, that's not the purpose of buying canned air. You don't want to buy canned air so you can release it at room temperature. You don't care if it cools down; you just want the gas to come out really fast. So, if you don't allow heat to come in, an expanding gas will cool down. Okay, that's also why the universe cools down. Process of expansion.
Alright. So, here's a simple problem where you can do many things. You can find the change in energy from start to finish. Zero. Work done you find by integrating
PdV
and the heat input is equal to work done because there's no change in energy. This is all the stuff I did last time. I also did a couple of other topics. I'll just remind you what they are.
Chapter 2: Defining Specific Heats at Constant Pressure and Volume ( Cp, Cv ) [00:13:22]
I said we can define a specific heat for a gas. Now normally, specific heat is the number of calories to raise one gram or one kilogram by one degree. But for a gas, what matters is not the number of grams but number of moles. You have already seen it here. The energy of the gas is not proportional to the grams of gas you have but to the number of atoms you have or the number of moles you have. So, we define specific heat to be the heat needed to produce a certain temperature change for one mole. We take a mole of gas and you heat the guy and you see how many calories do I need to get an increase of one degree. But that turns out to be insufficient. This derivative does not have a unique value. Can someone tell me why it's not sufficient information? You remember from last time? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: In other words, when I take a solid and I say find the specific heat, take one gram of solid, pump in some heat so the temperature goes up by one degree, keep track of the calories. You are done. For a gas, it turns out if you took this gas in the cylinder and you pump in some calories, it's going to try to heat up and when it tries to heat up, it may also expand. When it's expanding, then some of the energy that you pump in the form of heat, some of it's turning into work to push the piston out. The part that goes through the internal energy, the part that really heats up the gas, is now less because you put in some heat from below, you lose some heat to the expansion, so what goes in to change the internal energy, which is what controlled the temperature, is less than the heat you put in. So, if the gas expands during the heating process, there's a certain energy lost due to work you have to take into account.
On the other hand, another person can do the same experiment of the gas but put a pin here so the piston cannot move. Then, of course, it cannot do any work and all the heat you put in goes into internal energy. That gas will heat up more readily. For a solid, we don't worry about it because the expansion of a solid is such a tiny fraction of its volume when the temperature changes that the fact that a chunk of copper, when you heat it, is also expanding against the universe, against the atmospheric pressure, is a negligible effect. The
ΔV
is so small for a solid we ignore it. For a gas it's very important.
Therefore, for a gas there are two kinds of specific heat. In fact, you can define many definitions. The two common ones are
CV
, which is
ΔQ
over
ΔT
at constant volume, and that's how you denote that in calculus [pointing to the equation]. The other one is
CP
, which is
ΔQ
over
ΔT
at constant pressure. So, let me derive one more time these two specific heats because it's worth going over this again and again.
The key to all of this is the First Law. The First Law, written after transposition, looks like this. Let's put
ΔQ
on one side and the other stuff on the right-hand side. In the first case, at constant volume, there is no
PΔV
term because
ΔV
is zero. Therefore,
ΔQ
/
ΔT
=
ΔU
/
ΔT
, and for one mole, you remember
U
is 3/2
nRT
but
n
is 1, for one mole. So,
dU/d
T is a simple derivative of this function with respect to
T,
which is 3/2
R
.
What do you notice about this formula? It's the specific heat of one mole of a gas doesn't depend on what the gas is. As long as it's a monoatomic gas, it doesn't matter what the mono atom is. It could be hydrogen, it could be helium; it doesn't matter. That's why we like to think about the molar-specific heat or specific heat per mole. You get an answer that's universal. If you took specific heat for a gram, then one gram of hydrogen and one gram of helium won't have the same specific heat because they don't have the same number of atoms. But if you count in moles, the beauty of the formula is this number is true for all ideal gases, whereas if you took the specific heat of copper or silver or iron, it varies from material to material. Specific heat of ideal gases is very simple. You don't need to look at a table. Here's the answer for all ideal gases. It's very important it's a monoatomic gas, which is a point-like atom which only moves but doesn't have any internal structure so it can spin and rotate and vibrate. If it can do that, there are other contributions to energy, but we're not going there.
Now, let's calculate
CP
.
CP
is
ΔQ
over
ΔT
at constant pressure. So now, you cannot ignore this term. So,
ΔU
, from what I did before, will be
Cv
times
ΔT
, plus there is a new term.
PΔV
is
Δ
of
PV
because
P
is constant. If
P
is a constant, the change in
PV
is the same as
P
times change in
V
. But
PV = RT
, so if
Cv
ΔT
plus
RΔT
. If you divide every side by
ΔT
and take
ΔQ
over
ΔT
, then
CP
will be
Cv
plus
R
and that's a very famous formula.
And you should understand why specific heat at constant pressure is more than specific heat at constant volume. Think about that. If the gas is stuck at a given volume, it's easier to heat it up because all the heat goes into internal energy. If it is at constant pressure, you're letting the piston move up and some of the heat is being paid to move the piston, only the rest is going to change the internal energy. That's why
CP
is always bigger than
Cv
, and for an ideal gas,
CP
is
Cv
plus
R
and this number,
γ
, is defined as
CP
over
Cv
. This is always the definition of
γ
, where there is an ideal gas or not. For an ideal gas, we can calculate
Cp
over
Cv
, which is 3/2
R
plus another
R
, divided by 3 /2
R
, which is 5 over 3. So, γ is not always 5 over 3. You should be aware of that. But for ideal gas,
γ
is 5 over 3. So, this is a review of what I did last time, but I'm very eager that you guys should be on top of this and it's worth doing it one more time.
But now, I'm going to consider some more processes where I want to find work done. So, maybe I'll start fresh here. Let's take the following process. I start here. I go on an isothermal here [pointing at graph], then I go backwards at constant pressure until I'm right below this point, then I go straight up. You can ask, "What is the work done in this process?" The work done in the curvy part of it is all of this. That's in the part
AB
. In the part
BC
, work done is the area of this rectangle but it's counted as negative, because a gas is being compressed. Or, if you like, it's at some constant pressure but the change in volume is negative for every step. So, even though the work done is said to be the area, you've got to keep track of sign. If you're compressing the gas,
PΔV
is negative. Therefore, in the part
BC
, we must take away the shaded region and
CA
, no work is done because volume is not changing. Area under the vertical line is zero. So, you can see that in this full cycle, when I go from
A
to
B
to
C
back to
A
, the work done is the area enclosed by the loop in the
PV
plane.
That's a very useful result. We say the work done in a cycle, there's a symbol we like to use. This curly thing on the integral means taken around a closed loop. But you guys have to be little careful when you write this, because somebody else can do the following thing to gas, do exactly the opposite. Come down like this, go down like this, and go down like that. Go up like that. The opposite way. In this case, the work done is considered positive because the part of it,
AB
, is taller than the
BC
at point
Y
, so the net work is positive. Here, it's the same amount of work but the net work is negative. So, you've got to be careful that you describe the sense in which you do the loop. So, the same loop, as a geometrical figure, as the same area, but the work done by the gas is positive in this case and negative in this case, and you can use common sense to find out if it's positive or negative. But here is another very interesting result. Let's go to the full cycle and ask, "What's the change in U?" Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: Right. His answer was
PV
is the same. And more generally, even if it's not an ideal gas, it's a gas made up of whatever you like. It's any system. If you return the system back to the same state, the internal energy returns to that value. That's what I meant by internal energy doesn't depend on the history of the gas. For example, you can take the cylinder, you leave it alone, I measure the energy, I go outside the room and come back. In the meantime, you took it on a loop and brought it back. I will not know, and I don't care because as far as I'm concerned, if
P
and
V
are back to where they are; the gas is back to where it is; energy is back to where it is. So, the change in the internal energy is zero. That means the work done and the heat input are the same. So, let's be very clear. If you guys do problems, I don't want you to lose points for sign mistake.
W
is always the work done and
Q
is always the heat into the gas.
So, this is a gas here which has done some work and some heat that's been put into the gas, and the two have to be equal because the energy doesn't change in the end. Now, that leads to a very, very subtle and interesting point. There is a very clear notion of what is the energy in the gas. There's a unique answer. There's no notion of what is the heat in the gas. You look at a gas and you cannot say this is the heat in the gas. That makes no sense. Try to understand why. Because if you say there's some amount of heat in the gas, okay, whatever you want, some number, I do the cycle and I come back to exactly where I am. I'll put in some amount of heat
Q
, which is non-zero. So, if there's anything called the heat in the gas, it has changed by an amount of
Q
. That's why there's no notion of heat in the gas or work in the gas. There's only energy in the gas. A state variable returns to its original value and when you go on closed loop, the change should add up to zero. That's not true for work, that's not true for heat, but it's true for the difference. That defines an internal state variable.
Chapter 3: Adiabatic Processes [00:26:01]
Okay, now I'm going to consider a new process which is of special importance. So, the processes I've considered so far are isothermal, at constant pressure is called isobaric, and I don't know the name for constant volume, but no work is done at constant volume. Now, I'm going to consider the last process very, very important. It's called adiabatic. Adiabatic process is in which the gas changes its volume but it's completely thermally isolated, so
ΔQ
is zero. You wrap this guy in a blanket and you do things to it. No heat can flow into the gas or out of the gas. That's called an adiabatic process. Isothermal is quite different. Isothermal, you keep it on a hotplate at a given temperature and as the volume changes, say as the volume increases, heat comes in from below. Or, when you compress it and you don't want it to heat up, heat is rejected below. But this is not the case here. In an adiabatic process, if you let the gas expand you thermally isolate it from everything. So, you should think about what'll happen to a gas if I start here. That's what isothermal is. What do you think will happen? So, let's draw a few isotherms. This is temperature, say
T
= 300. This is
T
equal to what? More than 300 or less than 300?
Student:
Less.
Professor Ramamurti Shankar
: Less. And why do I say less? You take any point here; it's got the same volume but lower pressure, so
P
times
V
is less. So, this may be
T
= 200. If I start here, now I let the gas expand adiabatically. That means I pull out the grains of sand, the gas expands against the atmosphere, but no heat is allowed to come in. Think about what that means. Gas is pushing the piston. Gas is doing some work. It'll pay for it through its own internal energy. Internal energy will go down and that means temperature will go down. So, what you will be doing is you'll be cascading down from one isotherm to another, plummeting down in temperature until you come and stop somewhere at the lower temperature. So, an adiabatic process will cross from one isotherm to the next to the next to the next, changing temperature.
Another way to say this is that the drop in pressure for a given drop in increase in volume, it would be more precipitous for adiabatic because it's expanding but there's no energy coming into the form of heat so pressure drops more precipitously. So, it won't be
PV
equal to constant, and the question is, "What is it?" What is the equation for an adiabatic process? What is
P
as the function of
V
? That's what we want to ask now.
So, whenever you have any such question in thermodynamics, up to this point the only law we know is the First Law of Thermodynamics. So, you have to go back to that. So far, I've driven home the point that every question asked in mechanics can be traced back to Newton's Law. There are no new laws. But when you come to thermodynamics and you study heat and temperature, there is new stuff and the First Law of Thermodynamics is called a law, because there is no way you can derive it from Newtonian laws. It's a new concept. So, let's ask what is
P
as a function of
V
, given that
ΔQ
= 0? So, what's our strategy going to be? How would you even begin this? Do you have some idea of what you might do? This is a tough question so even if you give a wrong answer, that's fine. How do I calculate the relation of
P
to
V
given that
ΔQ
= 0? Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: Okay. Let me write down everything he said. When I said
ΔQ
= 0, your first reaction has to go back to the First Law and write
ΔQ
as
ΔU + PΔV
, and set that equal to zero. But
ΔU
is
Cv
times
ΔT
, plus
PΔV
is zero. By the way,
ΔU
is
Cv ΔT
for one mole. I'm going to consider one mole of gas. Now, this is another thing you people should understand. The way in which pressure falls for temperature is going to be the same, whether I consider one mole or two moles or ten moles. The rate at which it changes will not be dependent on how many moles I took, so if you want you can take
n
moles and put an
n
here. You'll find everywhere an
n
will come and cancel out. Now,
P
is
nRT
over
V
. So, maybe I'll do it this way for you guys. If you want, put an
n
back there, but you will find
n
cancels part of the equation because
nCv ΔT
, plus
nRT ΔV
over
V
equals zero; so the answer doesn't depend on how many moles you took. So, I will take one mole for my calculation.
Think about what this says. Divide everything by
T
. You get
Cv
over
RΔT
over
T
plus
ΔV
over
V
is zero. This is telling you that as you change your volume and you're coming down this graph of adiabatic expansion, when you go from there to there, there's a change in temperature such that the change in temperature by the temperature, plus the change in volume divided by the volume, should add up to zero. That is a condition of no heat flow. So, it relates a change in
T
to a change in
V
. What I would have ideally liked is a change in
P
due to a change in
V
, but what comes more naturally is a change in
T
over a change in
V
. But let's worry about that later, because we've got
PV = RT
. We can always swap the temperature for pressure in the end. So, let's just take this definition. So, every change, remember now, you understand you go from one point to the neighboring point; there's a plunge in temperature. That's why
ΔT
will be negative and
Δ
will be positive and these numbers will, of course, cancel.
Now, let's add all the changes. Let's call it doing the integral. Do the integral of that from start to finish, do the integral of that from start to finish, and that integral of zero is just zero. So, this tells me
Cv
over
R
times log of
T2
over
T1
, plus log of
V2
over
V1
is zero. Now, you've got to go back and think about your logarithms and realize--and I can write it as log of
T2
over
T1
raised to the power
Cv
over
R
, times
V2
over
V1
is equal to zero. We just combine all the logarithms and realize the log of
X
to the power
n
is
n
log
X
. So, that is the same as this. Now, the log of something is zero means that something is 1, because log of 1 is zero. So, we rewrite the final expression I got up there by saying
T2
over
T1
raised to
Cv
over
R
times
V2
over
V1
is equal to 1. And we usually write it as follows. We say
T2
raised to the
Cv
over
R
,
V2
to the power of 1 is
T1
raised to the
Cv
. I'm sorry,
T1
raised to
Cv
over
R
times
V1
. So, this is the relation between the temperature and the volume. Yes?
Student:
[inaudible]
Professor Ramamurti Shankar
: You could do that. That's correct. You could write down three-halves if you like. At the moment, I'm trying to keep it general. If it was a gas for which
Cv
was not three-halves
R
, all of this would still be true. But he is quite right. For an ideal monoatomic gas,
Cv
over
R
would be just 3 over 2. So, what it's telling you is that when the gas expands, the temperature falls. I already told you that. It's telling exactly how it falls. It tells you that
T
to some strange power times
V
is constant during the process. Now, if you want to know what happens to the pressure, you can do the following. You remember
PV = RT
. There are many ways to write this. I'm going to write it in another way and you guys see if you can follow this.
T2V2
to the power
R
over
Cv
is equal to
T1V1
to the power
R
over
Cv
. You believe that? That's just a mathematical trick. If that is true, this is true. You know how I went from here to here? How did I go from here to here? Do you have an idea?
Student:
You take
R
over
Cv
to the power of [inaudible]
Professor Ramamurti Shankar
: Exactly. Raise both sides to the power
R
over
Cv
. It's cooked up so that
Cv
over
R
goes away and
R
over
Cv
falls on
V2
. There is another way to write it, if you like. I'll tell you why I write it this way. Because
T2
is just
P2V2
. But let me combine that one
V2
with this and write the one plus
R
over
Cv
. Then, I can show it as
P1V1
to the power 1 plus
R
over
Cv
. You may object that
PV
is not
T
but is
RT
, but
R
will cancel so I didn't bother with that. And this--don't draw the box around this yet. I will write it in a way that's very, very standard and if you remember in your high school days, you may remember is written as
P2V2
to the
γ
, is equal to
P1V1
to the
γ
, but
γ
is just 1 plus
R
over
Cv
, which you can see is equal to
Cv
plus
R
over
Cv
and that is
CP
over
Cv
. So, this
γ
is really
CP
over
Cv
. For an adiabatic process,
P2V2
to the
γ
is
P1V1
to the
γ
. That's one way to write it, but I will also expect you to know that you can also write it in terms of temperature, as temperature times volume raised to a strange power is equal to a constant, before and after. Any questions? So, what we have done is found pressure as the function of volume on an adiabatic curve.
So, I'm now going to do one last ingredient for the rest of the stuff, which is the following. I'm going to calculate the work done in an adiabatic process from here to here. This is one, this is two. This is not an isothermal, which looks like that, it's an adiabatic process. What's the work done in adiabatic process? So, let's calculate that. Work done is equal to integral
P(v)dV
. But remember,
PV
to the
γ
is a constant. Do you guys understand the relation of writing
PV
to the
γ
equal to constant? It's the same as saying
P1V1
to the
γ
is
P2V2
to the
γ
. That means you can pick any point on the path and
P
at that point times
V
at that point to the power of
γ
will be a fixed number. That number is
C
. In other words, this
C
can be
P1V1
to the
γ
if you like, or
P2V2
to the
γ
if you like or
P3V3
to the
γ
if
3
is another point on this trajectory. It's convenient to call that invariant product of
PV
raised to
γ
as
C
. Because then we can do the integral as
dV
over
V
to the
γ
with a constant
C
here from
V1
to
V2
.
And this is a pretty simple integral. You guys know that the
x
to the
n
integral is
x
to the
n
plus 1 over
n
plus 1, such that
V
to the
γ
minus 1, over
γ
minus 1. Because this is really
V
to the minus
γ
. Now, did I get it wrong here? I think I got it wrong. Sorry. It's 1 minus
γ
, 1 minus
γ
, over 1 minus
γ
. Because
V
to the minus
γ dV
, is equal to
V
to the minus
γ
plus 1 over minus
γ
plus 1. Right?
x
to the
n
integral is
X
to the
n
plus 1 over
n
plus 1,
n
happens to be minus
γ
here.
Okay, now watch this. This constant I said can be written as any of these numbers, but let me write when it multiplies this; let me write as
P2V2
to the
γ
. Can you see what happens if I do that? Try to do this in your head.
C
multiplies all of this. When
C
multiplies this guy, let me write the constant as
P2V2
to the
γ
; that gives me a
P2
,
V2
to the
γ
combines with
V2
to the one minus
γ
, to give me just
V2
. Likewise,
C
multiplying this one, when the same
C
multiplies this, let's write
C
as
P1V1
to the
γ
, and we'll find there's that. And people like to rewrite this by changing the sign everywhere as
P1V1
minus
P2V2
over
γ
minus 1, because
γ
minus 1 is the positive quantity. So, this is the work done in an adiabatic process.
So, what's been going on? Let's think about what I've been doing. I told you that there is a new process called adiabatic, a really important process, in which the system is not allowed to exchange heat with the outside world.
ΔQ
= 0 is a condition relating
ΔU
and
PΔV
. And the changes are correlated and the effect of adding up all the changes, namely doing the integral, is this one, namely temperature to the
Cv
over
R
times
V2
does not change along the path. So, if you take any two points, that combination of temperature and volume doesn't change. Then, since
PV
equal to essentially
T
, you can also write it as pressure times volume to the power of
γ
doesn't change. So, I'm saying you can call all of that equal to some constant
C
. The
C
is not a universal constant, like velocity of light. For a given gas, on a given experiment, it does not change as it goes through adiabatic expansion. So, don't think of it as a universal constant. On the trajectory, on the adiabatic curve, it's a constant. It's like saying kinetic energy plus potential energy is a constant. It's not a constant you can look up in a book. It depends on what your particle is doing. But for that particle in those conditions, kinetic with potential adds to a particular constant we call total energy. Likewise,
PV
to the
γ
is a constant for this particular gas.
Chapter 4: The Second Law of Thermodynamics and the Concept of Entropy [00:43:57]
Okay, so all this is actually a preparation for something else. And that's what we are going to discuss now. So, between now and the end of this course we are going to discuss the Second Law of Thermodynamics. So, we have done all we want to do with the First Law. So, you guys should be able to be given various graphs on the
PV
plane, find the work done in going from here to there, find the change in internal energy, find the heat added and so on. I hope you can do such problems, but they're all going to be one of these formulas. Say there's going to be adiabatic or constant pressure or constant temperature, so you just plug the numbers in, keep track of the signs by using common sense.
Alright. So now, we come to the last part of thermodynamics, which is to me one of the most beautiful parts of thermodynamics, which starts out with asking the following question. There are certain things in this world that are perfectly allowed but don't seem to happen. Let's take many examples. Take the Joule experiment. You take a cylinder of water with a paddle that can spin and you put some weight around the pulley and the weight goes down. Paddle spins; the water heats up. You take a movie of that, and the movie is so fine it can even catch individual molecules. Now, you play the movie backwards. So, you watch the movie being played back and what do you find? Suddenly, the weight starts moving up, paddle spins the other way, and the water cools down. This is not in violation of any of the laws you have learned including the First Law of Thermodynamics, because when the weight went down and the water heated up, some amount of work was done on the water, and the energy of the water went up. In the reverse process, the energy of the water went down and instead the weight went up, so work was done by the system. But that doesn't seem to happen. If the weight comes down you can wait all day.
Well, let me give you another example. Take a chunk of wood, you slide it there. Sorry. It was not a piece of wood and it didn't stop. See, this is why I don't do demonstrations because even the simplest demonstration I have done doesn't work. So, that's why some of us become theoretical physicists. I did a demonstration where some trolley is supposed to shoot a little marble. All the marble had to do was come down and even that didn't work, so I don't do demonstrations. Well, let's try this. Here's an eraser, and give it a push and it stops. Take the movie of that. Play it backwards. You will find suddenly, you know the table heats up a little bit due to friction. The table can cool down and the eraser can move backwards picking up speed [laughter]. Right. So, why did we laugh? You have no reason to laugh right now because it doesn't violate anything you have learned, other than your daily experience, because in the reverse process every atom, you know, every atomic thing on the desk that started moving, is made to stop, turn around, and move in the backwards direction. And every collision between atoms on the desk and atoms on the eraser will obey all the laws of mechanics.
For example, if you have a planet going around the Sun, if you stop the planet and you reverse the velocity, it will go the opposite way and the opposite motion is in complete accord with Newton's laws. In fact, there may be somewhere a solar system where the planet actually goes the other way. It doesn't violate anything. So, in all the movies which are played backwards, at the very microscopic level there's nothing that says it cannot happen, and yet it does not happen.
Here's another thing that does not happen. I take a box and I put some gas molecules on one side and there's a partition holding them in that side. Then I remove this partition and I wait a little bit; then I know the gas fills up. That's like perfume leaking out of the bottle. Now, take a movie of these molecules. When they go from here to here, and play the movie backwards--What'll happen when you play the movie backwards? Let's say this guy was moving like this the instant we played the movie back. Well, in the backwards movie it started going the other way and slowly the whole thing will untangle itself and end up here. That also will not happen. We all know that if you go to a room and you release some gas from one side, it can fill the room but it's not ever going to come back, and yet it doesn't violate any laws because if I made a movie and played it backwards, in every microscopic interaction between molecules, there'll be no violation of any of the laws of nature. But that doesn't happen.
Here's another thing that doesn't happen. I take a chunk of some hot copper and I take a chunk of some cold copper. Hot, cold. I just put them on top of each other, come back in an hour, it's become, say, lukewarm. That's fine. But now maybe, if I wait long enough, the lukewarm will automatically spontaneously separate into hot and cold. That doesn't seem to happen. The heat simply seems to flow from hot to cold but never back from cold to hot. But flowing from cold to hot will not violate the Law of Conservation of Energy. As long as the same number of calories go from cold to hot, it doesn't violate anything. And that doesn't seem to happen.
So, this can go on and on and on with some large number of things that are allowed but don't happen. So, we cannot explain them with any known laws of physics so we elevate that to a new law. The new law will say these things cannot happen. But you don't have a law that says these things cannot happen, right? That's not a good enough law. You've got to say what things cannot happen. I've got a list a mile long. Hot and cold, when mixed, will never separate back into hot and cold. A gas, that genie that got out of the bottle, won't go back, there's gas that came out won't go back. There's a whole lot of processes which we call irreversible. They never seem to happen backwards. They only happen forwards, and we cannot list all of them. So, you wonder if there's any law--see, anytime you cannot explain something from prior things, you elevate that to a law. But you like an economical law. You would not like a law that says the following million things cannot happen. And it's really amazing that there is one law, a single law, that not only is qualitative, but is quantitative, that tells you exactly when some things can happen and when some things cannot happen, and according to the one single law, all the things that we say don't happen won't happen. Will be forbidden by the law, and that's a Second law of Thermodynamics, but what form does it take?
Well, we will see it introduces a certain quantity called entropy, about which let's say right now we don't know anything, and the law will simply say the entropy of the universe will always increase. You don't have to write it down now. I'm going to define the concept. It'll arise naturally from more thinking. The one law that entropy will always increase, in the universe as a whole, is enough to forbid any of these forbidden processes. In other words, if the paddle spun the other way and the weight went up and the water cooled down, you can show the entropy of the universe would have actually gone down. That's why that's not allowed. If you drop a piece of egg, it comes and splatters all over the floor. If it rejoined and rose back to your hand, it won't violate any other principle other than the law of entropy, because the shattered egg has more entropy than the egg that comes back to your hand. And if hot and cold mix to become lukewarm, you can show the entropy goes up this way, but if you went the other way, entropy will go down and that's now allowed. So, one great law will take care of all these things. So, you've got to ask yourself, "What is the one great law and how do we get to it?"
Well, it turns out this great law was discovered by an engineer called Carnot. So, here is another thing. People don't wake up and say, "I'm going to discover a great law." People just go out and do their business and all you need is have enough sense to realize when you've stumbled on something really great. So, Carnot had a very practical question. Carnot was working on engines. At the time they were working on something like the steam engine. So, a steam engine--You know what happens in a steam engine. You take some coal, you set fire to it, then you boil some water, it turns into steam, then the steam pushes the pistons and the wheels turn and the train goes forward and that's your steam engine.
What happens in a steam engine we can schematically as follows. There is a hot reservoir
T1
that's the furnace of your steam engine. Then, you have an engine in which you've got some steam. You've got some water that's going to be boiled and it's going to boil only because you take in some heat. Here's my engine, it's got some substance inside, it could be a gasoline engine or a steam engine, we don't care what happens. Some amount of heat
Q1
is taken from a hot reservoir and some amount of work is delivered. Now, here is an engine which, as drawn here, doesn't violate any of the laws of physics, provided
Q1 = W
, then energy is conserved. In practice you find that's not how engines work. The engine also rejects some amount of heat
Q2
to a lower temperature
T2
.
The lower temperature, if you look at a steam engine--if you've gone--Have you guys seen a steam engine? Okay, if you really go see a steam engine you will find there's a lot of hot steam coming out of the back or in a car, you've got exhaust gases coming out. That's the hot gas emitted at atmospheric temperature. Inside the engine is a very hot place. So, the car emits some heat at a lower temperature. The steam engine emits some steam at a lower temperature. So, the work that you can get is really
Q1 - Q2
is what you can get. At least in this engine, you get
Q1
and
-Q2
. So, we define a quantity called efficiency
η
. It's called the efficiency. It's what you get divided by what you pay for. You pay for burning the coal and you get the work out. The work is, of course, the thing that makes the engine move forward. Turns into kinetic energy of the locomotive. That, then, you can see is
Q1 - Q2
. What you get divided by what you pay for, you can write it as 1 minus
Q2
over
Q1
.
So, in every engine, some heat is taken in. Some of it is converted to work and some of it is rejected. To the extent heat is rejected, the efficiency is less than 1, because Q2 minus--over Q1 and is subtracted from 1. So, you can ask yourself why not build an engine in which you just don't reject any heat downstairs? Why not take all the heat and convert it to work? So, Carnot gave a great argument on the most efficient engine you can build. In other words, there is an upper limit to the efficiency and it's not 1. So, what is it and how are you going to find out? Well, he's going to find out what it is, but he also needs a postulate. Carnot's postulate is the old version of the Second Law of Thermodynamics. He didn't talk about entropy. You can show in the end they're all equivalent, but Carnot's law, which is his own version of the Second Law, which says the following.
So, Law 2 according to Carnot. Let me just draw a figure; then, we'll say
T1
is not allowed. Carnot says you cannot build an engine whose sole effect at the end of the day is to transfer some heat from a cold body to a hot body, whose sole effect--that's very, very important. You cannot have a process whose sole effect is this. I mean, I don't feel like writing what this is. It's what the picture says. All right, it doesn't take a genius to have the heat flow the other way. You understand? If you want heat to flow from a hot body to a cold body, that's trivial. Just connect them with a metal rod and it'll flow. The sole effect of that is transfer of heat from hot to cold. That's the way of the natural order of things, but Carnot is saying you can never build a set of gears and wheels and teeth and whatever you like so that at the end of the day, all that has happened is heat has flowed from cold to hot. That is going to be taken as a postulate, and people are willing to take that as a reasonable postulate, and we want to see what we can get out of that postulate.
It turns out it is that postulate that's going to control the efficiency of heat engines, put a bound on the efficiency of heat engines. So, don't deduce this. This is a law. Now, you might say, well, this is how the law began, and the law assumed more and more sophisticated forms, so Carnot was not thinking entropy. That came later, but his postulate was, please grant me this, which seems to be a fact in nature. Then from that let me talk about heat engines and show you that there is an upper limit to the efficiency of an engine.
In particular, the upper limit is not 1. It's clear to everybody that the limit cannot be more than 1. If it's more than 1, you are taking some amount of heat and giving even more amount of work delivered. That violates the First Law of Thermodynamics. Conservation of energy. But the fact that you must necessarily reject some heat, which you cannot use in this experiment, is the content of Carnot's result.
So, here is the engine that Carnot built. This is called a Carnot engine. By the way, look, don't rely on my graphics. I mean, you have to go look at just about any book you can find on the market. It'll talk about Carnot engines. So, I'm here to merely tell you the words and not the pictures. So, Carnot's engine is like this. Take two isothermals,
T1
and
T2
. You remember the adiabatic curves are much steeper. Draw two adiabatic curves like that. Then take a gas from
A
to
B
to
C
to
D
and back to
A
. That was the Carnot engine. So, let's see what we are doing. In the process
AB
, take the piston with the gas in it; slowly lift the grains of sand so it expands to a volume
B
at the same temperature. Then having reached
B
, you thermally isolate the gas. It's not on top of a reservoir of temperature
T1
. It's completely isolated. Take out even more grains of sand. Now, it's expanding without any energy coming in. It cools down to
T2
. This is the point
C
. Now, you put the grains of sand back, but it's still on a hot reservoir at
T2
. I mean, the cold reservoir of
T2
. Put the grains of sand back, temperature is locked in at
T2
until you come here. Then, you isolate the gas and put more grains of sand back until you come back to
A
. Obviously, such a path exists because of the way isothermals and adiabatics are in the
PV
plane. That's the Carnot cycle, and the important part of the Carnot cycle is that it's reversible.
It's reversible because at every stage, when you took a grain of sand out you can put it back and you can run it backwards. So, it can also run backwards. The Carnot engine looks like this. Here is the engine, it takes some heat
Q1
from a reservoir of
T1
that delivers some work
W
; it rejects some heat
Q2
, of temperature
T2
. This is the model of a steam engine. Suppose you run the Carnot engine backwards. By the way, the work done by the Carnot engine is this shaded region here and it absorbs heat in the stage
AB
. It doesn't have any heat absorption in the state
BC
because it's adiabatic. In
CD
, it rejects some heat and
DA
again, there's no heat transfer. So, heat comes in here,
Q1
, heat is rejected here,
Q2
.
If you run the Carnot engine backwards, let me show you what it looks like. Everything is backwards in a Carnot engine if you run it the other way. Some work is put in here, some heat
Q2
is taken from the lower reservoir and the heat
Q1
is delivered to the upper reservoir. You know what that gadget is. That's a refrigerator. So, in a refrigerator, that's what happens. You might say hey, you violated the Second Law. You have transferred heat from a cold to hot body, but it was not the only thing that happened, because some compressor somewhere did some work. That's certainly allowed. What is not allowed is to have it flow from cold to hot with nothing involved.
The second thing to notice is the gas, after doing its thing, comes back to the starting point. That means you can do it over and over and over again. In one cycle, the gas has some heat coming in.
Q1
heat rejected
Q2
, some work done,
W
, and it comes back to where it is and you can go on doing it many, many times. That's why it's a useful engine. If the substance returns to the starting point, having done some work in return for some heat, you can do it over and over again. And Carnot's question was, "What's the efficiency of this engine?" We're going to calculate that now.
So, the efficiency of the engine is
η
, is
Q1 - Q2
over
Q1
. Or 1 -
Q2
over
Q1
. Well,
Q1
and
Q2
are pretty easy to calculate. Let me tell you why. In the process
AB
, remember isothermal expansion? The heat input is the work done, because change in internal energy is zero. And the work done, you remember, is
nRT
log VB
over
VA
. Similarly,
Q2
, as a positive number, is
nRT2
log Vc
over
VD
. Remember,
Q2
here is defined as a positive number, even though it's the heat rejected, so if I want to get a positive number, I write the log of the initial over
V
final, so I get a--sorry,
Vc
over
VD
. So, the efficiency now becomes 1 -
Q2
over
Q1
, becomes 1 minus
T2
over
T1 log Vc
over
VB
divided by log--I'm sorry,
Vc
over
VD
divided by a
log VB
over
VA
. Again, if you cannot follow my script here, you may have to go back and get the subscript right. But don't worry too much about all the details. What I want you to know is the heat input here and the heat rejected here are all a familiar quantities from what I did earlier.
But now, here is the punch line;
η
, I claim is 1 -
T2
over
T1
. In other words, I'm saying forget this ratio of logarithms. It is just 1. I will show that to you, of course. It's not going to be written without proof, but the final answer for efficiency of this engine is 1 -
T2
over
T1
. So, we need to show why
Vc/VD
is the same as
VB/VA
. Well, I will derive that here, then for a couple of minutes I'll talk about it, then we'll come back and resume the discussion. I'm going to show you that
Vc/VD
is the same as
VB/VA
. I'm going to show that to you. Then you agree, if I take the logs then, the logs will cancel. How do I know this? Well, go back and use the fact that that's an isothermal process. That is an isothermal process. That is an adiabatic process and that's an adiabatic process [drawing graph on board]. This is temperature
T1
, this is temperature
T2
, this is
A
,
B
,
C
,
D
.
Now, somewhere in your notes is a formula that in an adiabatic process, volume
A
times temperature 1 to some strange power, I don't care what the power is--it's not going to matter. It's the same. Sorry, volume
B
times temperature to some power is the same as volume
C
, the same, temperature
T2
to some power. Because in the process of adiabatic, we have seen
PV
to the
γ
is constant, but I told you can also write it as volume times temperature to some power is a constant. So,
B
and
C
are correlated this way.
Likewise,
A
and
D
are connected by an adiabatic process so you can be sure that
VA
,
TA,
that happens to be
T1
, raised to some power, is the same as
VDT2
raised to same power. We don't care what the power is. It's probably
Cv
over
R
or
R
over
Cv
. I'm not interested in that. In fact, if you go back to this top right-hand corner you can see it is volume times
T
to the power of
Cv
over
R
. But it's not important. The fact that
B
and
C
lie on an adiabatic curve means that the volume at
B
and the temperature at
B
, which happens to be
T1,
and the volume of
C
and the temperature of
C
, which happens to be
T2
, are connected by this result. Once I write it down for this adiabatic and this adiabatic, now divide that by that, and that by that, and the point is that
T1
, to whatever power it is, cancels top and bottom, top and bottom, and I get the result I wanted, which is
VB
over
VA
, is
Vc
over
VD
. Once you put that in, you get the final result
η
is 1 -
T2
over
T1
.
Now, there are some things you should know all the time and something you should know some of the time, and something you should've seen at least once. The derivation of the result you should've seen at least once in your life. Whether you carry it in your head or not, I'm not interested in. But what have I really done?
I've taken an ideal gas and taken it over a cycle and I found out that in that cycle, the ideal gas does function like a very primitive heat engine because it takes some heat
Q1
, rejects some heat
Q2
, and does some work given by the shaded area. And the ratio of work done to heat absorbed in the end happens to be 1 -
T2/T1
. It does not depend on the gas. It depends only on the upper temperature and the lower temperature. Now, the question you can ask is, "Why are you computing the efficiency of this really primitive and stupid engine when we're interested in real engines that GM is going to make or some steamship is going to make or some engineer is going to make?" We will show next time that this efficiency is a theoretical maximum. I will show you next time that no engine can beat the Carnot engine. No engine can be as good. It can be as good but cannot be better than the Carnot engine, and that's what makes the result important. It's a lot like a relativity example, but to show you why time slows down in a moving frame I took a very stupid clock where the clock ticks because light beam goes up and down. That's not your idea of a clock, but in that clock, if you can see why it slows down, you know that every clock has to slow down because all clocks in a moving rocket must run at the same rate. Otherwise, you can compare the two clocks and find out you are moving. Likewise, if you take a very primitive engine, but you can show that that engine is the most efficient engine, you are done because that's going to put an upper limit on the efficiency. So, I'll come back and I'll tell you next time why no engine can beat this engine and why hidden in this result is the notion of entropy.
[end of transcript]
Back to Top | [mp3](https://oyc.yale.edu/sites/default/files/courses/fall06/phys200/mp3/phys200_23_120406.mp3) |
