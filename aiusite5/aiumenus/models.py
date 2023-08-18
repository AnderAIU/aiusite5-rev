from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Menu(models.Model):
    name = models.CharField(
        _(u'Название'),
        max_length=100
        )

    slug = models.SlugField(
        _(u'Slug')
        )

    base_url = models.CharField(
        _(u'Базовый URL'),
        max_length=100,
        blank=True,
        null=True
        )

    description = models.TextField(
        _(u'Описание'),
        blank=True,
        null=True
        )

    class Meta:
        verbose_name = _(u'Меню')
        verbose_name_plural = _(u'Меню')

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):

        super(Menu, self).save(*args, **kwargs)

        current = 10
        for item in MenuItem.objects.filter(menu=self).order_by('order'):
            item.order = current
            item.save()
            current += 10


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        verbose_name=_(u'Название'),
        on_delete=models.CASCADE,
        )

    order = models.IntegerField(
        _(u'Приоритет'),
        default=500
        )

    link_url = models.CharField(
        _(u'Ссылка'),
        max_length=100,
        help_text=_(u'URL или URI к странице, /about/ или http://yandex.ru/')
        )

    title = models.CharField(
        _(u'Имя'),
        max_length=100
        )

    login_required = models.BooleanField(
        _(u'Авторизация пользователя'),
        blank=True,
        default=False,
        help_text=_(u'Должен ли этот элемент отображаться только авторизованным пользователям?')
        )

    anonymous_only = models.BooleanField(
        _(u'Анонимный юзер'),
        blank=True,
        default=False,
        help_text=_(u'Видит ли этот элемент анонимный пользователь?')
        )

    class Meta:
        verbose_name = _(u'Элементы меню')
        verbose_name_plural = _(u'Элементы меню')

    def __unicode__(self):
        return u"%s %s. %s" % (self.menu.slug, self.order, self.title)