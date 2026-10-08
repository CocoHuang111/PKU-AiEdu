> 检索摘要：HST.508 Quantitative Genomics（Fall 2005，Graduate）的「Projects」。页内标题：Projects；Final Project Assignments；Project Assignments by Prof. Leonid Mirny；Identification of Specificity - Determining Residues；Project Assignments by Dr. Alvin Kho and Prof. Isaac Kohane；Project 1；Project 2；Project 3；Project Assignments by Prof. Sunyaev (Courtesy of Prof. Shamil R. Sunyaev. Used with permission.)；Positive Selection in Human Genes；Discovering New Protein Domain (and Naming it After Your Pet) by Prof. Sunyaev and Prof. Mirny；Predicting New Exons Using Multiple Genomes。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/hst-508-quantitative-genomics-fall-2005/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### Final Project Assignments

Students select one of the following project assignments and present their results to the class at the end of the term. Oral presentations should last 15 minutes in addition to a 5 minute question and answer session with the class.

### Project Assignments by Prof. Leonid Mirny

New experimental evidences suggest that gene’s location inside a nucleus is critical for its regulation and transcription. Genes that are close in space can be easily co-regulated, while those that are distant maybe hard to co-regulate. Genes that are close on the chromosome are close in space inside the nucleus and hence could be co-regulated. Correlation between genes’ proximity and co-expression has been reported earlier (e.g. see papers by K. Wolfe). Here your goal is to go beyond simple correlation, to establish:

- At what genomic distance two proximal genes can be co-expressed.
- Whether genes that are distant can be co-regulated as precisely as genes that are proximal.
- Identify pairs/groups of yeast genes that are co-localized and co-expressed in several yeast species.

1. Download expression data, genomes and gene coordinates for several yeast species. Using TRANSFAC database identify regulons in *S. cerevisiae* as groups of genes regulated by the same transcription factor or same set of transcription factors. Test whether regulons tend to be co-expressed and co-localized (i.e. proximal on the chromosome). Now compute co-expression as a function of distance between two genes of the same regulon. Repeat for several regulons in several species. Plot co-expression as a function of distance. Do you see a drop in co-expression at a certain distance between two genes?
2. Using expression and gene coordinates for several yeast species, compute co-expression for pairs of genes. Compare genes that are precisely co-expressed. Do you see that precise co-expression requires genes’ proximity? What is the fraction of proximal genes among highly co-expressed vs. moderately co-expressed? At what distance between the genes the effect of proximity on expression diminishes?
3. Your goal is to identify pairs of yeast genes that are proximal to each other in all (or most) yeast genomes. You can find these genes using gene coordinates and lists of orthologs. You will have to develop some statistics to estimate significance of conserved proximity. Do genes that have conserved proximity tend to be co-expressed (as compared to genes that are proximal only in one of the genomes)? You may want to consider separately pairs of genes that remain proximal while having different relative orientation in different genomes.

#### Identification of Specificity - Determining Residues

Proteins have to recognize and bind their targets. A small group of residues could be responsible for specific recognition. These residues are called specificity-determining residues (SDRs). Analysis of other proteins with different specificity from the same organism (paralogs) and proteins with the same specificity in other organisms (orthologs) allows to predict SDRs (see papers by Gelfand and Mirny). We hypothesize that SDRs must be responsible for formation of hetero-and homodimers. Your goal is to test this hypothesis on coiled-coils and epidermal growth factor receptors (EGFR).

- Fos-Jun hetero-dimerization. Fos and Jun form a stable hetero-dimer whose coiled-coil structure is known. Eight amino acids had been suggested as primary determinants of Fos-Jun specificity (O’Shea et al 1992). Your goal is to predict SDRs for Fos and Jun and compare your predictions with
  1. The structure of the complex.
  2. Published experimental results.
- SDRs in hetero-dimers of EGFR. EGFR is a family of receptor tyrosine kinase that regulates cell proliferation and differentiation. Consider four important receptors Erb-1, 2, 3, 4 of the EGFR family that are generally present as heterodimers. Identify SDRs in the L-domain of these receptors. By examining the structure of the receptor
  1. suggest SDRs involved in heterodimerization of EGFRs, and
  2. SDRs that are likely to be important for recognition of the ligand. Compare your predictions with the literature.

