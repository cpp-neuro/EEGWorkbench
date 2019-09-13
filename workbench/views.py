from django.shortcuts import render


def index(request):
    return render(request, 'workbench/base.html', {'title': 'EEG Workbench'})
