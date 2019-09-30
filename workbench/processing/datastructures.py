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
            version=None,
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