### Project Assignments by Dr. Alvin Kho and Prof. Isaac Kohane

#### Project 1

Let P be a morphogenic protein, and S a (near) homogeneous population of cells which are P-responsive. Namely, S cells undergo observable changes in some phenotype in response to P after a specific time period T (A possible phenotypic transformation could be that S grows more heterogeneous). The negative control experiment is S subject to a vehicle protein C for the same length of time T. The general objective is to characterize the direct and indirect downstream molecular cascade/s of P in S, bioinformatically. The experimental data consists of transcriptome profiles of S under the conditions described above measured by micro array. An independent source of supplementary material may be the public BIND or DIP database of curated/predicted protein-protein interactions.

Some questions:

1. What is the (predicted) amino acid sequence binding motif of P, and what are proteins/RNA species that might interact (namely, bind) with P? Do RNA corresponding to these (putatively) P-binding proteins possess a common regulatory pattern of expression in the transcriptome dataset?
2. Given the above experiment design, design and justify a rationale method to decouple direct from indirect substrate elements of P.
3. Are the RNA species which are up- or down-regulated under influence of P enriched for specific ontologic categories (biological/molecular functions, cellular localization), or share common sequence motifs?
4. Real dataset: Mouse cerebellar granule cells (neuronal precursors) under influence of sonic hedgehog protein at three time points: 1h, 3h, and 24h, with corresponding negative (vehicle) controls. Micro ray derived transcriptome profiles.

#### Project 2

Let B and T be developmental transcriptome profiles (“time series”) of mouse B and T cells respectively (>4 developmental stages each, measurement/biological replicates at each stage), measured by micro arrays.

The general objective is to find genes whose time profiles distinguish between B and T cell development, and/or gene pairs whose pair wise dissimilarity measure are different in the B versus T datasets. For example, genes G1 and G2 are close to one another (belong to a common cluster/partition C1) in B, but G1 and G2 are distant from one another (belong to disjoint clusters/partitions) in the T.

Some questions:

