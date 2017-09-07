# bss_ica_eeg
Blind Source Separation:
Independent Component Analysis for EEG data with python-MNE package and SSVEP


This is an example package performing ICA noise removal for SSVEP data.

I. Required data format.
    Due to MNE-python policy, the data format has to be strictly abided.

    For our purpose it is Biosemi128 data format (csv).


II. Usage.

    ICA artifacts removal consists of two consecutive phases:
        1. Extract and plot indepentent components.
        *** Decide which of the components to remove ***
        2. Remove components.

    In this package these operations are devided (for tutorial purposes)
            into separate scripts:
        01_plot_ica_components.py
        02_plot_ica_selected_channels.py

        core file is bieg.py (Blind source separation Independent component
            analysis for EeG)

    User has to specify the following information/parameters:
        * Input file location.
        * Number of components to devide the data into.
        * Electrodes (channels) to pick.
        * INDICES of the components to remove (starting at 0.)
        * (optionally) output path (by default it takes the input file's
            path and simply adds "_cleaned" before a file extention.
