#!/bin/bash

#workdir=results/2017-11-16T10-17-05-556970_fb7b8229-9817-4190-90c9-948eeefeb670
workdir=results/2017-12-11T12-43-10-684086_495cdc52-e149-4244-a3b5-0150454cb9d2

#Make the pull plots, produces mlfitshapes file
#python ../../Plotting/python/Datacards/MakeLimits.py --jobtype pulls --config $workdir/analysis.pickle --group group_sldl,group_sl,group_dl

#Based on the pull plot results, do the best fit plot based on the mlfitshapes
python ../../Plotting/python/joosep/fit_results.py $workdir

#Prefit and postfit plots
python ../../Plotting/python/joosep/prefit_postfit.py $workdir

#Nuisance correlation plot
python corrs.py $workdir
