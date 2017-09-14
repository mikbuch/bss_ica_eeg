#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename: bieg.py

import scipy.io as sio
import numpy as np
import pandas as pd
from sklearn import preprocessing
import os
import matplotlib.pyplot as plt

import mne
from mne.preprocessing import ICA


def get_biosemi_indices(names_to_pick,
                        filename='biosemi_electrodes_names.txt'):
    electrodes_names = pd.read_csv(filename, index_col=None)
    return electrodes_names[names_to_pick].values[0].tolist()


class ICAManager(object):

    def __init__(self, input_path, n_components=None, picks=None,
                 method='fastica', var_name='EEGdata', sep=None,
                 kind='biosemi128', sfreq=256):

        self.input_path = input_path
        self.n_components = n_components
        self.picks = picks
        self.method = method
        self.var_name = var_name
        self.sep = sep
        self.kind = kind
        self.sfreq = sfreq


    def load_matlab_data(self):
        # Convert to numpy.
        self.data = sio.loadmat(self.input_path)
        # Extract the variable of interest.
        self.data = self.data[self.var_name]


    def load_csv_data(self):
        self.data = np.load_txt(self.input_path, delimiter=self.sep)


    def load_coords(self, scale_0_1=True):
        coords = np.loadtxt(self.input_path, sep=self.sep)
        if scale_0_1:
            coords = preprocessing.MinMaxScaler().fit_transform(coords)

        return coords


    def create_MNE_Raw(self, filter=(1, 40)):
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

        montage = mne.channels.read_montage(self.kind)

        # Create the info structure needed by MNE
        info = mne.create_info(montage.ch_names, self.sfreq, ch_types, montage)

        # Read montage.
        # 3D montage ==> 2D montage
        # https://gist.github.com/wmvanvliet/6d7c78ea329d4e9e1217
        #  info = mne.create_info(ch_names, sfreq, ch_types, montage)
        self.layout = mne.channels.make_eeg_layout(info)
        self.layout.pos = self.layout.pos[:-3]
        montage.ch_names = montage.ch_names[:-3]

        # Update pos to 2D scheme.
        montage.pos = self.layout.pos

        info = mne.create_info(montage.ch_names, self.sfreq, ch_types, montage)

        # Finally, get the data.
        self.load_data()
        # And create the Raw object.
        self.raw = mne.io.RawArray(self.data, info)

        if filter:
            self.raw.filter(filter[0], filter[1], n_jobs=2)


    def load_data(self):
        ext = os.path.splitext(self.input_path)[-1].lower()
        if 'mat' in ext:
            self.load_matlab_data()
        elif 'txt' or 'csv' or 'tsv' in ext:
            self.load_csv_data()
        else:
            print('File extention not recognized.')
            print('Please, use one of the following: mat, txt, csv or tsv.')


    def plot_timecourse(self, filter=(1,40), reload_dataset=True):

        if not self.raw or reload_dataset:
            self.create_MNE_Raw(filter=filter)
        # On ArchLinux, for unkown reason this works only within ipython
        # environement (probably display manger issue).
        self.raw.plot(order=self.picks, scalings={'eeg': 100.0})


    def plot_timecourse_mpl(self, filter=(1,40), reload_dataset=True,
                            show=True):

        if not self.raw or reload_dataset:
            self.create_MNE_Raw(filter=filter)

        # Get the (filtered) data.
        data = self.raw.get_data()

        for (i, no) in enumerate(self.picks):
            plt.subplot(len(self.picks), 1, i+1)
            plt.plot(data[no])
        
        if show:
            plt.show()


    def extract_components(self):

        self.create_MNE_Raw(filter=(1, 40))

        #######################################################################
        # Fit ICA
        # -------
        #
        # ICA parameters:

        # we need sufficient statistics, not all time points -> saves time
        decim = 3  

        # we will also set state of the random number generator - ICA is a
        # non-deterministic algorithm, but we want to have the same
        # decomposition and the same order of components each time 
        random_state = 23

        #######################################################################
        # Define the ICA object instance
        self.ica = ICA(n_components=self.n_components, method=self.method,
                       random_state=random_state)
        print(self.ica)

        #######################################################################
        # we avoid fitting ICA on crazy environmental artifacts that would
        # dominate the variance and decomposition
        reject = dict(mag=5e-12, grad=4000e-13)
        self.ica.fit(self.raw, picks=self.picks, decim=decim, reject=reject)
        print(self.ica)


    def plot_ica_components(self, plot_picks=None):

        self.extract_components()

        self.ica.plot_components(layout=self.layout, picks=plot_picks)


    def plot_ica_sources(self):

        self.extract_components()

        self.ica.plot_sources(self.raw)
    

    def exclude_ica_components(self, components_to_exclude):

        self.extract_components()

        self.ica.apply(self.raw, exclude=components_to_exclude)
