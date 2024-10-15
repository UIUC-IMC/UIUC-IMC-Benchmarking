# Benchmarking of In-memory Computing (IMC) Architectures

This is a repository of IMC metrics extracted from published IC prototypes in ISSCC, VLSI, CICC, (and ESSCIRC), since 2018, in order to infer trends in this area. The repository includes data for digital accelerators as well but it is not as comprehensive as those for IMCs. The
repository comprises a database (Benchmarking_Data.csv) and Python code (plot_all.py) to generate annually updated versions of the plots found in our CICC'22 paper [Benchmarking In-memory Computing (IMC) Architectures](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9772817) which describes the benchmarking methodology. Please check for annual updates to the database which will occur sometime in August. Users are welcome to generate their own plots using our database. If you do so, please cite our paper and this GitHub repository. A BibTex code is provided below for those using LaTex.

Please inform us of any errors in the database using [this form](https://forms.gle/xLT8NehqR1ALuW2p7). 

Maintained by: Soonha Hwang, Ph.D. student, University of Illinois at Urbana-Champaign (2023-present).

## Current State

## Update
- July 2023: the database now incorporates the 2023 data. Additionally, benchmarking plots from 2021, 2022, and 2023, are made available. As always, users can generate their own customized plots using the Python codes provided.
- Jan 2024: Errata found in Index No. 111, 112, 147, 151. The error in the digital accelerator's errata has been corrected
- October 2024: New data has been updated. Only 3 new data has been inputed given our updating methodology.
 
## About
In-memory computing (IMC) architectures have emerged as a compelling platform to implement energy efficient machine learning (ML) systems. However, today, the energy efficiency gains provided by IMC designs seem to be leveling off and it is not clear what the limiting factors are. The conceptual complexity of IMCs combined with the absence of a rigorous benchmarking methodology makes it difficult to gauge progress and identify bottlenecks in this exciting field. Our benchmarking methodology for IMCs comprises of: 1) a compositional view of IMCs that enables one to parse an IMC design into its canonical components; 2) a set of benchmarking metrics to quantify the performance, efficiency, and accuracy of IMCs; and 3) a strategy for analyzing the reported IMC data and metrics.

## Usage
Set the `OUTPUT_DIR` parameter on line 20 of `plot_all.py` to the output folder, and run 
``` 
python3 plot_all.py
```
to reproduce the most recent version of the figures in our CICC'22 paper.

The `SAVE_PDF` and `SAVE_SVG` toggles determine which formats the plots are saved as. The `MARK_IMC_PROCESSOR`  controls whether each plot has IMC processors marked with red boxes.   

## Environment
The following Python 3 packages are required to run the program
* numpy
* matplotlib

## Citation
Please cite our paper and this GitHub repository if you use our benchmarking data.

Paper BibTex:
```
@inproceedings{shanbhag2022comprehending,
  title={Comprehending In-memory Computing Trends via Proper Benchmarking},
  author={Shanbhag, Naresh R and Roy, Saion K},
  booktitle={2022 IEEE Custom Integrated Circuits Conference (CICC)},
  pages={01--07},
  year={2022},
  organization={IEEE}
}
```
Repository BibTex:
```
@software{Shanbhag_IMC-Benchmarking_GitHub_respository_2022,
author = {Shanbhag, Naresh R and Roy, Saion K},
month = {10},
title = {{IMC-Benchmarking GitHub respository}},
year = {2022}
}
```
