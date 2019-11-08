from workbench.processing.datastructures import *
import workbench.processing.parsing as parsing
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.response import JsonResponse, HttpResponse

import os
from EEGWorkbench.settings import BASE_DIR

UPLOAD_DIR = os.path.join(BASE_DIR, 'workbench/uploaded_files')

data_sets = []
source_index = -1
target_index = -1

def index(request):
    return redirect('upload')

def upload_page(request, uploaded_file_url=""):
    return render(
        request,
        'workbench/upload.html',
        {
            "uploaded_file_url": uploaded_file_url,
            "data_sets": data_sets
        }
    )

def preprocess_page(request):
    return render(request, 'workbench/preprocess.html')


def data_analysis_page(request):
    return render(request, 'workbench/data_analysis.html')


def feature_extract_page(request):
    return render(request, 'workbench/feature_extract.html')


def classify_page(request):
    return render(request, 'workbench/classify.html')


def upload_file(request):
    global data_sets

    if request.method == 'POST' and 'file' in request.FILES.keys():
        file = request.FILES['file']
        new_data_set = parsing.get_workbenchdata_object_from_json(file.name, file)
        data_sets.append(new_data_set)
        return redirect('upload')
    return redirect('upload')


# todo: switch to source and target data instead of raw eeg
def load_sensors(request):
    if request.method == "GET" and request.is_ajax():
        index = int(request.GET["file"])

        return JsonResponse(data_sets[index].get_raw_eeg_lengths_as_dictionary())


def compute_statistics(request):
    if request.method == "GET" and request.is_ajax():

        query_params = request.GET

        # object to be returned
        raw_eeg = {"src": dict(), "tgt": dict()}

        # extract the sensors from the get requeset
        src_sensors = []
        tgt_sensors = []

        # extract the requested sensor names
        try:
            src_sensors = query_params.getlist("src_eegs[]")
        except Exception as e:
            print(e)

        try:
            tgt_sensors = query_params.getlist("tgt_eegs[]")
        except Exception as e:
            print(e)



        print(request.GET)

        # add data sets to the return container
        # TODO: save the loaded index and retrieve the proper sensor amplitudes
        for sensor in src_sensors:
            # print(sensor)
            raw_eeg["src"][sensor] = data_sets[0].get_raw_sensor_data(sensor)
        for sensor in tgt_sensors:
            # print(sensor)
            raw_eeg["tgt"][sensor] = data_sets[0].get_raw_sensor_data(sensor)

        # return the dictionary in JSON format
        return JsonResponse(raw_eeg)
