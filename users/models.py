import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


def upload_to(instance, filename):
    today = datetime.today().strftime('%Y/%m/%d')
    filename = os.path.basename(filename)
    return f'profile_pics/{today}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=upload_to)

    def __str__(self):
        return f'{self.user.username} Profile'
