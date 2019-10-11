from workbench.processing.datastructures import *
from workbench.processing.parsing import *
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadedFileForm

import os
from EEGWorkbench.settings import BASE_DIR

UPLOAD_DIR = os.path.join(BASE_DIR, 'workbench/uploaded_files')

data_sets = []

def index(request):
    return redirect('upload')

def upload_page(request, uploaded_file_url=""):
    return render(request, 'workbench/upload.html', {'uploaded_file_url': uploaded_file_url})

def preprocess_page(request):
    return render(request, 'workbench/preprocess.html')


def data_analysis_page(request):
    return render(request, 'workbench/data_analysis.html')


def feature_extract_page(request):
    return render(request, 'workbench/feature_extract.html')


def classify_page(request):
    return render(request, 'workbench/classify.html')


def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES.keys():
        file = request.FILES['file']
        data_sets.append(parse_json(file))
        print(data_sets[0])
        return redirect('upload')
    return redirect('upload')
