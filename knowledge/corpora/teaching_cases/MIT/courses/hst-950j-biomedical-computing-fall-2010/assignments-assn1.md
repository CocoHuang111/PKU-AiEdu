> 检索摘要：HST.950J Biomedical Computing（Fall 2010，Graduate）的「Assignments Assignment 1: Clinical Databases」。页内标题：Assignments Assignment 1: Clinical Databases；Part 1；Part 2。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/hst-950j-biomedical-computing-fall-2010/pages/assignments/assn1/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments Assignment 1: Clinical Databases

### Part 1

This assignment contains two parts. The first asks you to consider some of the important issues underlying the motivations for healthcare IT systems, and some of the policy issues that influence their adoption and use. Much of the material can be answered from the readings. Please give concise thoughtful answers.

1. What is an EHR? Outline the principal advantages and disadvantages, compared to a paper record.
2. From your own experience with health care and the information infrastructure that it uses, how do you think we compare in practice to the vision outlined in Shortliffe’s first chapter?
3. Discuss the relative advantages and disadvantages of unstructured text entry into an EHR vs. fully coded information.
4. Briefly describe the hypothetico-deductive method, and its relation to health care. What aspects of this do you think would be simplest and most difficult to automate using computer processing?
5. Given that nearly half of healthcare in the US is paid by CMS (Centers for Medicare and Medicaid Services) of the federal government, could CMS simply mandate that all clinical data be standardized according to one standard, stored and reported in electronic form, and thus seamlessly shared among healthcare institutions? What would be the technical medical and political consequences of such a move?
6. Some argue that it is essential to distinguish between an EHR that is meant to be shared among health care providers and a “Personal Health Record” (PHR) that is meant to inform patients and to allow them to keep track of their own diseases treatments, immunizations, medications, etc. Muster some brief arguments, for why these should be different, and some counter- argument for why they should be the same.

### Part 2

The second part of the assignment asks you to explore the organization and content of an extract of 300 patients’ data from an operational database taken in the mid-1990’s. Although these were real data, we have worked very hard to de-identify the data, so all the names, addresses, medical record numbers, etc., that you see in the database are synthesized replacements for the actual patient identities. We have also gone through all the text fields in the data and removed or replaced all such identifying information. (This process will be discussed later in the term, as part of the issue of how to use clinical data for research purposes. If you find what you believe to be true identifying data that we missed, please let us know so we can correct it; however, no such data have been found in this database in the past decade.)

Refer to the following resources to help you review or learn the relevant aspects of how contemporary relational databases work, and how they have been adapted for use in EHR’s.

1. A general primer on relational data bases and relational algebra: Date, C.J. *An Introduction to Database Systems,* *some edition earlier than 6th ed*. Addison Wesley.
2. A paper describing [normal forms in relational databases](http://www.bkent.net/Doc/simple5.htm)
3. A paper on [generic data models](http://dx.doi.org/10.1136/jamia.1996.97035024). This is in line with the currently-popular Semantic Web notion of using RDF as a general data model for any kind of data.
4. You can find any number of helpful documents on-line. For example, MySQL, a free (for non-commercial use) database is available for Windows, Mac OS and Linux systems provides extensive and handy [documentation](http://dev.mysql.com/doc/).

*Note: The following questions refer to a “scrubbed” clinical database, called cws (for Clinical Work Station). Due to residual concerns about confidentiality, the database has not been included in this publication, but the questions have been retained below for reference. As an alternative, the MIMIC II Database* ([http://www.physionet.org/mimic2/](https://archive.physionet.org/physiobank/tutorials/using-mimic2/)) *is available free of charge to qualified researchers, and contains comprehensive clinical data from thousands of Intensive Care Unit patients that has been thoroughly de-identified (all personal health information has been removed and all dates have been changed).*

You will need to have available to you a database system of some sort that accepts standard (or at least typical) SQL commands and into which you can load some version of the above data. We have found it easiest to use MySQL, for which implementations exist for Mac OS X, Windows, and various flavors of Unix/Linux. If you don’t already have MySQL server running on your system, it may be obtained and freely installed from the [MySQL download site.](http://dev.mysql.com/downloads/mysql/5.0.html)

The following questions require you to examine and explore the database:

1. The table pat_demograph has dozens of columns. Comment on the design of this table from the viewpoint of Kent’s article on relational forms.
2. The table pat_fin_acct (key to billing operations), has a column called pat_num but clearly does not have only one row per patient. What is the primary key of this table?
3. Give the SQL query to retrieve the names of all doctors in the database.
4. Suppose you are doing medical research on **Diabetes-Insipidus** and need related patient documents. Give the query for retrieving documents of patients with **Diabetes-Insipidus**.
5. Retrieve a table of the number of distinct patients who have each of the many problems listed in the problems table.
6. Give three different queries, each of which will estimate the total number of patients being tracked in the database. If they result in different numbers, discuss why. (Ignore the possibility that the same patient is entered several times but with different identifiers.)
7. Sometimes, de-normalized database structures are designed deliberately and defensibly. Consider the pat_test table, which stores with each (numerical) data value the low and high bounds of the normal range of that value. One might argu_e_ that these bounds are properties of a test, not a specific test result, and change at most infrequently, e.g., when the test equipment is re-calibrated or the chemistry of the test is altered. Nevertheless, can you defend the decision to do this in the way CWS does? If you chose an alternative design, in which these bounds data were kept in a separate table, what columns would such a table need, and what SQL expression would you use to retrieve a specific test value and its appropriate normal range?
8. (SQL challenge): Formulate a query that retrieves patients who have had a series of two or more tests in which adjacent tests yield a value that is abnormally high immediately followed by a value that is abnormally low. Produce the list of patients, which lab value, and when the two occurred. (Note: the hard part of this is making sure the values are adjacent, with no intervening valu_e_s.)
9. Consider a patient-oriented journal in which doctors will enter, at each visit, the following data: Build a data model for such a patient journal, making reasonable assumptions as necessary, and write the SQL table definitions to implement it. Also mark the key fields. Make sure you satisfy the third normal form.
  1. visit date
  2. chief complaint (unstructured text)
  3. results of exams, if performed, which include the following, but to which others may be later added
    1. physical exam
      1. pulse (beats/minute)
      2. respiration rate (breaths/minute)
      3. blood pressure (systolic and diastolic, in mmHg)
    2. total blood count
      1. red blood cell count
      2. white blood cell count
  4. Diagnosis ICD9 code)
  5. plan (unstructured text )
  6. provider name and signature
10. Johnson’s “Generic Data Modeling” paper suggests that you could use an alternative design for the relational data base, in which the attributes of an entity such as a visit are represented not all as distinct columns in the data, but as different properties of the entity, stored in a table with fewer columns but many more rows. Give a description of how you might transform your design above to such a representation.
