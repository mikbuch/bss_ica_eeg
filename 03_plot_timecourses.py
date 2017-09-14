#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename: 03_plot_timecourses.py

from bieg import ICAManager, get_biosemi_indices
import os
# bieg -- [B]lind source separation [I]ndependent component analysis
#    for [E]e[G]

'''
Plot values for channels in time domain.

Now lets assume that you are willing to use only the selected channels
(electrodes) then you have to pass ``picks`` argument. Again, if you leave
n_components unset the algorithm will generate as many components as many
channels you chose.

Tasks:
    03.01. Pick other electrodes and plot their timecourse in two ways.
    03.02. Uncomment the last line to see the unfiltered signal.
'''

# Input file location.
input_filepath = os.path.join(os.environ['HOME'],
                     'mne_data/SSVEP-sample/SUBJ1/SSVEP_14Hz_Trial1_SUBJ1.MAT')

# Select some electrodes.
picks = get_biosemi_indices(['A10', 'A15', 'A21', 'A23', 'A28', 'B7', 'C17'])


# Create an object to govern the analysis.
bss_ica = ICAManager(input_filepath, picks=picks)


'''
In the bieg class there are two ways to plot the signal timecourse.

First one is an internal MNE's plot() method that can be called upon a raw
dataset object.

The second one was written in pure, simple matplotlib and plots each electrode
in separate figure.
'''

# First method.
bss_ica.plot_timecourse()

# Press any key. Without this pause, the canvas is overwritten automatically.
print('\nEnter any key and accept it with the return key ...')
input()

# Second method. 
bss_ica.plot_timecourse_mpl()

# To plot the timecourse without bandpass filter.
#  bss_ica.plot_timecourse_mpl(filter=None)
