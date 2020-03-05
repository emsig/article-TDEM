# Fast time-domain electromagnetic modelling in the frequency domain

> Werthmüller, D., W.A. Mulder, and E.C. Slob, 2020, Fast time-domain
> electromagnetic modelling in the frequency domain: Submitted to Geophysical
> Prospecting.


## Manuscript for Geophysical Prospecting paper

Directory contains the LaTeX source of the manuscript as well as the notebooks
to reproduce all the figures.


## History

1. First submitted 05/03/2020 to Geophysical Prospecting.


## Requirements

Required are Python version 3.6 or higher and the modules `emg3d`, `empymod`,
`discretize`, and `SimPEG` (for the 3D model comparison). To reproduce the
figures with the provided notebooks the modules `IPython`, `Jupyter`, and
`matplotlib` are required additionally.


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

The final edited version is &copy; European Association of Geoscientists &
Engineers EAGE.
