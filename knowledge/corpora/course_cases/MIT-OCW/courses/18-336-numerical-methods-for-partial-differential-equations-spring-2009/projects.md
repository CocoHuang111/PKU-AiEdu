- Source: https://ocw.mit.edu/courses/18-336-numerical-methods-for-partial-differential-equations-spring-2009/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### Project Description and Schedule

The course project counts for 50% of the overall course grade.

The project consists of

- a midterm report (20% of the project grade)
- a final report (60% of the project grade), and
- a presentation (20% of the project grade)

Throughout the term, each participant works on an extended problem related to the content of the course. You are allowed to choose a project which is related to your thesis, however, the following restrictions apply:

- The project must focus on computational aspects related to the lecture topics.
- It is illegal to “reuse” a project from another course or thesis work. Your 8.336 project must cover specific questions and goals, which must not to be identical to the questions and goals of your thesis. For instance, you can investigate a specific computational aspect of your work, and investigate this aspect deeper than you would in your thesis work.

Of course, you can also choose a topic unrelated to your other work. For instance, you can consult the lecturer for interesting problems related to his research.

Any course project has to be agreed on by, and is under the supervision of the lecturer.

The following deadlines apply:

- By Ses #4: Submit project proposal
- By Ses #13: Submit midterm report on project
- By Ses #25: Submit final project report
- Last two sessions: Give short talk on project

### Project Proposal

Your project proposal to should include the following information:

- Project title
- Project background Does it relate to your work in another field (e.g. your thesis)? If yes, briefly outline the questions and goals of your work in the other field.
- Questions and Goals Briefly describe the questions you wish to investigate in your project. What are your expectations?
- Plan Which language do you plan to program in? Do you intend to use special software? Does your project work relate to the work of other people at MIT?

### Project Abstracts

Project presentations take place on a Saturday, and are aimed at a general scientific audience, with focus on the numerical solution of physically arising equations.

The following represents the project abstracts chosen by the students during the Spring ‘09 term.

#### Numerical Solution for Poisson Equation with Variable Coefficients

I will present a numerical technique to obtain the solution of a quasi-3-dimensional potential distribution due to a point source of current located on the surface of the semi-infinite media containing an arbitrary 2-dimensional distribution of conductivity. I will show how two different boundary conditions (Neumann and mixed) chosen to simulate the “infinitely distant” edges of the lower half-space affect the accuracy of the solution. The solution on the uniform and non-uniform grid will be compared. Some figures showing the potential field over the simple structures (such as layered media, vertical contact, square body) will be presented.

#### Finite Difference Elastic Wave Modeling with an Irregular Free Surface

The objective of my project is to model elastic wave propagation in a homogenous medium with surface topography. Surface topography and the weathered zone (i.e., heterogeneity near the earth’s surface) have great effects on seismic surveys as the recorded seismograms can be severely contaminated by scattering, diffractions, and ground rolls that exhibit non-ray wave propagation phenomena. implemented a 2-D staggered finite difference approximation of first order PDEs that is second-order accurate in time and space (with velocity-stress formulation), and described the results of the finite-difference scheme on various irregular free surface models.

#### Simulation of the Onset of Baroclinic Instability

Many features of atmospheric dynamics can be demonstrated with a simple table-top rotating tank experiment. Here a numerical simulation of the incompressible Navier-Stokes equations and the heat equation is applied to a flow in a rotating annular tank. A finite difference method is used on an axisymmetric 2-Drotating reference frame. At low rotational rates a stable vertical velocity gradient is observed in the zonal flow, corresponding to the tropical Hadley cell flow. At high rotational rates a baroclinic instability is observed, corresponding to atmospheric dynamics seen in the upper-latitudes.

#### Analysis of the Time-Dependent Coupling of Optical-Thermal Response of Laser-Irradiated Tissue Using Finite Difference Methods

Over the years lasers have been extensively used for detection and treatment of diseases and abnormal health conditions including cancerous tissues and arterial plaques. While such detection and treatment has numerous advantages including superior accuracy and unparalleled control over conventional techniques, it is imperative to optimize light dosimetry, treatment parameters and conditions of delivery a priori so that thermal damage due to laser irradiation is limited to the tissue area (volume) under consideration. In this work, a non-linear finite-difference program is developed to simulate the dynamic evolution of tissue coagulation considering the dependence of the optical properties and blood perfusion on the instantaneous temperature and damage index. Using this coupled optical diffusion-bioheat equation model, we observe that significant changes arise as a function of the dynamic behavior of the optical properties and the perfusion. Specifically, the model reveals that the heat penetration in laser irradiated tissue is much lesser than what would be expected from a static treatment of the biophysical parameters. Finally, we provide preliminary results on the optical-thermal response of the tissue on application of a pulsed laser.

#### Modeling and Simulation of Self-Sustained Combustions in Reactive Multi-Layers of Energetic Materials

