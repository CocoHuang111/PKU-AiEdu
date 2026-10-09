- Source: https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

### Homework 1

#### Problem 1: The Charles Book Club Case

Read the case and answer all the questions at the end of the case.

Readings:

Bhandari, Vinni, and Dr. Nitin Patel. *“The Charles Book Club Case*”

Levin, Nissan, and Jacob Zahav. *“A Case Study in Database Marketing*.” Tel Aviv University. Direct Marketing Educational Foundation, Inc.. March 1995.

Association of American Publishers. *Industry Statistics, 2002.*

#### Art History of Florence

A new title, “The Art History of Florence”, is ready for release. CBC has sent a test mailing to a random sample of 4,000 customers from its customer base. The customer responses have been collated with past purchase data. The data has been randomly partitioned into 3 parts- Training Data (1800 customers): initial data to be used to fit response models, Validation Data (1400 customers): hold-out data used to compare the performance of different response models, and Test Data (800 Customers): data only to be used after a final model has been selected to estimate the likely accuracy of the model when it is deployed. The Sample Data are in a separate spreadsheets**CBC_4000.xls** ([XLS](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/resources/cbc_4000/)). Each row (or case) in the spreadsheet (other than the header) corresponds to one market test customer. Each column is a variable with the header row giving the name of the variable. The variable names and descriptions are given in Table 1, below:

#### Table 1: List of Variables in CBC_4000.xls

| Variable Names | Descriptions |
| --- | --- |
| Seq# | Sequence number in the partition |
| ID# | Identification number in the full (unpartitioned) market test data set |
| Gender | O=Male, 1=Female |
| M | Monetary- Total money spent on books |
| R | Recency- Months since last purchase |
| F | Frequency - Total number of purchases |
| FirstPurch | Months since first purchase |
| ChildBks | Number of purchases from the category: Child books |
| YouthBks | Number of purchases from the category: Youth books |
| CookBks | Number of purchases from the category: Cookbooks |
| DoItYBks | Number of purchases from the category Do It Yourself books |
| RefBks | Number of purchases from the category: Reference books (Atlases, Encyclopedias, Dictionaries) |
| ArtBks | Number of purchases from the category: Art books |
| GeoBks | Number of purchases from the category: Geography books |
| ItalCook | Number of purchases of book title: “Secrets of Italian Cooking.” |
| ItalAtlas | Number of purchases of book title: “Historical Atlas of Italy.” |
| ItalArt | Number of purchases of book title: “Italian Art.” |
| Florence | =1 “The Art History of Florence.” was bought, <br> =0 if not |
| Related purchase | Number of related books purchased |

#### Problem 2: The German Credit Case

Read the case and answer all the questions at the end ([PDF](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/resources/germancredit-1/))

German Credit Case Data ([XLS](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/resources/germancredit/))

### Homework 2

#### Problem 1:

A common application of Discriminant Analysis is the classification of bonds into various bond rating classes. These ratings are intended to reflect the risk of the bond and influence the cost of borrowing for companies that issue bonds. Various financial ratios culled from annual reports are often used to help determine a company’s bond rating.

The Excel spreadsheet **BondRatingProb1.xls** ([XLS](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/resources/romybondratingprob1/))contains two sheets named Training data and Validation data. These are data from a sample of 95 companies selected from COMPUSTAT financial data tapes. The company bonds have been classified by Moody’s Bond Ratings (1980) into seven classes of risk ranging from AAA, the safest, to C, the most risky. The data include ten financial variables for each company. These are:

LOPMAR: Logarithm of the operating margin,
LFIXMAR: Logarithm of the pretax fixed charge coverage,
LTDCAP: Long-term debt to capitalization,
LGERRAT: Logarithm of total long-term debt to total equity,
LLEVER: Logarithm of the leverage,
LCASHLTD: Logarithm of the cash flow to long-term debt,
LACIDRAT: Logarithm of the acid test ratio,
LCURRAT: Logarithm of the current assets to current liabilities,
LRECTURN: Logarithm of the receivable turnover,
LASSLTD: Logarithm of the net tangible assets to long-term debt.

