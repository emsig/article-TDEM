# Fast time-domain electromagnetic modelling in the frequency domain

> Werthmüller, D., W.A. Mulder, and E.C. Slob, 2020, Fast time-domain
> electromagnetic modelling in the frequency domain.


## Manuscript for Geophysical Prospecting paper

Directory contains the LaTeX source of the manuscript as well as the notebooks
to reproduce all the figures.


## History

1. First submitted 2020-03-05 to Geophysical Prospecting.
   GP rejected it on 2020-04-27. We are of the opinion that:

   1. The review process was not properly conducted.
   2. The deputy editor simply takes the recommendation from the associate
      editor (AE) and does not identify derogatory remarks in the reviews, nor
      opinions rather than substantiated scientific critiques, and neither
      errors by the AE and reviewer.
   3. The AE makes several false statements and incorrect remarks (we do not
      want to speculate why this occurs, but it is not a good sign) and
      therefore we do not trust that the final decision was based on
      scientific arguments.
   4. The (only) reviewer provides opinions rather than a critically
      constructive review, as he hardly ever gives substantiated scientific
      arguments for what is wrong with the manuscript. The review also
      contains erroneous comments.

   We filed an official complaint to the editor in chief on 2020-05-20.
   Our decision to file an official complaint did not come easy. But all in all
   we found this to be a serious breach in the integrity and ethical standards
   of the journal. However, the editor in chief decided to protect his deputy
   and associate editors without going into the details of our complaint.


## Requirements

Required are Python version 3.6 or higher and the modules `emg3d`,
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

The final edited version will probably be &copy; by the Journal.
