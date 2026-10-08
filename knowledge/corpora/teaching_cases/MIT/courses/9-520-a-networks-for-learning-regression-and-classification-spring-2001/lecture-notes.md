> 检索摘要：9.520-A Networks for Learning: Regression and Classification（Spring 2001，Graduate）的「Lecture Notes」。页内标题：Lecture Notes；The Course at a Glance；The Learning Problem in Perspective；Regularized Solutions；Reproducing Kernel Hilbert Spaces；Classic Approximation Schemes；Nonparametric Techniques and Regularization Theory；Ridge Approximation Techniques；Regularization Networks and Beyond；Applications to Finance；Introduction to Statistical Learning Theory；Consistency of the Empirical Risk Minimization Principle。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/9-520-a-networks-for-learning-regression-and-classification-spring-2001/pages/lecture-notes/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Lecture Notes

The lecture notes contain an executive summary of each class.

### The Course at a Glance

We introduce and motivate the main theme of the course, the setting of the problem of **learning from examples** as the problem of **approximating a multivariate function from sparse data** - the examples. We present an overview of the theoretical part of the course and anticipate the connection between Regularization Theory and Statistical Learning Theory, the two cornerstone theories on which the course rests. We briefly describe biological implications and several different applications derived from the proposed framework, ranging from vision to computer graphics and the stock market.

### The Learning Problem in Perspective

We present most of the concepts we will need (like **target space**, **loss function, empirical risk, expected risk,** and **hypothesis space**) and explain the structure of the theoretical part of the course. We look at the problem of learning from examples as the problem of **multivariate function approximation** from sparse **chosen** data, and then consider the case in which the data are **drawn,** instead of chosen, according to a probability measure. This enables us to illustrate the viewpoint of **Statistical Learning Theory** that will be used extensively during the course. **Regularization Theory** is introduced as a natural framework for studying this classic, ill posed problem which otherwise admits an infinite number of solutions.

### Regularized Solutions

A brief, somewhat unorthodox, review of Regularization Theory is presented. We show that uniqueness of the solution to the learning problem in the case of regression can be restored by appropriately restricting the space of the admissible solutions to sufficiently smooth functions. The important concept of smoothness functional is introduced. After a minimal primer on functional differentiation, we obtain the general form of the regularized solution as a weighted sum of kernel functions centered at the data points.

### Reproducing Kernel Hilbert Spaces

We discuss at length the properties of a very important class of kernels which lead to the key notion of **Reproducing Kernel Hilbert Space** (RKHS). RKHS will be an essential tool for establishing a connection between Regularization Theory and Statistical Learning Theory. We first provide the background to the concept of Hilbert space, introduce RKHS, and then clarify the relation between smoothness and a priori knowledge on the solution in RKHS. A simpler derivation of the general form of the regularized solution is also obtained.

### Classic Approximation Schemes

We show that a large number of classis approximation schemes, including splines and Radial Basis Functions (RBFs), are particular examples of the general framework presented so far. The dependence of the solution on the regularization parameter is also studied.

### Nonparametric Techniques and Regularization Theory

We introduce the theoretical properties of several nonparametric techniques for regression estimation, including nearest-neighbor techniques, local models, and kernel regression. Then we highlight their relation to the proposed regularization approach by means of the Parzen windows method for density estimation.

### Ridge Approximation Techniques

We introduce ridge approximation techniques, which include single- and multi-layer perceptrons and projection pursuit regression techniques. We discuss theoretical properties, implementation issues, merits and limitations of these techniques and explore in depth their relation with regularization theory.

### Regularization Networks and Beyond

In this class, we investigate the connection between networks for learning and the approximation scheme described so far. We discuss strengths and weaknesses of RBFs and RBF extensions which depend on the a priori knowledge on the solution, like Hyper Basis Functions. The relation between network architecture and the proposed regularization approach is unveiled.

### Applications to Finance

There are many uses of the learning/interpolation techniques we have discussed so far. In this class we present a non-parametric approach for estimating the value of derivative securities such as options in the stock market. The relation between relevant variables and the option price is “learned” from historical data. Computer simulations show that the learning techniques we described earlier (Hyper Basis Functions, Multi-Layer Perceptrons, Projection Pursuit Regression) can learn the Black-Scholes equation from synthetic data (generated using the Black-Scholes assumptions). They also perform well on real data of call options on SP500 futures.

### Introduction to Statistical Learning Theory

With this class we start to develop VC theory. The problem of learning from examples is set into a rigorous probabilistic framework. Several important concepts like expected and empirical risks, target and hypothesis spaces, and Bayes optimal solution are either introduced or revisited in the light of statistical learning theory.

