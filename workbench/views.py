from django.shortcuts import render


def index(request):
    return render(request, 'workbench/base.html')


def upload(request):
    return render(request, 'workbench/upload.html')


def preprocess(request):
    return render(request, 'workbench/preprocess.html')


def data_analysis(request):
    return render(request, 'workbench/data_analysis.html')


def feature_extract(request):
    return render(request, 'workbench/feature_extract.html')


def classify(request):
    return render(request, 'workbench/classify.html')