It is known that forced mixing of energetic materials such as nickel and aluminum results in highly exothermic reactions. The reaction, herein combustion, initiated by thermal impulses propagates through the materials in self-sustained manner. In this project, self-sustained combustion and its propagation in a reactive Ni-Al nanolaminate is first mathematically modeled in two coupled partial differential equations for heat and atomic diffusions. The, the coupled governing equations are discretized in time and space, and numerically solved using the finite difference schemes for the Ni-Al nanolaminate domain with appropriate initial and boundary conditions for the temperature and atomic composition. The simulation results for the heat and mass diffusion with combustions would be presented, and compared with several experimental results. Also, several important effects of simulation conditions such as initial temperature profile, ambient temperature and Ni-Al premixed thickness would be discussed. Finally, several important features for the governing equations, and physical and chemical assumptions for the models would be addressed.

#### Simulation of an Airbag for Landing of Re-Entry Vehicles

This presentation will focus on the implementation of the Immersed Boundary Method to approximate the dynamics of an impacting airbag intended for use in Earth re-entry vehicle applications. Specifically, the numerical approach and its related implementation issues will be discussed, followed by a discussion and analysis of the obtained results.

#### Immersed Boundary Method (IBM) for the Navier Stokes Equations

Studying certain medical conditions, such as hypertension, requires accurate simulation of the blood flow in complex-shaped elastic arteries. In this work we present a 2-D fluid-structure interaction solver to accurately simulate blood flow in arteries with bends and bifurcations. Such blood flow is mathematically modeled using the incompressible Navier-Stokes equations. The arterial wall is modeled using a linear elasticity model. Our solver is based on the immersed boundary method (IBM). The numerical accuracy of our solver stems from using a staggered grid for the spatial discretization of the incompressible Navier-Stokes equations. The computational efficiency of our method stems from using Chorin’s projection method for the time stepping, coupled with the fast Fourier transform (FFT) to solve the intermediate Poisson equations. We have validated our results versus reference results obtained from MERCK Research Laboratories for a straight vessel of length 10cm and diameter 2cm. Our results for pressure, flow and radius variations are within 5% of those obtained from MERCK.

#### Finite Difference Modeling of Seismic Wave Propagation in Fractured Media (2D)

It is critical to detect and characterize fracture networks for production of oil reservoirs. Much effort has gone into the development of methods for identifying and understanding fracture systems from seismic data. Forward modeling of seismic wave propagation in fractured media plays a very important role in this field. In equivalent medium theory, background medium pluses fracture is equivalent to anisotropy medium, in this paper, I will use this theory together with staggered finite difference technique for modeling seismic wave propagation in fractured media.

#### Glacial Ice Streams

Two models of one-dimensional longitudinal glacial ice flow as a function of depth are presented. The system dynamics are governed by Stokes? 2019 flow acting under the influence of a velocity dependent viscosity coefficient. The domain of computation is discretized on a staggered one-dimensional grid to enhance the stability of the methods. The first model uses a centered finite difference scheme to treat the problem as a diffusion problem with non-constant spatially and temporally varying coefficients. The second model combines centered and upwinded finite difference schemes to treat the problem as an advection problem. These methods are compared for a range of basal boundary conditions representative of the found in large glacial ice sheets, with prescribed velocities, shear stresses, or shear stress limits.

#### Solver for Axisymmetric Low Speed Inviscid Flow

A blade row refers to a set of airfoils attached circumferentially to a central hub. The blades and hub may be stationary (stator) or rotating (rotor) and each such arrangement forms a stage of turbomachinery systems. These systems include compressors, turbines, pumps, propellers and fans and have crucial applications in all aspects of engineering. This project addresses reduced order modeling of the 3d flow characteristics of a low speed axisymmetric blade row in the 2d meridional reference frame. The approach is to implement a finite difference discretization of the 2d domain and represent the effect of the blades using a postulated blade loading model (local forcing term). However, the iterative solver for the large non-linear 3x3 system proved very difficult to implement in the finite difference setting being very prone to implementation errors. Accuracy of the blade loading model was also hard to quantify due to the complexity involved with higher order spatial discretization.

#### Modeling the Process of Milk Steaming by an Espresso Machine

In this project the insulating properties of a ceramic mug and an aluminum mug are compared. The Heat Transfer equation is solved over the systems as to compare the speed at which heat is lost from the beverage. The radial symmetry of the system is employed to simplify the calculation from a 3 dimensional physical space to a 2 dimensional cylindrical system without rotation. The complications arising from the 1/*r* term in the cylindrical form of the Heat Transfer equation is discussed and resolved. Additionally, a predictive model is developed to determine the temperature of a cup of coffee at a certain time, *t*, given the vessel’s material and the percentage of milk in the coffee.

#### Numerical Solution of the Continuous Linear Bellman Equation

Solutions to the Hamilton-Jacobi-Bellman (HJB) equation describe an optimal policy for controlling a dynamical system such as a robot or a virtual character. However, the HJB equation is a non-linear PDE that is difficult to solve directly, especially for stochastic systems. For a certain class of optimal control problems, a change of variables turns the non-linear Hamilton-Jacobi-Bellman (HJB) equation into a linear PDE. This PDE, the linear Bellman equation, can be solved analytically in certain cases and numerically using standard methods in other cases. As an example application, one can use solutions of the linear Bellman equation to navigate a three wheeled robot.
