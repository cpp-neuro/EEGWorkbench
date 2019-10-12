from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_page, name='upload'),
    path('preprocess/', views.preprocess_page, name='preprocess'),
    path('data_analysis/', views.data_analysis_page, name='data_analysis'),
    path('feature_extract/', views.feature_extract_page, name='feature_extract'),
    path('classify/', views.classify_page, name='classify'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('load_sensors/', views.load_sensors, name='load_sensors'),
    path('get_sensor_data', views.get_sensor_data, name='get_sensor_data'),

]
