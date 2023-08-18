from django.db import models

# Create your models here.
class AiuExtParam(models.Model):
    name_profile = models.CharField(default="extended01", max_length=64, verbose_name="Профиль расширенных управлений")
    disMenuClick = models.BooleanField(default=False, verbose_name="Отключить переходы по меню")
    disMenuMove = models.BooleanField(default=False, verbose_name="Отключить наведение=клик")
    enPreloader = models.BooleanField(default=False, verbose_name="Включить прелоадер")
    dMode = models.BooleanField(default=False, verbose_name="Активировать DEBUG mode")

    class Meta:
        verbose_name = 'Расширенное администрирование (в разработке)'
        verbose_name_plural = 'Расширенное администрирование (в разработке)'

    def __str__(self):
        return self.name_profile