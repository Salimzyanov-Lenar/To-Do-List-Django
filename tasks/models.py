import os
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Task(models.Model):
    """ Модель задачи """
    TASK_PRIORITY = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]

    user = models.ForeignKey(User, verbose_name='Создатель задачи', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название задачи', max_length=255)
    description = models.TextField(verbose_name='Описание задачи')
    priority = models.IntegerField(verbose_name='Приоритет задачи', choices=TASK_PRIORITY)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    deadline = models.DateTimeField(verbose_name='Срок выполнения', null=True, blank=True)

    def __str__(self):
        return self.title


def upload_to(instance, filename):
    today = datetime.today().strftime('%Y/%m/%d')
    filename = os.path.basename(filename)
    return f'profile_pics/{today}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=upload_to)

    def __str__(self):
        return f'{self.user.username} Profile'