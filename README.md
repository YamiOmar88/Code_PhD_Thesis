# Code for PhD Thesis

**Thesis Title:**  Complex Networks in Manufacturing - Suitability and Interpretation

**Author:** Yamila Mariel Omar

**Expected Defense Date:** 8th July 2021

**Institution:** University of Luxembourg


This repository contains all the code necessary to reproduce my PhD Thesis. Find below a description of the files.

## Directories
1. `data`: The raw data used for my thesis corresponds to the `train_date.csv` file in the [Kaggle competition titled "Bosch Production Line Performance".](https://www.kaggle.com/c/bosch-production-line-performance) Semi-processed data is available in this folder instead.
2. `figures`: Some of the figures in my Thesis are available in this folder.
3. `flow_networks`: all the code corresponding to the Chapter of "Flow Networks" is available in this directory.


## Files description grouped by use

### Data cleaning
1. `from_timestamp_to_paths.py`: code used to process the train_date.csv data from Kaggle (see here) to obtain manufacturing paths and manufacturing edges.
2. `path_data_cleaning.py`: code necessary to remove "noisy" data. It produces two files: clean manufacturing paths and clean edges.

### Modules developed
1. `graphfile.py`: class used to open and write data from/to text files.
2. `graph.py`: class used to do complex network analysis.
3. `betweenness_centrality.py`: functions necessary to calculate the Betweenness centrality. Read docstrings for details.
4. `clustering_coefficient`: functions necessary to calculate the Clustering Coefficient. See docstrings for details.
5. `depth_first_search.py`: functions needed for the Depth First Search algorithm. Some functions to determine strongly connected components are also available here.
6. `pagerank.py`: functions needed to calculate the PageRank algorithm.

### How to obtain the results in the Thesis manuscript:
1. `traditional_topological_metrics.py` will produce the results in Chapter 7, titled "Traditional Topological Metrics".
2. `main_pagerank.py` will produce the results in Chapter 8, titled "PageRank".

### Profiling
1. `main_for_entropy_code_profiling.py`: To profile the code in the Entropy Chapter (Chapter 9) only the data from product family F2 was used. This snipped is the one profiled (otherwise, it would require HPC use).

### Graphs and plots
1. `plot_network.py`: code used to generate the DOT file to plot the manufacturing network in the Thesis.
