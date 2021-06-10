# Thin_Slice_Sampling

## Overview

## Prerequisites
* Access mother-infant video data from ALSPAC and GiW. 
* Code interactions using Observer XT, and extract data in .xlsx format.

## Code
All code is written in Python 3.0 and modules used are pandas, NumPy, datetime and SciPy.

The complete set of files used in these analyses are described below.

* **coding_scheme.py**: defines the MHINT coding scheme used to code the interaction data, for use in other files.
* **reformat.py**: used to process and reformat the raw interaction files. 
* **dataframes.py**: defines large dataframes used to store transition matrices and stationary distributions.
* **markov_func.py**: defines functions *MarkovTime* and *Station*, used to calculate transition matrices and stationary distributions for each thin slice.
* **extract_measures.py**: the main data processing file; takes interaction data as an input, and outputs behavioural frequencies and associated correlations, plus transition matrices and stationary distributions, for each of the 14 thin slices.
* **transition_analyses.py**: used for processing transition matrices; takes transition data as an input, outputs 1) a box plot of absolute differences between thin slice and full-session transition matrices, and 2) a table comprised of associated chi square analyses.
* **stationary_analyses.py**: used for processing stationary distributions; takes distribution data as an input, outputs 1) a box plot of absolute differences between thin slice and full-session stationary distributions, and 2) a table comprised of associated chi square analyses.
