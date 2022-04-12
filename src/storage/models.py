from django.db import models


class FileUpload(models.Model):
    '''Карточка загруженного файла'''
    name = models.CharField(
        max_length=128,
        verbose_name='Имя файла',
        )
    description = models.TextField(
        verbose_name='Описание файла',
        max_length=512,
        blank=True,
        help_text='несколько слов о том, что это за файл и для чего'
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
        )
    path = models.CharField(
        verbose_name='Путь к файлу',
        max_length=512,
        )
    content_type = models.CharField(
        verbose_name='Тип файла',
        max_length=128,
        blank=True,
        )
    size = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Fu(models.Model):
    n = models.CharField(max_length=2)
    def __str__(self):
        return self.n

