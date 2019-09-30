import json
from datastructures import *

def parse_json(loaded_json):
    wb_data = WorkbenchData()

    # read in the data from the loaded dictionary
    # if key does not exists then skip the field

    # read workbench version
    try:
        wb_data.version = int(loaded_json[VERSION_KEY])
    except KeyError:
        print("No {} in JSON".format(VERSION_KEY))
    except TypeError:
        print("Incorrect version format: {}".format(loaded_json[VERSION_KEY]))

    # read sample rate
    try:
        wb_data.sample_rate = int(loaded_json[SAMPLE_RATE_KEY])
    except KeyError:
        print("No {} in JSON".format(SAMPLE_RATE_KEY))
    except ValueError:
        print("Incorrect sample rate format: {}".format(loaded_json[SAMPLE_RATE_KEY]))

    # read device id
    try:
        wb_data.device_id = loaded_json[DEVICE_ID_KEY]
    except KeyError:
        print("No {} in JSON".format(DEVICE_ID_KEY))

    # read record timestamp
    try:
        wb_data.record_timestamp = loaded_json[RECORD_TIMESTAMP_KEY]
    except KeyError:
        print("No {} in JSON".format(RECORD_TIMESTAMP_KEY))

    # read raw eeg data
    try:
        wb_data.raw_eeg_data = loaded_json[RAW_EEG_DATA_KEY]
    except KeyError:
        print("No {} in JSON".format(RAW_EEG_DATA_KEY))

    # read source time frequencies
    try:
        wb_data.source_tf_data = loaded_json[SOURCE_TF_DATA_KEY]
    except KeyError:
        print("No {} in JSON".format(SOURCE_TF_DATA_KEY))

    # read target time frequencies
    try:
        wb_data.target_tf_data = loaded_json[TARGET_TF_DATA_KEY]
    except KeyError:
        print("No {} in JSON".format(TARGET_TF_DATA_KEY))

    # read cross time frequencies
    try:
        wb_data.cross_tf_data = loaded_json[CROSS_TF_DATA_KEY]
    except KeyError:
        print("No {} in JSON".format(CROSS_TF_DATA_KEY))

    # read classification data
    try:
        wb_data.classification_data = loaded_json[CLASSIFICATION_DATA_KEY]
    except KeyError:
        print("No {} in JSON".format(CLASSIFICATION_DATA_KEY))

    # read classification results
    try:
        wb_data.classification_results = loaded_json[CLASSIFICATION_RESULTS_KEY]
    except KeyError:
        print("No {} in JSON".format(CLASSIFICATION_RESULTS_KEY))

    return wb_data

version = 1
sample_rate = 128
device_id = "EMOTIVPRO"
record_timestamp = "2012-04-23T18:25:43.511Z"
raw_eeg_data = {"AF3": [0, 1, 0, -1, 0], "AF4": [1, 0, -1, 0, 1]}
source_tf_data = {
    "trial 1": {
        "AF3": {
            "Alpha": [0, 1, 0, 1, 0],
            "Beta": [1, 0, 1, 0, 1]
        },
        "AF4": {
            "Alpha": [0, 1, 0, 1, 0],
            "Beta": [1, 0, 1, 0, 1]
        },
        "time": [5, 10, 15, 20, 25]
    },
    "trial 2": {
        "AF3": {
            "Alpha": [0, 2, 0, 2, 0],
            "Beta": [2, 0, 2, 0, 2]
        },
        "AF4": {
            "Alpha": [0, 2, 0, 2, 0],
            "Beta": [2, 0, 2, 0, 2]
        },
        "time": [6, 12, 18, 24, 32]
    }
}
target_tf_data = {
    "trial 1": {
        "AF3": {
            "Alpha": [0, 1, 0, 1, 0],
            "Beta": [1, 0, 1, 0, 1]
        },
        "AF4": {
            "Alpha": [0, 1, 0, 1, 0],
            "Beta": [1, 0, 1, 0, 1]
        },
        "time": [5, 10, 15, 20, 25]
    },
    "trial 2": {
        "AF3": {
            "Alpha": [0, 2, 0, 2, 0],
            "Beta": [2, 0, 2, 0, 2]
        },
        "AF4": {
            "Alpha": [0, 2, 0, 2, 0],
            "Beta": [2, 0, 2, 0, 2]
        },
        "time": [6, 12, 18, 24, 32]
    }
}
cross_tf_data = {
    "source": {
        "AF3": {
            "Alpha": [0, 1, 0, 1, 0],
            "Beta": [1, 0, 1, 0, 1]
        },
        "AF4": {
            "Alpha": [0, 1, 0, 1, 0],
            "Beta": [1, 0, 1, 0, 1]
        },
        "time": [5, 10, 15, 20, 25]
    },
    "target": {
        "AF3": {
            "Alpha": [0, 2, 0, 2, 0],
            "Beta": [2, 0, 2, 0, 2]
        },
        "AF4": {
            "Alpha": [0, 2, 0, 2, 0],
            "Beta": [2, 0, 2, 0, 2]
        },
        "time": [6, 12, 18, 24, 32]
    }
}
classification_data = {
    "train": [
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3]
    ],
    "validation": [
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3]
    ],
    "test": [
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3]
    ]
}
classification_results = [2, 4, 6, 8, 10]

data_object = {
    VERSION_KEY: version,
    SAMPLE_RATE_KEY: sample_rate,
    DEVICE_ID_KEY: device_id,
    RECORD_TIMESTAMP_KEY: record_timestamp,
    RAW_EEG_DATA_KEY: raw_eeg_data,
    SOURCE_TF_DATA_KEY: source_tf_data,
    TARGET_TF_DATA_KEY: target_tf_data,
    CROSS_TF_DATA_KEY: cross_tf_data,
    CLASSIFICATION_DATA_KEY: classification_data,
    CLASSIFICATION_RESULTS_KEY: classification_results
}

contrived = json.dumps(data_object)

with open("example.json", 'w') as json_file:
    json.dump(
        contrived, json_file, sort_keys=False, indent=4, ensure_ascii=False
    )

with open("example.json", 'r') as json_file:
    loaded = json.load(json_file) # read json as str
    loaded = json.loads(loaded)   # convert string to dict

wb_data = parse_json(loaded)

print(wb_data)