### Consistency of the Empirical Risk Minimization Principle

We introduce the basic concepts needed to analyze the estimation error in VC theory by showing the connection between Empirical Risk Minimization (ERM) consistency and uniform convergence and illustrate necessary and sufficient conditions for the consistency of the ERM principle, that is for the convergence of the minimum of the empirical risk to the minimum of the expected risk.

### VC-Dimension and VC-bounds

After discussing the concepts of VC-entropy, annealed VC-entropy, and growth function for pattern recognition, the fundamental notion of Vapnik-Chervonenkis dimension is introduced and the so called VC-bounds are presented and discussed.

### VC Theory for Regression and Structural Risk Minimization

We first develop VC theory for regression estimation introducing the concept of V-gamma dimension, an extension of VC dimension. Then we show how to justify - for finite samples - in the framework of VC theory and through the RKHS formalism, a broad class of classification and regression schemes, which include Support Vector Machines and Regularization Networks.

### Support Vector Machines for Classification

In this class we describe in detail the Support Vector Machine, a pattern classification/regression algorithm recently developed by V. Vapnik and his team at AT&T Bell Labs. SVM can be seen as a new way to train polynomial, neural network, or Radial Basis Functions classifiers. From the implementation point of view, training a SVM is equivalent to solving a linearly constrained Quadratic Programming (QP) problem in a number of variables equal to the number of data points.

**Project Discussion:** This class is devoted to the discussion of the class projects.

### Support Vector Machines for Regression

In this class we describe Support Vector Machines for regression estimation and illustrate the connection between SVMs and Basis Pursuit De-Noising. Finally, we discuss the Bayesian interpretation of RNs and SVMs.

### Current Topics of Research I: Kernel Engineering

In this class we discuss some results and open problems related to the construction and choice of the appropriate kernel functions for Support Vector Machines and Regularization Networks.

### Applications to Computer Vision and Computer Graphics

This class will describe some applications, among those developed at CBCL, relevant to Computer Vision and Computer Graphics:

- Classifying gender from face images
- Analyzing and synthesizing images
- Learning object detection

The first topic is about the use of a very simple HyperBF network to classify face images as male or female. After training, the centers of the network come to resemble caricatures of male and female faces.

The second topic describes how to train networks to analyze or generate new images of the same or similar object - such as a face - in terms of user defined control parameters such as viewpoint or expression. The key element is a representation of images that ensures a sufficient degree of smoothness between inputs and outputs.

The last topic is about a trainable object detection system using at its core a Support Vector Machine classifier.

### Neuroscience I

One of the main scientific questions associated with the computer vision problems that we have seen in a previous class concerns the mechanisms and strategies underlying visual learning and object recognition in human perception. We will describe ongoing work, suggested by the computational schemes described earlier, which shows that several visual tasks can be learned from a set of associations. In particular, the perception of shape-from-image can be determined by experience in a top-down fashion.

### Neuroscience II

We will describe in some detail psychophysics and physiology of object recognition. Infra-Temporal cells become view-tuned to specific objects and may represent the basic modules that our view-based models - directly suggested by the learning-from-examples framework - require.

### Current Topics of Research II: Approximation Error and Approximation Theory

This class, taught by the guest speaker, is devoted to the study of the approximation error, and some of its general properties. We will present the well known phenomenon of “the curse of dimensionality” and show that, when the dimensionality of the inputs is high, the numbers of units and samples that are needed to guarantee good results are huge, unless we impose some restrictions on the class of function to be approximated.

### Current Topics of Research III: Theory and Implementation of Support Vector Machines

This class, taught by the guest speaker, is devoted to the optimization problems underlying the implementation of Support Vector Machines. The primal and dual formulations are derived and the main problems and issues arising in the implementation of the associated QPs discussed at length.

### Current Topics of Research IV: Feature Selection with Support Vector Machines and Bioinformatics Applications

This class, taught by the guest speaker, is devoted to the application of statistical learning techniques to bioinformatics applications. In particular methods for confidence estimation and feature selection with Support Vector Machines will be described.

### Current Topics of Research V: Bagging and Boosting

We discuss **bagging** and **boosting** and suggest some plausible justification for their success. We also describe some recent work about combining SVMs in a way similar to bagging.

### Selected Topic: Wavelets and Frames

Wavelets, an approximation technique that has received increasing attention in the last decade, are briefly reviewed. The basic ideas and motivations underlying the wavelet approach will be given, together with some examples. Then we introduce the basics of the theory of frames, which intuitively correspond to over complete, non-orthogonal systems of basis functions.
**
Project Presentation:** This final class is devoted to the presentation of the class projects.
