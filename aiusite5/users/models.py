from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from aiupages.models import *

# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения", help_text="Дата рождения, необязательно")
    bio = models.TextField(null=True, blank=True, verbose_name="О себе", help_text="О себе, например биография и прочее")
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile-avatar/")
    vkid = models.CharField(max_length=50, null=True, blank=True, verbose_name="Свой ВК", help_text="Свой VK для связи")

    def __str__(self):
        return self.username