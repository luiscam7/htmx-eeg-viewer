"""Use NeuroDSP to generate synthetic oscillation to test DSP algorithms."""

import pandas as pd
from neurodsp.sim import sim_oscillation
from neurodsp.utils import create_times


class SyntheticEDFWriter:
    def __init__(self, n_seconds, fs):
        """
        Initialize the EEGWriter with the duration of the signals and sampling frequency.

        Parameters
        ----------
        n_seconds : float
            Length of the signal in seconds.
        fs : float
            Sampling frequency of the signal.
        """
        self.n_seconds = n_seconds
        self.fs = fs
        self.times = create_times(n_seconds, fs)
        self.df = pd.DataFrame(index=self.times)

    def generate_eeg_signal(self, central_freq, phase_degrees=0, amp_factor=10):
        """
        Generate an EEG signal centered around one frequency using neurodsp with a specific phase.

        Parameters
        ----------
        central_freq : float
            The central frequency of the EEG signal in Hz.
        phase_degrees : float, optional, default: 0
            The initial phase of the signal in degrees.
        amp_factor : float, optional, default: 1
            Amplitude scaling factor.

        Returns
        -------
        signal : 1d array
            Generated EEG signal.
        """
        phase_fraction = phase_degrees / 360.0
        signal = amp_factor * sim_oscillation(
            self.n_seconds, self.fs, central_freq, phase=phase_fraction
        )
        return signal

    def generate_synthetic_eeg(self):
        """
        Populate the dataframe with EEG signals for each 10-20 system channel.
        """
        # Frontal Region
        self.df["Fp1"] = self.generate_eeg_signal(2)
        self.df["Fp2"] = self.generate_eeg_signal(6)
        self.df["F3"] = self.generate_eeg_signal(10)
        self.df["F4"] = self.generate_eeg_signal(20)

        # Central Region
        self.df["C3"] = self.generate_eeg_signal(3)
        self.df["Cz"] = self.generate_eeg_signal(7)
        self.df["C4"] = self.generate_eeg_signal(10)
        self.df["T3"] = self.generate_eeg_signal(15)

        # Occipital Region
        self.df["O1"] = self.generate_eeg_signal(4)
        self.df["O2"] = self.generate_eeg_signal(6)
        self.df["P3"] = self.generate_eeg_signal(10)
        self.df["P4"] = self.generate_eeg_signal(18)

        # Opposite Phase for Alpha
        self.df["F7"] = self.generate_eeg_signal(
            10, phase_degrees=180
        )  # Opposite phase Alpha

        # Combined Signals
        self.df["F8"] = self.generate_eeg_signal(2) + self.generate_eeg_signal(
            6
        )  # Delta + Theta
        self.df["T4"] = (
            self.generate_eeg_signal(2)
            + self.generate_eeg_signal(6)
            + self.generate_eeg_signal(10)
        )  # Delta + Theta + Alpha
        self.df["T5"] = (
            self.generate_eeg_signal(2)
            + self.generate_eeg_signal(6)
            + self.generate_eeg_signal(10)
            + self.generate_eeg_signal(20)
        )  # Delta + Theta + Alpha + Beta

        # Varying Alpha Frequencies
        self.df["T6"] = self.generate_eeg_signal(9)
        self.df["Fz"] = self.generate_eeg_signal(10)
        self.df["Pz"] = self.generate_eeg_signal(11)

    def serve_json(self):
        return self.df.to_json()
