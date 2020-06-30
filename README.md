# Fast time-domain electromagnetic modelling in the frequency domain

> Werthmüller, D., W.A. Mulder, and E.C. Slob, 2020, Fast time-domain
> electromagnetic modelling in the frequency domain: Submitted to Geophysical
> Journal International.


## Manuscript for Geophysical Journal International paper

Directory contains the LaTeX source of the manuscript as well as the notebooks
to reproduce all the figures.


## History

1. Submitted 2020-06-30 to Geophysical Journal International.


## Requirements and Environment

Required are Python version 3.7 or higher and the modules `emg3d`,
`discretize`, and `SimPEG` (for the 3D model comparison). To reproduce the
figures with the provided notebooks the modules `Jupyter`, and `matplotlib` are
required additionally.

We provide an `environment.yml` to ensure everything can be reproduced.

To create the environment simply run
```bash
conda env create -f environment.yml
```
This will create a new conda environment called `article-tdem`.

To activate and deactivate the environment run
```bash
conda activate article-tdem
conda deactivate
```

To use this environment in the Jupyter notebook, you have to register it first:
```bash
python -m ipykernel install --user --name article-tdem
```
Then, in Jupyter, you can select it by going to `Kernel`->`Change kernel` and
select `article-tdem`.

To completely remove the environment run
```bash
conda remove --name article-tdem --all
```

`emg3d` requires at least Python 3.7.


## Reproducing

Start `Jupyter` and navigate to the notebooks-folder. The notebooks to
reproduce the figures in the article are:

- **Frequency-Selection.ipynb**: Figures 1, 2, and 3.
- **Fullspace.ipynb**: Figures 4 and 5.
- **1D-Model.ipynb**: Figures 6 and 7.
- **1D-Model-wrong-x-y.ipynb**: Figure 8.
- **3D-Model.ipynb**: Figures 9 and 10.
- **3D-Model-double.ipynb**: As `3D-Model.ipynb`, but doubled cells in each
  direction.

## Note

The final edited version will be &copy; Geophysical Journal International.
