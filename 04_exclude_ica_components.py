#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename: 04_exclude_ica_components.py

from bieg import ICAManager, get_biosemi_indices
import os
# bieg -- [B]lind source separation [I]ndependent component analysis
#    for [E]e[G]

'''
Exclude selected components from the EEG signal.

I. Extract and plot components.
II. Decide which components to remove.
III. Exclude selected components.

Tasks:
    04.01. Select other components to exclude.
    04.02. Try the components exclusion with other electrodes picked.
'''

# Input file location.
input_filepath = os.path.join(os.environ['HOME'],
                     'mne_data/SSVEP-sample/SUBJ1/SSVEP_14Hz_Trial1_SUBJ1.MAT')

# Select some electrodes.
picks = get_biosemi_indices(['A10', 'A15', 'A21', 'A23', 'A28', 'B7', 'C17'])


# Create an object to govern the analysis.
# Available ICA methods: 'fastica', 'infomax' xor 'extended-infomax'.
# TODO: add 'amuse'
bss_ica = ICAManager(input_filepath, picks=picks, method='fastica')


'''
I. Extract and plot components.
'''
bss_ica.plot_ica_components()

# Additionaly, we can plot estimated sources.
bss_ica.plot_ica_sources()

'''
II. Decide which components to remove.

It has to be indices! (counting starts from 0)
'''

print('')
print(' #################################################################')
print(' # Enter the indices of the components you would like to exclude.')
print(' # Separated the indices with space, accept with the return key.')
print(' #')
print(' # By default the first and the last one components are excluded.')
print(' # i.e. \'0 6\'.\n')
components_to_exclude = input()

if components_to_exclude == '':
    components_to_exclude = [0, len(bss_ica.picks)-1]
else:
    components_to_exclude = [int(i) for i in components_to_exclude.split(' ')]

print('\n # Components to exclude: %s\n\n' % components_to_exclude)

'''
III. Exclude selected components.
'''
# Plot timecourse before removal. But don't show it yet.
bss_ica.plot_timecourse_mpl(show=False)

# Exclude the specified components.
bss_ica.exclude_ica_components(components_to_exclude)

# Plot cleaned signal (without reloading the dataset).
bss_ica.plot_timecourse_mpl(reload_dataset=False)
