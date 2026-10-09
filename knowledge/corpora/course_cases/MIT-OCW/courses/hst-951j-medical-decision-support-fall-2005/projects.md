- Source: https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### General Guidelines for Final Project

You should apply **one or more** of the models covered in class for your final project.

If you implement the algorithms yourself, then you do not need to compare more than one model, but you have to **document your implementation** and append it with the final report (e.g., you implemented a genetic algorithm that selects variables to be used in a neural network model).

If you are using existing software packages (See5.0, Genie, Rosetta, etc.), then I would like you to apply your data in **at least two different types of models, preferably more** (e.g. classification tree and rough sets), justify why you think the data are better suited for these methods (e.g., categorical data are better suited for classification trees than neural networks).

Use medically related data. I will provide those with little medical connections with published data sets (e.g., trauma patients, extracted from Christensen’s textbook on logistic regression). Use this set or another of your interest to compare performance of several models or to investigate selection of variables (e.g., comparison of different selection methods), selection of cases (e.g., detection of outliers). You can use medical data from:

- [UCI depository and UCI KDD archive](http://www.ics.uci.edu/~mlearn/MLRepository.html)
- [Statlib](http://lib.stat.cmu.edu/DASL/)
- [Delve - Data for Evaluating Learning in Valid Experiments](http://www.cs.toronto.edu/~delve/)
- [R Project](http://www.r-project.org/)
- [NCBI - National Center for Biotechnology Information](http://www.ncbi.nlm.nih.gov/)

too.

Remember to **use the evaluation methods** covered in class (ROC curves, calibration curves and indices, etc.) to report performance of your models.

### Reports

The report should be **between 4-6 single spaced pages**, 10-point font. Report can be longer if you really need, but please do not add fluff. Include the usual:

- Abstract
- Background: (why the problem being addressed is important.)
- Material and Methods: (include here as much detail as possible here, such as the exact parameters you used – learning rate 0.05, etc. – software name and version, and anything that would make your work reproducible by another person.) Include pointers to the data sets you used, as well as any detail of pre- or post processing that was used (e.g., constructed randomly 10 pairs of training and test sets for cross-validation, etc.).
- Results
- Discussion
- Conclusion
- References
- Appendices (e.g., code implemented, pointers to data sets)

### Web page

Delivery: Please create a web-page for your report. This web-page should contain:

- Title of the report
- An abstract/summary of the report
- A link to the report proper
- Links to source code/application files and data needed to repeat what you did for the report

### Software

If you want to install stuff on your own machine, [R](http://www.r-project.org/) is free. Feel free to implement algorithms if you want. Other packages you might consider are:

- Neural networks: NevProp4, by Prof. Phil Goodman
- Logistic regression: SAS
- Classification trees: [See5.0](http://www.rulequest.com/)
- Rough sets: [Rosetta](https://www.rosettacommons.org/software)
- Belief networks: [SamIam](http://reasoning.cs.ucla.edu/samiam/)

Please note that some of these are freely available as demo versions only, so there may be limits on number of cases, variables, days available for trial, etc.

### Examples of OK projects

- Compare performances of 4 different machine learning models in a certain data set, and fully report results using evaluation methods described in class.
- Compare performance of 1 machine learning model (explain why you chose this one) and one or more medical experts (the expert cannot be yourself).
- Investigate variable selection methods in different types of models (use of artificial sets to make a point is OK, but please also try in some real data).
- Investigate case selection methods in different types of models (use of artificial sets to make a point is OK, but please also try in some real data).

### Examples of Not OK projects

- Build a framework for application of some method without actually using or implementing the method and showing results in artificial or real data.
- Build a decision tree on some medical topic using you or your colleague’s probabilities and utilities without testing in the real world.
- Apply one machine learning model in a data set and not compare results to an existing reported model or other models.
- Report results of machine learning models using accuracy alone.
- Recycle projects from other classes.

If you don’t know whether your project would be OK or not, please discuss it with the instructors.

### Example Student Work

Example final projects are included courtesy of the students listed below. Used with their permission.

#### Final Project by Mark Meyer, MD MPH.

[Application of Sequence Alignment Algorithms in Location Tracking Data to Determine Patient State in a Clinical Process](https://ocw.mit.edu/ans7870/HST/HST.951/f05/projects/Meyer/index.html)

Final Report ([PDF](https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/resources/hst951_fin_rep/))

Oral Presentation ([PDF - 1.70 MB](https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/resources/seq_align/))

#### Final Project by Michael Blechner, MD.

[Behavior of Various Machine Learning Models in the Face of Noisy Data](https://ocw.mit.edu/ans7870/HST/HST.951/f05/projects/Michael_Blechner/Behavior%20of%20Various%20Machine%20Learning%20Models%20in%20the%20Face%20of%20Noisy%20Data.htm)

Final Report ([PDF](https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/resources/full_text/))

#### Final Project by Jaime Chang

[Computerized Pulmonary Artery Catheter Waveform Interpretation](https://ocw.mit.edu/ans7870/HST/HST.951/f05/projects/Jamie_Chang/Computerized%20Pulmonary%20Artery%20Catheter%20Waveform%20Interpretation.htm)

Final Report ([PDF](https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/resources/pac/))

Oral Presentation ([PDF](https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/resources/pac_ppt/))

#### Final Project by Jessie I. Chen

[C# .NET Algorithm for Variable Selection Based on the Mallow’s Cp Criterion](https://ocw.mit.edu/ans7870/HST/HST.951/f05/projects/JessieChen/MDS%20Final%20Project.htm)

Final Report ([PDF](https://ocw.mit.edu/courses/hst-951j-medical-decision-support-fall-2005/resources/jessiechenpaper/))
