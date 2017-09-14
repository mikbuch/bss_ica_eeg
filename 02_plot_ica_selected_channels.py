#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename: 02_plot_ica_selected_channels.py

from bieg import ICAManager, get_biosemi_indices
import os
# bieg -- [B]lind source separation [I]ndependent component analysis
#    for [E]e[G]

'''
Now lets assume that you are willing to use only the selected channels
(electrodes) then you have to pass ``picks`` argument. Again, if you leave
n_components unset the algorithm will generate as many components as many
channels you chose.

Tasks:
    02.01. Start the script in an unchanged form and observe the result.
    02.02. Select some other electrodes, set n_components. See what happens
        if you select n_components>=n_picks.
'''

# Input file location.
input_filepath = os.path.join(os.environ['HOME'],
                     'mne_data/SSVEP-sample/SUBJ1/SSVEP_14Hz_Trial1_SUBJ1.MAT')

# Select some electrodes.
picks = get_biosemi_indices(['A10', 'A15', 'A21', 'A23', 'A28', 'B7', 'C17'])


# Create an object to govern the analysis.
bss_ica = ICAManager(input_filepath, picks=picks)
#
# If data is saved in txt, csv or tsv format you also have to specify the
# separator, sep='' argument (by default sep='\t').

# Number of components to extract (optional). By default the n_components
# variable is set to None. Then all PCA components are used, for reference see:
# https://martinos.org/mne/stable/generated/mne.preprocessing.ICA.html#mne.preprocessing.ICA
# If ``None`` then take as many as possible (the number of channels picked).
#
#  n_components = 4

# If number of components is to be specified.
#  bss_ica = ICAManager(input_filepath, n_components, picks=picks)

# Finally, visualize components.
bss_ica.plot_ica_components()
