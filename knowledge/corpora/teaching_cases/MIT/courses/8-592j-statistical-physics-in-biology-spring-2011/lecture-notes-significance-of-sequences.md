> 检索摘要：8.592J Statistical Physics in Biology（Spring 2011，Graduate）的「Lecture Notes Significance of Alignments」。页内标题：Lecture Notes Significance of Alignments。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/8-592j-statistical-physics-in-biology-spring-2011/pages/lecture-notes/significance-of-sequences/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Lecture Notes Significance of Alignments

1. [Sequence alignment](http://www.ncbi.nlm.nih.gov/BLAST/tutorial/Altschul-1.html)
  - Inputs:
    - *Explicit*—Two sequences {a1, a2, …., am} and {b1, b2, …., bn} (e.g. query and database)
    - *Implicit*—A scoring procedure, e.g. pairwise scores s(ai,bj) and gap costs
  - Alignment algorithm: global, local, gapped, gapless (dynamic programming, applet)
  - Output: matching (sub)sequences with an overall score S . ([example](http://en.wikipedia.org/wiki/File:Zinc-finger-dot-plot.png))
  - Significance: What is the probability of getting a score S by chance?
2. Statistics of gapless local alignments:
  - Random walks of scores as a function of matching length
  - [Extreme Value Distributions](http://mathworld.wolfram.com/ExtremeValueDistribution.html), the [Gumbel distribution](http://www.itl.nist.gov/div898/handbook/eda/section3/eda366g.htm)
  - Tails of distribution in a [gapless alignment](http://online.itp.ucsb.edu/online/infobio01/altschul/)
  - The Karlin-Dembo formula
3. Gapped alignments and Statistical Physics
  - Transfer Matrix method for [Directed Paths in Random Media (PDF)](https://arxiv.org/pdf/cond-mat/9411022.pdf)

- [Tutorial by Ralf Bundschuh](http://online.itp.ucsb.edu/online/infobio01/bundschuh/) on Sequence Alignment (and [associated paper](http://pre.aps.org/abstract/PRE/v65/i3/e031911))

([Detailed Lecture Notes (PDF)](https://ocw.mit.edu/courses/8-592j-statistical-physics-in-biology-spring-2011/resources/mit8_592js11_lec8/))
