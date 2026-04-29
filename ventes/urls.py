from django.urls import path
from .views import home, dashboard, download_file

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('download/', download_file, name='download'),
]