- Source: https://ocw.mit.edu/courses/hst-950j-medical-computing-spring-2003/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

The last four class sessions will be an opportunity for students to present the results of significant research projects done for the class. We encourage you to team up (in teams of two or three students) to work on projects, and teams that span students with different interests, skills and approaches are encouraged. Below is a set of example projects for the final project. Some of these were prior final projects.

1. Calculate which documents at Pubmed (see [http://www.ncbi.nlm.nih.gov](http://www.ncbi.nlm.nih.gov)) are the closest to any patient’s context based on a problem list. You can use the problem list from the Clinician’s Workstation database (an available clinical database for the class).
2. Use the Gene Ontology nomenclature to cluster gene results in a microarray experiment based on how close two genes are in the literature citing them.
3. Translate the CWS (or other clinical database) relational database into an XML stream and re-constitute the data in a better normalized data model. Compare your effort and results when the “better” data model is a generic model vs. one containing many distinct tables.
4. Implement role-based access to the CWS (or other clinical database). Implement cryptographic authentication. Describe the weaknesses of your approach and how you would compromise privacy in your system if you were a medical knave.
5. How will patients understand the meaning of a polymorphism/mutation that they were just “diagnosed” with? Create a web-enabled script that given a locus link ID returns all the gene polymorphisms, OMIM citations associated with that gene. Then automatically scour the entire web and pubmed to find consumer-oriented (i.e. plain English) explanations of information that would help a patient understand the meaning of a polymorphism/mutation of a particular gene.
6. Given a microarray data set, articulate all the sources of error in measurement and find them in the particular data set. How will these errors affect the conclusions of the paper based on these results? Can you estimate a probability distribution of errors across the microarray surface? Find microarrays in a data set which are outliers in this distribution. Illustrate these analyses with two-dimensional surface plots/error surfaces.
7. Calculate the distibution of the melting temperature of the oligonucleotide probe sets that Affymetrix uses for its microarrays. Determine the relationship between the measured variability of gene expression in one or more data sets and the variation of the melting temperature within a probe set. Can you identify a subset of probes which reduce variability for a probe set? How does using ONLY those reduced variability probe sets affect the classification task for which the data set was originally used?
8. Develop a set of tools to de-identify sensitive medical records by finding and replacing data that appear to identify the patient, such as names, nicknames, various identification numbers, addresses, phone numbers, etc.
9. Use simple natural language techniques to extract interesting coded aspects of the medical record from unstructured text. For example, find all mention of medications, dosages, routes of administration, etc. Another example would be to try to determine by textual analysis whether the description of a patient might be consistent with some specific disease of public health interest (ranging from meningitis to anthrax).

This list is meant only to be suggestive. Any reasonable project of roughly the above level of sophistication will be welcome. We ask you to submit a proposal by Lecture 17 that describes the proposed project in enough detail that we can critique it. It should also identify the group of people (we suggest 2-3) who will work together on the project.
