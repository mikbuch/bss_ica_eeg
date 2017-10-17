#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename: 01_plot_ica_components.py

from bieg import ICAManager
import os
# bieg -- [B]lind source separation [I]ndependent component analysis
#    for [E]e[G]

'''
Tasks:
    01.01. Run the script.
        Command (from the terminal):
            $ python 01_plot_ica_components.py
        or via ipython:
            run 01_plot_ica_components.py

    01.02. Modify (uncomment certain lines) to display only the selected
        number of components.
'''

# Input file location.
input_filepath = os.path.join(os.environ['HOME'],
                 'eeg_data/SSVEP_Bakardjian/SUBJ1/SSVEP_14Hz_Trial1_SUBJ1.MAT')

# Create an object to govern the analysis.
bss_ica = ICAManager(input_filepath)
#
# If data is saved in txt, csv or tsv format you also have to specify the
# separator, sep='' argument (by default sep='\t').

# Number of components to extract (optional). By default the n_components
# variable is set to None. Then all PCA components are used, for reference see:
# https://martinos.org/mne/stable/generated/mne.preprocessing.ICA.html#mne.preprocessing.ICA
#
#  n_components = 7

# If number of components is to be specified.
#  bss_ica = ICAManager(input_filepath, n_components)


# Finally, visualize components.
bss_ica.plot_ica_components()
