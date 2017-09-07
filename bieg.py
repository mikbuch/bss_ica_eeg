#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename: bieg.py

import scipy.io as sio
import numpy as np
import pandas as pd
from sklearn import preprocessing
import os

import mne
from mne.preprocessing import ICA


def load_matlab_data(filepath, var_name='EEGdata', sep=None):
    # Convert to numpy.
    data = sio.loadmat(filepath)
    # Extract the variable of interest.
    data = data[var_name]
    return data


def load_csv_data(filepath, sep='\t'):
    data = np.load_txt(filepath, delimiter=sep)
    return data


def load_coords(filepath, sep=',', scale_0_1=True):
    coords = np.loadtxt(filepath, sep=sep)
    if scale_0_1:
        coords = preprocessing.MinMaxScaler().fit_transform(coords)

    return coords


def create_MNE_Raw(data, kind, sfreq, dbg=False):
    '''
    Based on: http://stackoverflow.com/a/38634620

    sfreq : float or int
        Sampling rate of the machine [Hz].

    Channel types. From documentation:

    ch_types : list of str | str
        Channel types. If None, data are assumed to be misc.
        Currently supported fields are 'ecg', 'bio', 'stim', 'eog', 'misc',
        'seeg', 'ecog', 'mag', 'eeg', 'ref_meg', 'grad', 'hbr' or 'hbo'.
        If str, then all channels are assumed to be of the same type.
    '''
    ch_types = 'eeg'

    montage = mne.channels.read_montage(kind)

    # Create the info structure needed by MNE
    info = mne.create_info(montage.ch_names, sfreq, ch_types, montage)

    # Read montage.
    # 3D montage ==> 2D montage
    # https://gist.github.com/wmvanvliet/6d7c78ea329d4e9e1217
    #  info = mne.create_info(ch_names, sfreq, ch_types, montage)
    layout = mne.channels.make_eeg_layout(info)
    layout.pos = layout.pos[:-3]
    montage.ch_names = montage.ch_names[:-3]

    # Update pos to 2D scheme.
    montage.pos = layout.pos

    #  info = mne.create_info(montage.ch_names, sfreq, ch_types, montage, layout)
    info = mne.create_info(montage.ch_names, sfreq, ch_types, montage)

    # Finally, create the Raw object
    raw = mne.io.RawArray(data, info)

    if dbg:
        # Plot it.
        raw.plot()

    return raw, layout


def load_data(filepath, sep='\t'):
    ext = os.path.splitext(filepath)[-1].lower()
    if 'mat' in ext:
        data = load_matlab_data(filepath)
    elif 'txt' or 'csv' or 'tsv' in ext:
        data = load_csv_data(filepath, sep)
    else:
        print('File extention not recognized.')
        print('Please, use one of the following: mat, txt, csv or tsv.')
    return data


def get_biosemi_indices(names_to_pick):
    electrodes_names = pd.read_csv('biosemi_electrodes_names.txt',
                                   index_col=None)
    return electrodes_names[names_to_pick].values[0].tolist()


def extract_components(input_filepath, sep='\t', n_components=None,
                       picks=None):

    data = load_data(input_filepath, sep)

    kind = 'biosemi128'

    raw, lay = create_MNE_Raw(data, kind, sfreq=256)

    raw.filter(1, 40, n_jobs=2)


    ###########################################################################
    # Fit ICA
    # -------
    #
    # ICA parameters:

    method = 'fastica'
    # we need sufficient statistics, not all time points -> saves time
    decim = 3  

    # we will also set state of the random number generator - ICA is a
    # non-deterministic algorithm, but we want to have the same decomposition
    # and the same order of components each time this tutorial is run
    random_state = 23

    ###########################################################################
    # Define the ICA object instance
    ica = ICA(n_components=n_components, method=method,
              random_state=random_state)
    print(ica)

    ###########################################################################
    # we avoid fitting ICA on crazy environmental artifacts that would
    # dominate the variance and decomposition
    reject = dict(mag=5e-12, grad=4000e-13)
    ica.fit(raw, picks=picks, decim=decim, reject=reject)
    print(ica)

    return ica, lay


def plot_ica_components(input_filepath, sep='\t', n_components=None,
                        picks=None, plot_picks=None):

    ica_components, lay = extract_components(input_filepath=input_filepath,
                                             sep=sep, picks=picks,
                                             n_components=n_components)

    ica_components.plot_components(layout=lay, picks=plot_picks)
