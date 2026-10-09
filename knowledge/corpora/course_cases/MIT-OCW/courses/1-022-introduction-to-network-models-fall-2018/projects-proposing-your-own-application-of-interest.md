- Source: https://ocw.mit.edu/courses/1-022-introduction-to-network-models-fall-2018/pages/final-project/proposing-your-own-application-of-interest/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Final Project Proposing Your Own Application of Interest

You have the option of proposing your own application of interest for the project. To do so, you will first need to write a short one-page proposal:

- Briefy describe the application in mind and the model you want to use (this could be a reference to a paper on the topic from which you want to use the model).
- Specify the dataset you want to work with (with the link to the dataset).
- Discuss what you want to do with the data.

You should email your proposal to both the Teaching Assistant and instructor by Lecture 18. Be sure to specify your research question (Part II) and your proposed approach (Part III). Don’t worry about the bumps that you may face by going with your own project, we will help you get it done. If the findings are novel and interesting, it can result in some publication and you can continue working on it as a paid job at the [MIT Institute for Data, Systems, and Society (IDSS)](https://idss.mit.edu/) over the summer.

Here are some papers (and ideas based on them) that may help you come up with an idea for your proposal:

- Battiston et al. (2012) [*DebtRank: Too Central to Fail? Financial Networks, the FED and Systemic Risk*](https://www.nature.com/articles/srep00541).

Analyze inter-bank connection to understand how the network (for example, distribution of degrees, centralities, …) changes with the state of the economy (e.g., in a volatile economy like 2008 versus a more stable economy in the years before). Consider the systemic risk in the network such as how defaults would spread from bank to bank. Does it depend on the centrality of the defaulting banks or the underlying network structure? A good database for this idea is provided by the [International Monetary Fund](https://www.imf.org/en/Data) website.

- Akbarpour et al. (2018) [*Just a Few Seeds More: Value of Network Information for Diffusion (PDF)*](http://web.stanford.edu/~mohamwad/NetworkSeeding.pdf).

Given some novel information and a social network, which individuals would you inform in order to maximize its spread if you can only contact a few people? First de fine an underlying model of diffusion for a network and then compare several seeding strategies for different realistic networks. Compare their performance and its dependence on the underlying network structure and diffusion model. Does it make sense to use centrality-based measures, or exploit the friendship paradox? How do these strategies compare to random seeding?

- Shah and Zaman (2011) [*Rumors in a Network: Who’s the Culprit? (PDF - 1.2MB)*](https://devavrat.mit.edu/wp-content/uploads/2017/10/Rumors-in-a-network-whos-the-culprit.pdf).

Consider a rumor that originates at a single node and spreads through a network. If you only observe the end result of the spread (which nodes end up hearing the rumor), can you come up with an algorithm to determine which node initiated the rumor? This paper proposes an algorithm based on what they call rumor centrality. See if you can apply it to some realistic or simulated networks. Propose alternative algorithms and test their performance.

You can also look at the datasets available at the following databases to come up with an idea:

- [The Colorado Index of Complex Networks (ICON)](https://icon.colorado.edu/)
- [The Koblenz Network Collection (KONECT)](https://dl.acm.org/doi/10.1145/2487788.2488173)
- [Stanford Large Network Dataset Collection](http://snap.stanford.edu/data/index.html)

### Timeline

Each individual (or group if you are working with someone else) will have to write and submit a report along with their Python code.<sup>1</sup> The report should describe the motivation of your project, the network dataset, the descriptive information from Part I, the research question, model and thesis from Part II, and fi nally your approach and results from Part III. The Part I descriptive write-up will be due before the fi nal report, in order to make sure everyone is on track. You will also have to give a 15 minute presentation on your project during the last week of class. There will be the following deadlines.

- Lecture 21: Part I descriptive write-up.
- Lecture 25: Oral Presentation (15 minutes).
- One week after Lecture 25: Final project report (including all code).

<sup>1</sup>You may use other programming languages, while Python is preferred.
