- Source: https://ocw.mit.edu/courses/6-s897-machine-learning-for-healthcare-spring-2019/pages/projects/final-project-suggestions/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects Final Project Suggestions

Students will produce a final project using a health insurance claims database such as IBM MarketScan, Optum, Center for Medicare & Medicaid Services claims data, or state All-Payer Claims Databases.

Below we describe two types of projects, those focused more on answering a specific clinical question and those focused more on developing novel ML methods. That said, we imagine that many projects may involve a bit of each, and that’s OK!

### MIMIC Projects

#### Clinical Projects

MIMIC-III provides a wealth of data to tackle a variety of clinical tasks in the ICU. Here are a few examples of potential clinical questions:

- Identify organ failure
  - In the ICU, we are concerned about organ failure in the heart, kidney, liver, and lung. What predictors could be useful for organ failure?
  - We would want an early enough prediction to be productive and sufficient data in the lab tests (e.g. liver enzymes, creatinine and BUN, blood pressure) in earlier data.
- Effects of interventions
  - Which interventions should we do and at what time?
  - Potential interventions include vasopressors, mechanical ventilation, dialysis, and cardiac assist devices.

Below are some examples of research papers that used the MIMIC-III dataset:

- Che et al, 2018. “[Recurrent Neural Networks for Multivariate Time Series with Missing Values](https://www.nature.com/articles/s41598-018-24271-9).” *Nature Scientific Reports.*
- Dernoncourt et al, 2016. “[De-Identification of Patient Notes with Recurrent Neural Networks](https://academic.oup.com/jamia/article/24/3/596/2769353).” *JAMIA*.
- Ghassemi et al, 2014. “[Unfolding Physiological State: Mortality Modelling in Intensive Care Units](https://www.ncbi.nlm.nih.gov/pubmed/25289175).” *KDD*.
- Boag et al, 2018. “[Racial Disparities and Mistrust in End of Life Care](https://arxiv.org/abs/1808.03827).” *MLHC*.
- Johnson et al, 2017. “[Reproducibility in Critical Care: A Mortality Prediction Case Study](http://proceedings.mlr.press/v68/johnson17a.html).” *MLHC*.
- Schulam et al. 2016. “[Integrative Analysis using Coupled Latent Variable Models for Individualizing Prognoses (PDF)](http://jmlr.org/papers/volume17/15-436/15-436.pdf).” *JMLR*.
- Young et al. 2018. “[Uncovering the Heterogeneity and Temporal Complexity of Neurodegenerative Diseases with Subtype and Stage Inference](https://www.nature.com/articles/s41467-018-05892-0).” *Nature Communications*.

#### Machine Learning Methodology

Similar to above, you can also explore how to extend known machine learning methodology given the challenges of clinical data:

- Clinical natural language processing (NLP)
  - How can we better extract entities from the clinical notes such as diseases, symptoms, and treatments? We saw in problem set 3 how existing methods can be flawed. Once we do have these entities, how can we identify relations between the extracted clinical concepts?
  - Can we construct a timeline from the clinical notes? How would these extracted entities relate with the coded events in the patient chart?
- Time series
  - How can we better predict a patient’s progression? Challenges could include missing data, unknown alignment of patients, and heterogeneity of conditions.
  - How can we interpret a patient’s progression? Clinicians may be interested in how a patient progresses through known concepts (e.g. ICD-9 codes) and also what the specific stages of progression might be.

### Projects Using IBM MarketScan Data

Although not publicly available, students were provided access to the IBM MarketScan research database in the 2019 version of the course. These ideas can easily be extended to other research databases such as Optum, Center for Medicare & Medicaid Services claims data, or state All-Payer Claims Databases. Since the MarketScan research database has coverage of a patient’s full longitudinal clinical trajectory, it is a gold mine for research and already thousands of papers have been published using it. Students should expect to access the data including basic demographics, diagnoses, procedures, outpatient prescription orders, laboratory test orders, and enrollment information.

#### Clinical Projects

This type of MarketScan project will focus on studying a new clinical question using machine learning and causal inference methods studied in class.

- Early detection of a medical condition, e.g. rheumatoid arthritis or Sjogren’s syndrome
- Causal inference of the effect of an intervention
- Subtyping or clustering to better understand a population, e.g. individuals rehospitalized within 30-days

Below are examples of papers that have explored some of the above questions. We encourage students to use these for inspiration, but to tackle new clinical questions that weren’t already answered in these (e.g., studying a different disease or a different outcome).

- *Example of Prediction*: Razavian et al., 2015. “[Population-Level Prediction of Type 2 Diabetes From Claims Data and Analysis of Risk Factors: Big Data.](https://www.liebertpub.com/doi/full/10.1089/big.2015.0020)”
- *Example of Causal inference*: Brat et al., 2018. “[Postsurgical Prescriptions for Opioid Naive Patients and Association With Overdose and Misuse: Retrospective Cohort Study.](https://www.bmj.com/content/360/bmj.j5790)”
- *Example of Characterization*: Hripcsak et al., 2016. “[Characterizing Treatment Pathways at Scale Using the OHDSI Network, PNAS.](https://www.pnas.org/content/early/2016/06/01/1510502113.full)”
- *Example of Subtyping*: Doshi-Velez et al., 2014. “[Comorbidity Clusters in Autism Spectrum Disorders: An Electronic Health Record Time-Series Analysis, Pediatrics.](https://www.ncbi.nlm.nih.gov/pubmed/24323995)”

#### Machine Learning Methodology

The projects mentioned here focus on developing new machine learning methods:

- Develop better deep learning algorithms for claims data.
  - Example: widening the gap between the deep learning and baseline methods from [Rajkomar et al., 2018](https://www.nature.com/articles/s41746-018-0029-1) and [Choi et al., 2016 Doctor AI (PDF)](http://proceedings.mlr.press/v56/Choi16.pdf). You could design [new architectures](https://ieeexplore.ieee.org/abstract/document/7762861) that are better suited for medical data, unsupervised learning algorithms (see e.g. [Choi et al., 2016 Relationships](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5001761/) and [Beam et al., 2018](https://arxiv.org/abs/1804.01486)), etc.
- Develop synthetic data generation methods that produce realistic data but have provable privacy guarantees (this is a good project for a group with a theoretical computer science bent).
  - Recent work has been interested in using deep learning for this, e.g. [Choi et al., 2017](https://arxiv.org/abs/1703.06490) and [Hyland et al., 2017](https://arxiv.org/abs/1706.02633). However, there is a natural trade-off between truly capturing the data density (not just being able to reproduce aggregate statistics from synthetic data) and not leaking private information from the training data. How does one formalize this mathematically?
- Learn models of what a “normal” treatment policy is for a disease (note: it may be sequential).
  - How do these differ across populations, either geographic or based on patient characteristics? Can you automatically discover different treatment strategies for the same condition? Can you identify patients that are outliers or are receiving abnormal treatment (these may because of fraud, improper treatment, medical errors, etc.)?
- Develop algorithms for inferring causality (e.g., one condition causes another, or a medication causes a side-effect) from longitudinal claims data, e.g. by using ideas from Granger causality, the recently developed [entropic causality](https://arxiv.org/abs/1611.04035), causal Bayesian networks, or [Hawkes processes (PDF)](https://people.csail.mit.edu/yujia/assets/pdf/hawkes_pdf.pdf).
- Develop algorithms to identify and explain non-stationarity, e.g. through changepoint detection and interpretable ML algorithms.

### Other Datasets

- [Multiple Myeloma Research Foundation Compass](https://research.themmrf.org/)
- [The Parkinson’s Progression Markers Initiative](http://www.ppmi-info.org/)
  - Specific project suggestion: Learning a representation of MRI images that will help with downstream tasks, e.g. classifying healthy, prodromal, early-stage Parkinson’s, vs late-stage Parkinson’s, or time to outcome. Possible methodologies to consider include [3-D CNN](https://arxiv.org/abs/1806.05233), [voxel-based logistic regression](https://www.sciencedirect.com/science/article/pii/S1053811917301787?via%3Dihub), or principal components. Can you interpret what the representation is capturing?
- [eICU](https://eicu-crd.mit.edu/about/eicu/)
  - Same access requirements as MIMIC-III. eICU has clinical ICU data from 200+ hospitals.
- Chest X-rays
  - [The MIMIC-CXR Database](https://archive.physionet.org/physiobank/database/mimiccxr/)
  - [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/)
  - [Open-i service of the National Library of Medicine](https://openi.nlm.nih.gov/faq)
- [The Osteoarthritis Initiative](https://data-archive.nimh.nih.gov/oai/)
- A more extensive [list of medical datasets](https://github.com/beamandrew/medical-data).