1. What is a reasonable dissimilarity measure to use in this problem? Or a measure of cluster / partition membership discrepancies between B and T?
2. How does the distribution of dissimilarity measures between all gene pairs look like? Are gene (pairs) at the tail ends of the distribution enriched for specific ontologic categories, chromosomal loci/location, or sequential motifs? For example, is there a higher likelihood for gene pairs which occupy common loci to live in the same clusters in B and T?
3. Dataset B: [GDS44](http://www.ncbi.nlm.nih.gov/geo/gds/gds_browse.cgi?gds=44) and [GDS52](http://www.ncbi.nlm.nih.gov/geo/gds/gds_browse.cgi?gds=52). Dataset T: [GDS237](http://www.ncbi.nlm.nih.gov/geo/gds/gds_browse.cgi?gds=237) and [GDS257](http://www.ncbi.nlm.nih.gov/geo/gds/gds_browse.cgi?gds=257).

#### Project 3

Bioinformatically characterize in trisomy 21 transcriptome datasets the interactions between presence of an extra chromosome 21 and loci of non-21 chromosomes in mouse and human. The general question is to assess the likelihood of an extra Chr: 21 affecting homologous genes in human and mouse, and to check whether a gene’s chromosomal location is a modulating factor in its interaction with a Chr: 21 gene. Construct and justify a rational approach to resolving this problem.

1. Human trisomy 21, [GSE1397](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE1397) mouse trisomy 21, [GDS681](http://www.ncbi.nlm.nih.gov/geo/gds/gds_browse.cgi?gds=681) [GDS682](http://www.ncbi.nlm.nih.gov/geo/gds/gds_browse.cgi?gds=682)

### Project Assignments by Prof. Sunyaev (Courtesy of Prof. Shamil R. Sunyaev. Used with permission.)

#### Positive Selection in Human Genes

Several recent papers claim that some genes have multiple amino acid replacements driven by positive selection after divergence of human and chimpanzee lineages. It was suggested earlier that pattern of amino acid substitutions in genes under positive selection differs from other genes. The goal of this project is to compare patterns of amino acid replacements in genes showing signs of positive selection. You can take any subset of genes evolving under positive selection from any of the papers below. To find substitutions you can compare human proteins to chimpanzee genomes using tblastn (to obtain translated alignments). Alternatively, you can translate alignments from Clark et al. 2003 (Science 302:1960-3). It is very important to exclude any doubtful alignments and gene annotations. There are three questions to be answered:

1. Are there statistically significant differences in patterns of amino acid replacements in genes evolving under positive selection?
2. Are amino acid substitutions in these genes more radical or more conservative?
3. What are possible interpretations of the results?

#### Discovering New Protein Domain (and Naming it After Your Pet) by Prof. Sunyaev and Prof. Mirny

Many proteins that contain well-annotated domains also contain sequence regions that do not correspond to any known domains or sequence motifs. Some domains can be evolving fast which makes difficult their identification as conserved mobile sequence elements. This project is based on the hypothesis that in some cases domain organization of proteins may be conserved even if some domain sequences diverged beyond detectable level of sequence similarity. This would allow finding new domains by association with other domains (similarly to the idea of conserved gene neighborhood). The goal is to identify a novel domain (or show a lack of such) located between two known domains. First, you use existing databases to identify all proteins with the same domain organization as proteins in a given set (e.g. EGFR, insulin receptors etc). Second, you test a hypothesis that sequence regions between corresponding domains of these proteins also belong to the same uncharacterized domain. Weak sequence similarity, similarity in predicted secondary structure, length and amino acid composition should be explored.

#### Predicting New Exons Using Multiple Genomes

Currently available annotation of protein coding genes in the genome is not perfect. As a result, many genes contain cryptic exons-exons which were not properly annotated. Most frequently these exons are alternatively spliced. The aim of this project is to discriminate between protein coding exons and conserved non-coding sequence regions using comparative genomics. MultiZ alignments of mammalian genomes needed for this project can be downloaded from the UCSC genome browser. For simplicity we can use three genomes (e.g. human, mouse and dog). Coding and non-coding sequences are expected to have very different patterns of sequence changes because of the following characteristics of coding sequences: biased codon composition, higher conservation, absence of stop codons and frameshifts, higher fraction of synonymous than nonsynonymous substitutions, higher frequency of substitutions corresponding to changes of chemically similar amino acids, higher proportion of mutable contexts. All these differences can be captured explicitly if substitution pattern for tri-nucleotides in multiple genomes would be compared in coding and non-coding sequences. The project aims at estimating frequencies *f<sub>ijk</sub>* that tri-nucleotides *i*, *j* and *k* are observed in corresponding positions in human, mouse and dog genomes. These frequencies should be estimated for both coding exons in the correct frame and non-coding sequences included in the alignments. Since some *f<sub>ijk</sub>* can be very small, the use of pseudo counts may be necessary. After estimating the above frequencies, we will have to test whether an additive score of logarithmic ratio of frequencies corresponding to coding exons and frequencies corresponding to non-coding sequences can discriminate between exons and non-coding sequence.

#### Estimate Variation in Mutation Rate Along Human Genome

Mutation rate is a fundamental parameter in models of population genetics and molecular evolution. Estimation of neutral mutation rate is critical for many tests for natural selection. The purpose of this project is to test whether mutation rate is constant along the genome. Assume that the fraction of functionally important sequence in the genome is small and can be neglected. The projects will use whole genome alignment of human and chimpanzee, which can be downloaded from the UCSC genome browser. Homogeneity of mutation rate, can be estimated from variance of number of substitutions in windows of a given length. Is observed variance similar to the variance expected under the assumption of homogeneity of mutation rate along the genome for all window lengths? If mutation rate is not homogeneous along the genome, what is characteristic scale of this inhomogeneity? How does the result change if substitutions in hypermutable CpG dinucleotides were excluded?
