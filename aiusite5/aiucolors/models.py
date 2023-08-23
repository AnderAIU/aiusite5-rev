from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from colorfield.fields import ColorField

#Colors schema
class color_profile(models.Model):
    name_profile = models.CharField(default="profile01", max_length=64, verbose_name="Название профиля")
    name_site = models.CharField(default="Сайт", max_length=255, verbose_name="Название сайта")
    #title_color = models.CharField(default="rgba(70,135,79,1)", max_length=64)
    left_padding = models.IntegerField(default=0, validators=[ MaxValueValidator(100), MinValueValidator(0)], verbose_name="Левый отступ, % от экрана", help_text="Регулировка левого отступа, пользовательская модификация")
    title_color = ColorField(format="hexa", verbose_name="Цвет заголовков")
    hover_color = ColorField(format="hexa", verbose_name="Фон при наведении на подпункты меню")
    hover_files = ColorField(format="hexa", verbose_name="Фон при наведении на файлы")
    text_color = ColorField(format="hexa", verbose_name="Цвет основного текста")
    menu_color = ColorField(format="hexa", verbose_name="Цвет фона меню и обводок")
    menu_text_color = ColorField(format="hexa", verbose_name="Цвет текста меню")
    background_color = ColorField(format="hexa", verbose_name="Фон сайта")
    pos_code = models.TextField(default="", verbose_name="Код для интеграции ПОС Госуслуги")
    onmenu = models.BooleanField(default=False, verbose_name="Меню на странице", help_text="Отключить меню/включить")
    yandex_meta = models.CharField(default="", max_length=255, verbose_name="ID верификации в Яндексе")

    class Meta:
        verbose_name = 'Глобальные настройки сайта'
        verbose_name_plural = 'Глобальные настройки сайта'

    def __str__(self):
        return self.name_site