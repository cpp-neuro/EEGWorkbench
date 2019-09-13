from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('preprocess', views.preprocess, name='preprocess'),
    path('data_analysis', views.data_analysis, name='data_analysis'),
    path('feature_extract', views.feature_extract, name='feature_extract'),
    path('classify', views.classify, name='classify'),
]