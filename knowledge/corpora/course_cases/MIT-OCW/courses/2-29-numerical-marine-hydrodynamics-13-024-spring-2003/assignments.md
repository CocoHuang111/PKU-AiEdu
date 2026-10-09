- Source: https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

### Notes about Problem Sets 6 and 8

In problem sets 6 and 8, students write MATLAB® programs to solve two-dimensional boundary integral equations based on Green’s Theorem. In problem set 8, the inviscid streaming flow about an arbitrary two-dimensional object is calculated. The solution is done for a circular cylinder.

In problem set 8, the method is extended to the flow around a lift-generating airfoil with a wake across which there is a jump in the velocity potential. The two-dimensional Green function that is used is G = -ln r, where r is the distance between a “source point” and a “field point”.

The student is not expected to write an efficient MATLAB® m-file for computing the integral of the Green Function over a panel. Rather, that m-file is given to the students and it is called **rank2d.m**. This m-file computes the integral of the Green function, g, and of the normal derivative of the Green function, **dg/dn**, over a panel. This m-function works in local coordinates for which the “source panel” is approximated as a line on a local x-axis with the center of the line at the local origin. The “field point” is at (x,y) in local coordinates. The normal vector to the panel is in the positive local y-direction.

To use **rank2d.m** function, the panel length and the location of the field point in local coordinates must first be determined. This is done in the m-function “**localize.m**”, which should also be provided to the student who writes and used the remainder of the set of programs needed to complete the problem sets.

The m-functions, **rank2d** and **localize** are provided with problem set 6.

### Problem Sets

- Problem Set 1 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps1/))
- Problem Set 2 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps2/))
- Problem Set 3 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps3/))
- Problem Set 4 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps4/))
- Problem Set 5 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps5/))
- Problem Set 6 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps6/))
- Problem Set 7 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps7/))
- Problem Set 8 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps8/))
- Problem Set 9 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps9/))
- Problem Set 10 ([PDF](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/ps10/))

### Supporting Files

- 64a012.fin ([FIN](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/64a012/))
- LOCALIZE.M ([M](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/localize/))
- RANK2D.M ([M](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/rank2d/))
- wig4125.out ([OUT](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/wig4125/))
- wigley5.out ([OUT](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/wigley5/))
- wigley9.out ([OUT](https://ocw.mit.edu/courses/2-29-numerical-marine-hydrodynamics-13-024-spring-2003/resources/wigley9/))
