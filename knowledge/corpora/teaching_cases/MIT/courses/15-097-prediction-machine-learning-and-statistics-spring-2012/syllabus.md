> 检索摘要：15.097 Prediction: Machine Learning and Statistics（Spring 2012，Graduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times:；Course Description；Audience, Prerequisites, and Related Courses；Course Requirements；Additional References (Optional)；Course Material；Overarching Themes；Concepts；Algorithms (some covered in more depth than others)；History；Theory。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/15-097-prediction-machine-learning-and-statistics-spring-2012/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times:

Lectures: 2 sessions / week, 1.5 hours / session

### Course Description

Prediction is at the heart of almost every scientific discipline, and the study of generalization (that is, prediction) from data is the central topic of machine learning and statistics, and more generally, data mining. Machine learning and statistical methods are used throughout the scientific world for their use in handling the “information overload” that characterizes our current digital age. Machine learning developed from the artificial intelligence community, mainly within the last 30 years, at the same time that statistics has made major advances due to the availability of modern computing. However, parts of these two fields aim at the same goal, that is, of prediction from data. This course provides a selection of the most important topics from both of these subjects.

The course will start with machine learning algorithms, followed by statistical learning theory, which provides the mathematical foundation for these algorithms. We will then bring this theory into context, through the history of ML and statistics. This provides the transition into Bayesian analysis.

Major topics:

- An overview of the “top 10 algorithms in data mining,” following a survey conducted at the International Conference on Data Mining (including association rule mining algorithms, decision trees, k-nearest neighbors, naïve Bayes, etc.)
- A unified view of support vector machines, boosting, and regression, based on regularized risk minimization
- Statistical learning theory, structural risk minimization, generalization bounds (using concentration bounds from probability), the margin theory, VC dimension and covering numbers
- Frameworks for knowledge discovery (KDD, CRISP-DM)
- Notes on the history of ML and statistics
- Bayesian analysis (exponential families, conjugate priors, hierarchical modeling, MCMC, Gibbs sampling, Metropolis-Hastings)

### Audience, Prerequisites, and Related Courses

This course is aimed at the introductory graduate and advanced undergraduate level. It will provide a foundational understanding of how machine learning and statistical algorithms work. Students will have a toolbox of algorithms that they can use on their own datasets after they leave the course.

The course contains theoretical material requiring mathematical background in basic analysis, probability, and linear algebra. Functional analysis (Hilbert spaces) will be covered as part of the course, and previous knowledge of the topic is not required. There will be a project assigned, and you are encouraged to design the project in line with your own research interests.

The material in this course overlaps with [9.520](https://ocw.mit.edu/courses/9-520-statistical-learning-theory-and-applications-spring-2006) (which has more theory and is more advanced), [6.867](https://ocw.mit.edu/courses/6-867-machine-learning-fall-2006) (which has less theory, covers different algorithms, and is less advanced), and 6.437 (which does not cover ML or statistical learning theory). This course could be used as a follow-up course to 15.077, or taken independently.

Students will be required to learn R. Knowledge of MATLAB may also be helpful.

### Course Requirements

<table><tr><th>ACTIVITIES</th><th>PERCENTAGES</th></tr><tr><td>Problem sets, including computational exercises [not available on MIT OpenCourseWare]</td><td>50%</td></tr><tr><td colspan="2">Course Project</td></tr><tr><td>Proposal</td><td>10%</td></tr><tr><td>Advertisement</td><td>2%</td></tr><tr><td>Progress report</td><td>0%</td></tr><tr><td>Paper and talk</td><td>38%</td></tr></table>

### Additional References (Optional)

Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 3rd ed. Prentice Hall, 2009. ISBN: 9780136042594.

Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. 2nd ed. Springer, 2009. ISBN: 9780387848570. [Preview with [Google Books](http://books.google.com/books?id=tVIjmNS3Ob8C&printsec=frontcover)]

Cristianini, Nello, and John Shawe-Taylor. *An Introduction to Support Vector Machines and Other Kernel-based Learning Methods*. Cambridge University Press, 2000. ISBN: 9780521780193.

Gelman, Andrew, et al. *Bayesian Data Analysis*. 2nd ed. Chapman and Hall/CRC, 2003. ISBN: 9781584883883.

Bousquet, Olivier, Stéphane Boucheron, and Gábor Lugosi. [*Introduction to Statistical Learning Theory*. (PDF)](http://www.econ.upf.edu/~lugosi/mlss_slt.pdf)

Wu, Xindong, et al. [“Top 10 Algorithms in Data Mining.” (PDF)](https://link.springer.com/article/10.1007/s10115-007-0114-2) *Knowledge and Information Systems* 14 (2008): 1-37.

### Course Material

Machine learning and statistics tie into many different fields, including decision theory, information theory, functional analysis (Hilbert spaces), convex optimization, and probability. We will cover introductory material from most or all of these areas.

#### Overarching Themes

- Five important problems in data mining: classification, clustering, regression, ranking, density estimation
- The “top 10 algorithms in data mining”
- Frameworks for knowledge discovery (CRISP-DM, KDD)
- Priors in statistics

#### Concepts

- Training and testing, cross-validation
- Overfitting/underfitting, structural risk minimization, bias/variance tradeoff
- Regularized learning equation
- Conjugate priors and exponential families

#### Algorithms (some covered in more depth than others)

- Apriori (for association rule mining)
- k-NN (for classification)
- k-means (for clustering)
- Naive Bayes (for classification)
- Decision trees (for classification)
- Perceptron (for classification)
- SVM (for classification)
- AdaBoost and RankBoost (classification and ranking)
- Hierarchical Bayesian modeling (for density estimation), including sampling techniques

#### History

- Selected topics from the history of machine learning and statistics

#### Theory

- SVM derivation: convex optimization, Hilbert spaces, reproducing kernel Hilbert spaces
- Large deviation bounds and generalization bounds: Hoeffding bounds, Chernoff bounds (derived from Markov’s bound), McDiarmid’s inequality, VC bounds, margin bounds, covering numbers