The data are divided into 81 observations in the Training data sheet and 14 observations in the Validation data sheet. The bond ratings have been coded into numbers in the column with the title CODERTG, with AAA coded as 1, AA as 2, etc. Use XLMiner to develop Discriminant Analysis and Neural Networks models to classify the bonds in the Validation data sheet. You will need to use the score new data option. What is the performance of the best classifier you have been able to find? Notice that the there is order in the class variables (i.e., AAA is better than AA, which is better than A,…). Would certain misclassification errors be worse than others? If so, how would you suggested measuring this?

#### Problem 2:

Give true false answers to the following questions with one sentence to justify your answer.

1. The adjusted R2 value for a set of independent variables in multiple linear regression is always less than the value of R2.
2. The most promising subsets of variables to include in a multiple linear regression model are those that have few variables and have a high value for Mallow’s Cp.
3. An Artificial Neural Network with no hidden layers is used to predict a continuous variable y using p input variables, x1, x2 … xp. The network is trained on a training dataset and it is found that the sum of squared errors on a validation dataset is SSN. A multiple linear regression model with independent variables x1, x2 … xp and dependent variable y is fitted to the same validation data. The sum of squared residuals for the regression model is SSR. SSR cannot be greater than SSN.
4. The backprop algorithm when used in training an Artificial Neural Network will always terminate at a global or local minimum of the error function.
5. The number of variables used in training an Artificial Neural Network is equal to the total number of nodes in the network.

#### Problem 3:

The Excel spreadsheet **RegressionProb3.xls** ([XLS](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/resources/romyregressionprob3/)) contains two sheets named Training Data and Validation Data. We will use XLMiner to build two models with the training data and then use the validation data to compare their performance as prediction models.

1. Fit a multiple regression model, Model1, to the training data using all the variables X1 through X9 (and the constant term). Call the coefficient vector for this model ß**1**.
2. Use the subset selection options in XLMiner to choose a model using only the training data. Call the coefficient vector for this model ß**2**.
3. Use the Validation Data to compute the mean and the standard deviation of errors for Model1 by copying ß**1** into cells B5 through K5. Do the same for Model2 by copyingß**2**.
4. Compare the models in terms of (i) bias in the predictions, (ii) mean square error of predictions.

#### Problem 4:

The Excel spreadsheet **NormalsProb4.xls** ([XLS](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/resources/romybivarnormprob4/)) contains 1000 observations with two groups (Group 0 and Group 1) and two variables (x and y).

1. Plot all the data points in a 2-dimensional scatter plot. Mark Group 1 points and Group 0 points differently (e.g., one with a ‘x’ and the other with ‘o’) so you can visualize the distribution of the points of each Group.
2. Partition the data into training and classification sets with 600 and 400 observations respectively.
3. Compare the performance of:
  - Logistic Regression
  - Discriminant Analysis
  - Neural Nets
  - K-Nearest Neighbor ClassifiersRemember that logistic regression and discriminant analysis are linear classifiers - i.e., it separates points of different classes with a plane. In contrast, neural networks and k-nearest neighbors allow non-linear classifiers (do you have an intuitive idea on the geometry of how the latter two classifies points?).
4. For each method, plot a scatter plot for the best classifier. On each plot, display the following series
  - Group 0 points that are classified correctly,
  - Group 0 points that are misclassified,
  - Group 1 points that are classified correctly,
  - Group 1 points that are misclassified.
5. The data was simulated. The (x,y) values for each class follow a bivariate normal distribution. The Bayes Rule for minimum misclassification has an error rate of 18.5%. How close is the best classifier you have developed of each type to this error rate? Give an intuitive explanation of why certain types of classifiers seem to be better for this data.
