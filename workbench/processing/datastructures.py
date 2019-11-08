import json
import mne
import numpy as np
import matplotlib.pyplot as plt

VERSION_KEY = "version"
SAMPLE_RATE_KEY = "sample_rate"
DEVICE_ID_KEY = "device_id"
RECORD_TIMESTAMP_KEY = "record_timestamp"
RAW_EEG_DATA_KEY = "raw_eeg_data"
SOURCE_TF_DATA_KEY = "source_tf_data"
TARGET_TF_DATA_KEY = "target_tf_data"
CROSS_TF_DATA_KEY = "cross_tf_data"
CLASSIFICATION_DATA_KEY = "classification_data"
CLASSIFICATION_RESULTS_KEY = "classification_results"


class WorkbenchData:
    def __init__(
            self,
            set_name="workbenchdata",
            version=1,
            sample_rate=None,
            device_id=None,
            record_timestamp=None,
            raw_eeg_data=None,
            source_tf_data=None,
            target_tf_data=None,
            cross_tf_data=None,
            classification_data=None,
            classification_results=None
    ):
        self.set_name = set_name                             # name of imported or exported file
        self.version = version
        self.sample_rate = sample_rate
        self.device_id = device_id
        self.record_timestamp = record_timestamp             # JavaScript Format: 2012-04-23T18:25:43.511Z
        self.raw_eeg_data = raw_eeg_data                     # {sensor # : [a1, a2, ...], ...}
        self.source_tf_data = source_tf_data                 # {trial #: {{sensor : {freq 1 : []}, ...,}, ..., time : [t1, t2, t3 ...]} ...}
        self.target_tf_data = target_tf_data                 # {trial #: { sensor : band frequencies ..., time : [t1, t2, t3 ...]} ...}
        self.cross_tf_data = cross_tf_data                   # {source : { sensor : band frequencies ..., time : [t1, t2, t3 ...]} ..., target : ...}
        self.classification_data = classification_data       # {train : [[row 1][row 2][row 3]...], validation : [[row 1]...], test : [row 1]...}
        self.classification_results = classification_results # array of classification results from chosen algorithm

    def __str__(self):
        s = ""
        s += "{}: {}\n".format(VERSION_KEY, self.version)
        s += "{}: {}\n".format(SAMPLE_RATE_KEY, self.sample_rate)
        s += "{}: {}\n".format(DEVICE_ID_KEY, self.device_id)
        s += "{}: {}\n".format(RECORD_TIMESTAMP_KEY, self.record_timestamp)
        s += "{}: {}\n".format(RAW_EEG_DATA_KEY, self.raw_eeg_data)
        s += "{}: {}\n".format(SOURCE_TF_DATA_KEY, self.source_tf_data)
        s += "{}: {}\n".format(TARGET_TF_DATA_KEY, self.target_tf_data)
        s += "{}: {}\n".format(CROSS_TF_DATA_KEY, self.cross_tf_data)
        s += "{}: {}\n".format(CLASSIFICATION_DATA_KEY, self.classification_data)
        s += "{}: {}\n".format(CLASSIFICATION_RESULTS_KEY, self.classification_results)
        return s

    def to_json(self):
        data = dict()
        data[VERSION_KEY] = self.version
        data[SAMPLE_RATE_KEY] = self.sample_rate
        data[DEVICE_ID_KEY] = self.device_id
        data[RECORD_TIMESTAMP_KEY] = self.record_timestamp
        data[RAW_EEG_DATA_KEY] = self.raw_eeg_data
        data[SOURCE_TF_DATA_KEY] = self.source_tf_data
        data[TARGET_TF_DATA_KEY] = self.target_tf_data
        data[CROSS_TF_DATA_KEY] = self.cross_tf_data
        data[CLASSIFICATION_DATA_KEY] = self.classification_data
        data[CLASSIFICATION_RESULTS_KEY] = self.classification_results

        return json.dumps(data)

    def get_raw_eeg_lengths_as_dictionary(self):
        lengths = dict()

        for key in self.raw_eeg_data.keys():
            lengths[key] = len(self.raw_eeg_data[key])

        return lengths

    def get_source_tf_lengths_as_dictionary(self):
        lengths = dict()

        for key in self.source_tf_data.keys():
            lengths[key] = len(self.source_tf_data[key])

        return lengths

    def get_target_tf_lengths_as_dictionary(self):
        lengths = dict()

        for key in self.target_tf_data.keys():
            lengths[key] = len(self.target_tf_data[key])

        return lengths

    def get_raw_sensor_data(self, sensor):
        return self.raw_eeg_data[sensor]

    def get_mne_rawarray_from_raw_eeg(self, ch_type="mag"):

        # create the necessary metadata for the mne array
        # more info can be found at https://mne.tools/dev/auto_examples/io/plot_objects_from_arrays.html
        ch_names = list(self.raw_eeg_data.keys())
        ch_types = [ch_type] * len(ch_names)
        info = mne.create_info(ch_names=ch_names, sfreq=self.sample_rate, ch_types=ch_types)

        data = np.array([self.raw_eeg_data[ch] for ch in ch_names])

        return mne.io.RawArray(data, info)

    def get_spectral_density_from_raw_eeg_as_dicitonary(self):
        spectral_analysis_dicitonary = dict()

        rawarray = self.get_mne_rawarray_from_raw_eeg()
        psds, freqs = mne.time_frequency.psd.psd_welch(rawarray)

        ch_names = rawarray.ch_names

        spectral_analysis_dicitonary["freqs"] = freqs

        for i in range(len(ch_names)):
            spectral_analysis_dicitonary[ch_names[i]] = psds[i]

        return spectral_analysis_dicitonary



