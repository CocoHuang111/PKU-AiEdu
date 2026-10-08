> 检索摘要：20.453J Biomedical Information Technology（Fall 2008，Graduate）的「Syllabus」。页内标题：Syllabus；Course Meeting Times；Course Description；Prerequisites；Reference Materials；Term Paper；Calendar。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/20-453j-biomedical-information-technology-fall-2008/pages/syllabus/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Syllabus

### Course Meeting Times

Lectures: 2 sessions / week, 1.5 hours / session

### Course Description

Biology and medicine are moving into a new era that is characterized as being “data-rich.” In biological research, a single laboratory can produce terabytes of data per month that needs to be shared across the research community. Drug development involves analyzing hundreds of compounds with laboratory tests that generate huge amounts of data that must be analyzed and shared. Clinical trials assay thousands of individual data elements on hundreds of patients over many time points.

The objective of this course is to provide the students with the knowledge to address these challenges. We focus on the storage, integration, querying and management of heterogeneous, voluminous, geographically dispersed biomedical data. In addition to primary data, such as experimental data, the methods also address derived data such as those from analyzed microscope images. Examples of pathway analysis methods and the sharing and storage of the data that they generate will be presented. Querying across multiple databases is described, where the databases can be as diverse as microarray experiments, curated databases compiled by domain experts, or biomedical images. Other data sources include medical records, information on disease, references to literature, and biological pathways predicting protein expression. Several current examples from biological research will be presented.

### Prerequisites

1.00 Introduction to Computers and Engineering Problem Solving; 6.001 Structure and Interpretation of Computer Programs; or experience with Web-based computing.

### Reference Materials

There is no recommended text book for this course simply because to the best of our knowledge there is no single text book available that can address the breath and depth of the issues in this course. Hence the reference materials will be lecture notes, research experience of the course instructors in biomedical data management, and a set of research papers.

### Term Paper

A term paper is required of all students. The subject of the term paper is the choice of the student, and can as examples be a driving problem in research, a new idea for managing biomedical data, or an improvement on an existing system.

### Calendar

Instructors Key:

CFD = Prof. C. Forbes Dewey, Jr. (MIT)
SSB = Prof. Sourav S. Bhowmick (NTU, Singapore)
HY = Prof. Hanry Yu (NUS, Singapore)

<table><tr><th>LEC #</th><th>TOPICS</th><th>INSTRUCTORS</th><th>KEY DATES</th></tr><tr><td colspan="4">Part 1: Introduction</td></tr><tr><td>1</td><td>Biomedical information technology today <br> - Grand challenge problems in biology and medicine <br> - The key role of information technology <br> - Semantics, ontologies, and standards <br> - Pathway modeling <br> - Term paper instructions</td><td>CFD</td><td></td></tr><tr><td colspan="4">Part 2: Biological and Medical Data</td></tr><tr><td>2</td><td>Types and characteristics of biological and medical data <br> - Distributed data systems <br> - The life cycle of scientific data <br> - Current challenges</td><td>HY</td><td>Assignment 1 out</td></tr><tr><td>3</td><td>Examples from liver fibrosis <br> - Gel electrophoresis <br> - Microarrays <br> - FACS and other methods <br> - Creating biological pathways <br> - Designing new experiments <br> - Integrating information from the literature</td><td>HY</td><td></td></tr><tr><td colspan="4">Part 3: Storing, Querying, and Integrating Biomedical Data</td></tr><tr><td>4</td><td>Data avalanche in the biomedical world and role of databases <br> - Relational data model <br> - ER modeling</td><td>SSB</td><td></td></tr><tr><td>5</td><td>Designing good database schema <br> - Functional dependencies <br> - Normalization</td><td>SSB</td><td></td></tr><tr><td>6</td><td>Querying relational databases using SQL</td><td>SSB</td><td></td></tr><tr><td>7</td><td>Querying relational databases using SQL (cont.) <br> - Limitations of relational data <br> - Introduction to semi-structured data and XML</td><td>SSB</td><td></td></tr><tr><td>8</td><td>Issues in querying XML data using XPath and XQuery <br> - XML query languages <br> - Principles of XML query processing</td><td>SSB</td><td>Assignment 1A due</td></tr><tr><td>9</td><td>Querying XML data (cont.) <br> - XML and relational databases</td><td>SSB</td><td></td></tr><tr><td>10</td><td>Querying graphs (molecular networks) <br> - Querying pathways and protein sources</td><td>SSB</td><td></td></tr><tr><td>11</td><td>Data integration without semantics <br> - Issues related to biological data integration <br> - Standards for publishing and sharing data <br> - Examples and usage such as the DICOM standard <br> - Biological databases and supporting organizations</td><td>SSB</td><td>Assignment 1B due</td></tr><tr><td colspan="4">Part 4: Ontology Management in Systems Biology</td></tr><tr><td>12</td><td>Definitions and importance of ontologies <br> - Standards for publishing and sharing ontologies (OWL, RDF) <br> - Examples and usage of ontologies in life sciences <br> - Using unique identifiers and other semantic standards</td><td>CFD</td><td></td></tr><tr><td>13</td><td>Database approach to ontology storage and inference</td><td>SSB</td><td>Assignment 2 out</td></tr><tr><td>14</td><td>Creating relational databases from ontologies <br> - OWLdb <br> - Querying databases using ontologically-based queries</td><td>CFD</td><td></td></tr><tr><td>15</td><td>Querying ontologies with SPARQL <br> - Integrating ontologies and XML query processing <br> - Role of ontology management in system biology</td><td>SSB</td><td></td></tr><tr><td colspan="4">Part 5: Biological Pathways</td></tr><tr><td>16</td><td>Modeling and computing pathways <br> - Modeling and representation of pathways (SBML, CellML) <br> - Challenges of managing disparate sources of pathways <br> - Cell designer, cytosolve, and other computational environments</td><td>CFD</td><td></td></tr><tr><td>17</td><td>Discussions with TAs related to assignments and term project</td><td></td><td></td></tr><tr><td>18</td><td>Molecular network comparisons <br> - Importance of molecular network comparison <br> - Types of network comparison <br> - Network comparison algorithms</td><td>SSB</td><td></td></tr><tr><td colspan="4">Part 6: Biological and Medical Data Integration</td></tr><tr><td>19</td><td>SWAN: An advanced architecture for sharing scientific information <br> - The stakeholders, requirements, and functionality <br> - The available technology <br> - Workflow and usability</td><td>Guest lecturer: Tim Clark, Harvard University</td><td>Assignment 2 due 3 days later</td></tr><tr><td>20</td><td>Building a distributed pathway-enabled information system for biological research <br> - Scope of the data sources and the application constraints <br> - Workflow and usability <br> - Technical considerations <br> - Accommodating the future</td><td>CFD</td><td></td></tr><tr><td colspan="4">Part 7: Grand Challenges</td></tr><tr><td>21</td><td>Predicting drug efficacy by modeling <br> - Current limits of predictability <br> - Living with incomplete data <br> - Examples of success in quantitative modeling</td><td>CFD</td><td></td></tr><tr><td>22</td><td>Revolutionizing the drug discovery pipeline <br> - The need for change <br> - Key parts of the process <br> - Quantitative modeling as a paradigm</td><td>CFD</td><td></td></tr><tr><td colspan="4">Part 8: Term Paper Presentations</td></tr><tr><td>24-26</td><td>Term paper presentations</td><td></td><td></td></tr></table>
