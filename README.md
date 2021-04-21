# Classifying hyperfocused 12-arcs

This repository contains code used in the project of Philip DeOrsey, Stephen Hartke, and Jason Williford to classify hyperfocused 12-arcs.  The code consists of two Python 3 scripts that examine the nonisomorphic 1-factorizations of K<sub>12</sub>.

The input is a list of the nonisomorphic 1-factorization of K<sub>12</sub> provided by Kaski and Östergård.  They generated the list in their work generating the nonisomorphic 1-factorizations of K<sub>14</sub>.

Petteri Kaski and Patric R. J. Östergård. There are 1,132,835,421,602,062,347 nonisomorphic one-factorizations of $K_{14}$. Journal of Combinatorial Designs, 17 (2009), no. 2, 147-159.
[DOI](https://doi.org/10.1002/jcd.20188)

### Running the scripts

From a `bash` shell, the following commands will run the scripts:

```
    bzcat k12-1f.bz2 | python filter_using_C4_condition.py - filtered_with_C4.txt
    python filter_using_2K4me_condition.py filtered_with_C4.txt filtered_with_C4_and_2K4me.txt
```

The `filter_using_C4_condition.py` script takes about 40 hours to run.
It took 39.6 hours on an Intel Xeon E5-2695 v4 2.10GHz processor running Ubuntu 18.04.5 LTS.
The `filter_using_2K4me_condition.py` script takes less than 30 seconds.
