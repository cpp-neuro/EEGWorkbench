from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadedFileForm

import os
from EEGWorkbench.settings import BASE_DIR

UPLOAD_DIR = os.path.join(BASE_DIR, 'workbench/uploaded_files')


def index(request):
    return redirect('upload')


def upload_page(request):
    return render(request, 'workbench/upload.html', {'uploaded_file_url': ''})


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
        fs = FileSystemStorage(location=UPLOAD_DIR)
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return redirect('upload', {'uploaded_file_url': uploaded_file_url})
    return redirect('upload')
