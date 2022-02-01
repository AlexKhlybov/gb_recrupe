from django.db import models

from apps.tools import upload_to_and_rename


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    image = models.FileField(max_length=64, verbose_name='Картинка', upload_to=upload_to_and_rename('news', 'image'))
    short_text = models.CharField(max_length=255, verbose_name='Краткое описание')
    text = models.TextField(max_length=10000, verbose_name='Текст новости')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def split_text_to_lines(self):
        return self.text.split('\n')

    def __str__(self):
        return self.title
