from django.urls import path

from .views import upload_file
from .views import download_file
from .views import delete_file
from .views import UploadedFilesListView


urlpatterns = [
    path('', UploadedFilesListView.as_view(), name='files_list'),
    path('upload/', upload_file, name='upload'),
    path('download/<int:pk>', download_file, name='download'),
    path('delete/<int:pk>', delete_file, name='delete')
]
