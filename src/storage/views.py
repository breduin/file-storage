import django_rq
import logging
import os

from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from .forms import UploadFileForm
from .models import FileUpload
from .service import handle_uploaded_file
from .utils import get_upload_path


logger = logging.getLogger(__name__)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            # TODO колбэк по окончании загрузки для создания сущности FileUpload
            django_rq.enqueue(handle_uploaded_file, uploaded_file)
            # TODO валидация загружаемого файла
            file_name = uploaded_file.name.strip()
            file_cart = FileUpload.objects.create(
                name=file_name,
                description=request.POST['description'],
                content_type=uploaded_file.content_type,
                size=uploaded_file.size,
                path=get_upload_path(uploaded_file.name),
            )
            logger.info(f'Загружен файл {file_cart.path}')
            return HttpResponseRedirect(reverse('files_list'))
    else:
        form = UploadFileForm()
    return render(request, 'storage/upload.html', {'form': form})


def download_file(request, pk):
    file_container = get_object_or_404(FileUpload, pk=pk)
    file_path = file_container.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(),
                content_type=file_container.content_type
                )
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            logger.info(f'Скачан файл {file_path}')
            return response
    logger.error(f'Ошибочный запрос к файлу {file_path}')
    raise Http404


def delete_file(request, pk):

    # TODO запросить подтверждение удаления у пользователя
    # TODO переделать в метод класс FileUpload __delete__()
    file_container = get_object_or_404(FileUpload, pk=pk)
    file_path = file_container.path
    if os.path.exists(file_path):
        os.remove(file_path)
    file_container.delete()
    logger.info(f'Удалён файл {file_path}')
    return HttpResponseRedirect(reverse('files_list'))


class UploadedFilesListView(ListView):
    '''вывести список загруженных файлов'''

    template_name = 'storage/storage.html'
    model = FileUpload
    context_object_name = 'files'

    def get_queryset(self):
        qs = FileUpload.objects.all().order_by('-created_at')
        return qs
