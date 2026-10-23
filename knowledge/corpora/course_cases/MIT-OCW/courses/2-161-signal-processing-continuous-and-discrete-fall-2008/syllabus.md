- Source: https://ocw.mit.edu/courses/2-161-signal-processing-continuous-and-discrete-fall-2008/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Textbooks

Proakis, John G., and Dmitris K. Manolakis. *Digital Signal Processing*. 4th ed. Upper Saddle River, NJ: Prentice Hall, 2006. ISBN: 9780131873742.

Oppenheim, Alan V., Ronald W. Schafer, and John R. Buck. *Discrete-Time Signal Processing*. 2nd ed. Upper Saddle River, NJ: Prentice Hall, 1999. ISBN: 9780137549207.

These are recommended highly, but not mandatory. A list of other references is available in the [readings](https://ocw.mit.edu/courses/2-161-signal-processing-continuous-and-discrete-fall-2008/pages/readings/).

### Credit and Content

12 units, Graduate H level.

### Prerequisites

There is no stated prerequisite course for 2.161. Students entering this course are expected to have an undergraduate understanding of system dynamics and elementary linear system theory, such as provided by this department’s 2.003, 2.004, and 2.14 undergraduate sequence. There is no expectation of familiarity with discrete time signal processing.

MATLAB will be used extensively throughout the course. Students will be expected to be able to create “.m” files.

### Grading

There will be three quizzes in the class. In addition there will be regular homework and project assignments. (Projects will involve the manipulation of real experimental data.) Grades will be allocated on a score consisting of:

| ACTIVITIES | PERCENTAGES |
| --- | --- |
| Quizzes and projects | 80% |
| Homework | 20% |

### Course Ethics: Guidelines for Independent Effort

Students may collaborate on the formulation of solutions to problem sets, but each student must turn in a solution that is obviously his/her own work.

**Plagiarism**, or the copying of material from others, including paraphrasing materials from the reports of others without acknowledgment, is contrary to the standards of the Institute and will be considered **a** **serious academic offense**.

Possible sanctions against students suspected of plagiarism may include a grade of 0 for the report, a grade of F for the course, departmental probation, and/or appearance before the institute Committee on Discipline (COD).

### Topics to be Covered (not necessarily in this order)

#### 1) Review of Linear Continuous-Time Signal Processing

Fourier methods, Laplace transform, convolution, frequency/time domain processing. Passive and active continuous filters. Linear filter implementation using op-amps.

#### 2) Introduction to Real-Time Computation

Data converters (A/D, D/A), machine architecture, software considerations.

#### 3) Sampling and Reconstruction

Sampling theorem, aliasing, quantization, sampled data systems, cardinal (Whitaker) reconstruction, zero-, first-, second-order hold reconstructors, interpolators, non-resetting reconstructors, matched filtering. Interpolation and decimation.

#### 4) Discrete-Time Signal Processing

The z transform, difference equations, relationship between F(z) and F*(jw), mappings between s-domain and z-domain, inverse z transform. Discrete–time stability.

#### 5) Discrete Spectral Analysis

The DFT and its relationship to the continuous FT, the FFT and implementations (decimation in time and frequency), radix-2 implementation, leakage, windowing. Uses of the DFT: convolution — (overlap and add, select savings), correlation. Random processes, power spectral density (PSD) estimation — methods of smoothing the periodogram (Welch’s method, windowing the correlation function, etc). ARMA methods.

#### 6) Real-Time Simulation Methods Using Difference Equations

Impulse-, step-, ramp-invariant simulations. Tustin’s method, matched poles/zeros, bilinear transform methods. Error analysis.

#### 7) Filter Design — Continuous and Discrete

Butterworth, elliptic, Chebyshev low-pass filters. Low-pass design methods based on continuous prototypes. Realizations. Conversion to high-pass, band-pass, band-stop filters. Discrete-time filters: IIR and FIR. Linear phase filters. Frequency sampling filters.

#### 8) Statistical Signal Processing

Linear prediction, adaptive filters (LMS), recursive least-squares.

#### 9) Introduction to Discrete-Time Feedback
