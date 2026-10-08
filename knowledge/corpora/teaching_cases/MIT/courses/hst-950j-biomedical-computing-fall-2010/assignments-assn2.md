> 检索摘要：HST.950J Biomedical Computing（Fall 2010，Graduate）的「Assignments Assignment 2: Extracting Meaning from Text」。页内标题：Assignments Assignment 2: Extracting Meaning from Text；Installing Boostexter；Installing on Windows；Running Boostexter；Binary Classification；Multi-Class, Multi-Label Learning。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/hst-950j-biomedical-computing-fall-2010/pages/assignments/assn2/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments Assignment 2: Extracting Meaning from Text

This problem set asks you to run a relatively simple machine learning algorithm that is designed to work well with text extraction problems on some of the textual data that you encountered in homework assignment 1. The algorithm, called *BoosTexter*, is described in the following paper:

Schapire, Robert E., and Yoram Singer. “BoosTexter: A Boosting-based System for Text Categorization.” *Machine Learning* 39 (2000). ([PDF](http://www.cis.upenn.edu/~mkearns/finread/boostexter.pdf))

### Installing Boostexter

The program that implements these algorithms is available for download and should run on all common operating system from the following URL: [http://www.research.att.com/~gsf/cgi-bin/download.cgi?action=list&name=boostexter](http://www.research.att.com/~gsf/cgi-bin/download.cgi?action=list&name=boostexter).

This gives you the option of selecting implementations compiled for various flavors of Unix, Windows (32-bit) and Mac OS X. There is an odd method for agreeing to the license agreement, which involves clicking on “Cancel” when you get a dialog box asking for a username and password, so you can see the license agreement and retrieve the username and password you need. If you then refresh your browser window, it will again ask for the username/password that you just got. For me, this failed when using Safari on a Mac, but worked in Firefox. Your mileage may vary.

### Installing on Windows

Running Boostexter on Windows poses an additional challenge because it really is a Unix program. According to its documentation, it should be possible to run the program under Cygwin, which is a common Unix-like shell environment that is often installed on Windows machines. Unfortunately, our experience actually trying to make this work has been dismal. Jacinda Shelly, a former student in the class, has helped greatly and figured out that the program will run under AT&T’s uwin-base (aka ksh) environment. Here are her instructions for making this work on a Windows XP installation:

1. Download uwin at this Web site: [http://www.research.att.com/~gsf/cgi-bin/download.cgi?action=list&name=uwin-base](http://www.research.att.com/~gsf/cgi-bin/download.cgi?action=list&name=uwin-base)
2. Double-click the .exe file and install it. It might say installation failed (it did for mine, but the program still works). Ignore unless the following steps don’t work.
3. Download the win32 version of Boostexter from the link given above (choosing the win32 version)
4. Open uwin (which appeared as ksh on my desktop after installation) and navigate to the directory where you downloaded the boostexter executable. Use the following command to unzip: gunzip -c boostexter.2001-04-30.win32.tar.gz | tar xvf -
5. Go to the new Boostexter 2_1 directory.
6. The command is boostexter.exe [Parameters] (example output below).

I hope this helps! I’m glad it’s working now. The only annoying part about uwin is that up and down arrow keys will only let you reuse a command, not edit it (at least on my machine).

$ boostexter.exe -n 10 -W 1 -N ngram -S sample -V

Copyright 2001 AT&T. All rights reserved.

Weak Learner parameters:

-———————–

Window = 1

Classes = all

Expert = NGRAM

goal-in-life:be

C0: -1.199 0.168 0.168

C1: 0.549 -0.549 -0.549

rnd 1: wh-err= 0.724633 th-err= 0.724633 test= 1.0000000 train= 0.3333333

…

If at all feasible, I would encourage you to run under some Unix-like OS, such as Linux or Mac OS X.

### Running Boostexter

Once you have downloaded the program, look at the README file to see how to run it and to interpret the outputs, and the “sample.*” files to see examples of the input formats needed for the program. Note that the input texts to boostexter must not contain commas, periods or line breaks, because they are part of the formatting of the input files. In addition, I have discovered by the sad experience of having the program go into infinite loops that other symbols listed in *text-replacements* (in the Lisp code) also cause problems: colons and percent signs. These have all been substituted by upper-case symbols in the texts above.

### Binary Classification

Using the dmss data, try building models using BoosTexter to classify the cases based on text unigrams, bigrams, trigrams, etc., appearing in the data. Note that the parameters -W and -N control the types of features used in learning, and the -n option controls how many rounds of boosting are performed (roughly, how many features are selected). The -l and -z parameters select variations on the algorithm, as described in the paper. If you use the -V option, you can see the features being selected as the program runs. In any case, you can examine the file dmss.shyp after running boostexter to see the model that was generated. The distributed README file explains how to understand these. That document also shows how to run a trained model against the dmss.test data, to see how well it performs on data other than the set it was trained on.

1. Based on your experience, what combination of parameters gives you the best performance on this problem?
2. Look at the specific features used in your model(s) and comment on whether these seem to “make sense” independent of their contribution to program performance.
3. What do you think are the fundamental trade-offs in using fairly generic features such as unigrams vs. much more specific ones such as, say, trigrams.
4. When doing a “train once, test once” experiment, there is always some risk that you might have chosen a model that just happens to work very well or very poorly, by chance. Often people perform cross-validation studies, where they will split the total data set (e.g., dmss.data + dmss.test) into different (randomly selected) subsets on which to train and test with the same parameters. This method can be used to explore the robustness of the method selected or can be used to optimize the choice of training parameters. For the optimization task, it is typical to further subdivide the training set into development and validation subsets (in several different ways), then to train on each development set, test on its corresponding validation set, and choose the parameter setting that optimizes performance across these trials. Then you can train on the entire training set with those parameters and finally test against the test set. Perform a (limited) set of such cross-validation experiments to get a better understanding of what kinds of models perform best on this (relatively easy) task.

*Note*: If the goal of cross-validation is not to optimize parameters but to explore the robustness of a single chosen method, it’s possible to use the entire training + test set in cross-validation. However, it’s very important yet tricky to assure that one does not “corrupt” the final evaluation results when allowing the test data set to participate in any of the training tasks.

### Multi-Class, Multi-Label Learning

As described above, the hw2.* files contain notes with (possibly) multiple labels, from a list of 21 relatively common problems in the CWS. Nevertheless, the most common of these occurs nearly 50 times, and the least common only 4 times in the data set. Thus, the resulting classification problem is harder.

1. Try the same experiments with this data set that you did in the binary classification task, and compare the results on these data. Try to draw parallels between this data set and the original.
2. What were your expectations, and were they fulfilled?
3. *(Extra credit.)* Boostexter is able to use additional types of fields, not just text, in building its classification models. You could try to create new data sets that include not just a single text field as the basis for classification, but also other data from the CWS, such as age, gender, specific lab values, etc. How does the addition of such structured data affect the performance of boostexter?
