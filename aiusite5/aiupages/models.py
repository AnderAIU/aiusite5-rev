from django.db import models
#from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime
import mimetypes
import os
import uuid
import random
from functools import partial
from django.template.defaultfilters import slugify as django_slugify
from .validators import validate_file_extension

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

def user_directory_path(instance, filename):
    # Get Current Date
    todays_date = datetime.date.today()

    path = "files/document/{}/{}/{}/".format(todays_date.year, todays_date.month, todays_date.day)
    extension = "." + filename.split('.')[-1]
    stringId = str(uuid.uuid4())
    randInt = str(random.randint(10, 99))

    # Filename reformat
    filename_reformat = stringId + randInt + extension

    return os.path.join(path, filename_reformat)

# Create your models here.

class Pages(models.Model):
    slug = models.CharField(default="", max_length=255, verbose_name="Slug", help_text="Фигурирует в URL, как id для ссылки на страницу")
    title = models.CharField(default="", max_length=255, verbose_name="Краткий заголовок", help_text="Заголовок, отображаемый в меню, блоках и прочее")
    description = models.CharField(default="", max_length=255, verbose_name="Описание", help_text="Описание подробное страницы, обычно используется в поисковых системах, как параметр description")
    public_name = models.CharField(default="", max_length=255, verbose_name="Отображаемый заголовок", help_text="Заголовок в шапке страницы")
    date_pub = models.DateField(default=datetime.date.today, editable=False, verbose_name="Отображаемый заголовок", help_text="Заголовок в шапке страницы")
    fullmenu = models.BooleanField(default=False, verbose_name="Раскрытое меню на странице", help_text="Отображать на десктопах постоянно открытое меню сайта")

    class Meta:
        ordering = ['-date_pub']
        verbose_name = 'Страницы сайта'
        verbose_name_plural = 'Страницы сайта'

    def __str__(self):
        return self.title
    
    def get_containers(self):
        return Containers.objects.filter(page_member=self)
        
    def slugpage(self):
        return f'{self.slug}'
        
    def get_absolute_url(self):
        if (slugpage(self) == 'home'):
            return f'/'
        else:
            return f'/{self.slug}'
    
class Containers(models.Model):
    page_member = models.ForeignKey(Pages, on_delete=models.CASCADE, related_name="container_num")
    slug = models.CharField(default="container-", max_length=255, verbose_name="Slug контейнера", help_text="Код отображения")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Отображаемый заголовок", help_text="Роль подзаголовка, можно не указывать, если он не нужен к отображению")
    template_name = models.CharField(default="container.html", max_length=255, verbose_name="Файл шаблона", help_text="Название файла для шаблона контейнера, системная настройка, лучше оставлять по умолчанию")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")

    class Meta:
        ordering = ['order']
        verbose_name = 'Контейнер содержимого'
        verbose_name_plural = 'Контейнер содержимого'

    def __str__(self):
        return self.title
    
    def get_block(self):
        return Blocks.objects.filter(contid=self)

class Blocks(models.Model):
    contid = models.ForeignKey(Containers, on_delete=models.CASCADE, related_name="block_num")
    slug = models.CharField(default="contactblock-", max_length=255, verbose_name="Код отображения")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Код отображения", help_text="Роль подзаголовка, можно не указывать, если он не нужен к отображению")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")

    class Meta:
        ordering = ['order']
        verbose_name = 'Блок данных (строка разметки)'
        verbose_name_plural = 'Блок данных (строка разметки)'

    def __str__(self):
        return self.title
    
    def get_textblock(self):
        return TextBlock.objects.filter(blockid=self)
    
    def get_contact(self):
        return ContactBlock.objects.filter(blockid=self)
    
    def get_modern(self):
        return ModernBlock.objects.filter(blockid=self)
    
    def get_diagr(self):
        return DiagrBlock.objects.filter(blockid=self)
    
    def get_extfiles(self):
        return ExtendedFiles.objects.filter(blockid=self)
    
    def get_aiupanel(self):
        return PanelsBlock.objects.filter(blockid=self)

class TextBlock(models.Model):
    blockid = models.ForeignKey(Blocks, on_delete=models.CASCADE, related_name="textblock_num")
    contenthtml = RichTextField(default="")

    class Meta:
        verbose_name = 'Текст блок'
        verbose_name_plural = 'Текст блок'

    def __str__(self):
        return self.contenthtml

class ContactBlock(models.Model):
    blockid = models.ForeignKey(Blocks, on_delete=models.CASCADE, related_name="contact_num")
    col01html = models.TextField(default="")
    post_addr = models.TextField(default="")
    seo_pr = models.TextField(default="")
    tel = models.CharField(default="", max_length=255)
    fax = models.CharField(default="", max_length=255)
    email = models.CharField(default="", max_length=255)

    class Meta:
        verbose_name = 'Контакты блок'
        verbose_name_plural = 'Контакты блок'

    def __str__(self):
        return "Контакты блок"
    
class ModernBlock(models.Model):
    blockid = models.ForeignKey(Blocks, on_delete=models.CASCADE, related_name="modern_num")
    
    class Meta:
        verbose_name = 'Блок плиток'
        verbose_name_plural = 'Блок плиток'

    def __str__(self):
        return "Блоки плиток"
    
    def get_items(self):
        return ModernItem.objects.filter(modern=self)
    
class ModernItem(models.Model):
    modern = models.ForeignKey(ModernBlock, on_delete=models.CASCADE, related_name="modernitem_num")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")
    title = models.CharField(default="#.", max_length=120, verbose_name="Заголовок")
    link_url = models.CharField(default="#.", max_length=100, verbose_name="Ссылка")
    background = models.ImageField(upload_to='%d-%m-%Y/', blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Элемент плиток'
        verbose_name_plural = 'Элемент плиток'

    def __str__(self):
        return self.title
    
class DiagrBlock(models.Model):
    blockid = models.ForeignKey(Blocks, on_delete=models.CASCADE, related_name="diagr_num")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Строка", help_text="Строка, название диаграммы/структуры")

    class Meta:
        verbose_name = 'Диграмма для структуры'
        verbose_name_plural = 'Диграмма для структуры'

    def __str__(self):
        return 'Диграмма для структуры'
    
    def get_row(self):
        return DiagrRow.objects.filter(tableid=self)

class DiagrRow(models.Model):
    tableid = models.ForeignKey(DiagrBlock, on_delete=models.CASCADE, related_name="drow_num")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Строка", help_text="Строка, название")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")

    class Meta:
        ordering = ['order']
        verbose_name = 'Строка сетки'
        verbose_name_plural = 'Строка сетки'

    def __str__(self):
        return self.title
    
    def get_col(self):
        return DiagrColumn.objects.filter(rowid=self)

class DiagrColumn(models.Model):
    rowid = models.ForeignKey(DiagrRow, on_delete=models.CASCADE, related_name="dcol_num")
    slug = models.CharField(default="", max_length=255, editable=False)
    title = models.CharField(default="", max_length=255, verbose_name="Колонка", help_text="Отображаемое название")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")

    class Meta:
        ordering = ['order']
        verbose_name = 'Колонка сетки'
        verbose_name_plural = 'Колонка сетки'

    def __str__(self):
        return self.title
    
    def get_elem(self):
        return DiagrElement.objects.filter(colid=self)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[0:60]
        super().save(*args, **kwargs)
    
class DiagrElement(models.Model):
    colid = models.ForeignKey(DiagrColumn, on_delete=models.CASCADE, related_name="delem_num")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Подотдел", help_text="Название элемента")
    fio = models.CharField(default="", blank=True, max_length=255, verbose_name="ФИО", help_text="Фамилия Имя Отчество")
    tel = models.CharField(default="", blank=True, max_length=255, verbose_name="Телефон", help_text="Телефон")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")

    class Meta:
        ordering = ['order']
        verbose_name = 'Раскрывающийся элемент'
        verbose_name_plural = 'Раскрывающийся элемент'

    def __str__(self):
        return self.title
    
#Files module
#Tags menu
class TagsMenu(models.Model):
    titlemenu = models.CharField(default="", blank=True, max_length=255, verbose_name="Название критерия файла", help_text="Название критерия файла по которому идёт выборка")
    order = models.IntegerField(default=0, verbose_name="Приоритет", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")
    sidebar = models.BooleanField(default=False, verbose_name="Отображение боковым меню", help_text="Отображение фальтра категорий боковым меню")
    slug = models.CharField(default="", max_length=255, editable=False)

    class Meta:
        ordering = ['order']
        verbose_name = 'Меню тегов'
        verbose_name_plural = 'Меню тегов'

    def __str__(self):
        return self.titlemenu
    
    def get_itemtag(self):
        return TagsItem.objects.filter(tagsmenuid=self)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titlemenu)[0:60]
        super().save(*args, **kwargs)
    
class TagsItem(models.Model):
    tagsmenuid = models.ForeignKey(TagsMenu, on_delete=models.CASCADE, related_name="tagsmenu_url")
    order = models.IntegerField(default=0, verbose_name="Приоритет отображения", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")
    slug = models.CharField(default="", max_length=255, editable=False)
    titleitem = models.CharField(default="", blank=True, max_length=80, verbose_name="Название элемента выборки", help_text="Вариант выборки")

    class Meta:
        ordering = ['order']
        verbose_name = 'Тег'
        verbose_name_plural = 'Тег'

    def __str__(self):
        return self.titleitem + ' (Меню: ' + self.tagsmenuid.titlemenu + ')'
    
    def get_files(self):
        return FilesUpload.objects.filter(tagsid__in=self)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titleitem)[0:60]
        super().save(*args, **kwargs)
    
#Files
class FilesUpload(models.Model):
    filesUrl = models.FileField(upload_to=user_directory_path, verbose_name="Файл на сервере", validators=[validate_file_extension])
    filetype = models.CharField(default="", max_length=255, editable=False, verbose_name="Тип файла", help_text="Название файла отображаемое в таблице")
    title = models.CharField(default="", max_length=255, verbose_name="Название файла", help_text="Название файла отображаемое в таблице")
    tagsid = models.ManyToManyField(TagsItem, null=True, blank=True, related_name="tagsitem_url")
    date_pub = models.DateTimeField(verbose_name="Дата публикации", help_text="Установка дата публикации в таблице")
    pageid = models.ManyToManyField(Pages, null=True, blank=True, related_name="page_pub_file")

    class Meta:
        ordering = ['-date_pub']
        verbose_name = 'Файлы и документы'
        verbose_name_plural = 'Файлы и документы'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.filesUrl and self.filesUrl.url:
            try:
                self.filetype = mimetypes.guess_type(self.filesUrl.url)[0]
            except:
                pass
        super().save(*args, **kwargs)
    
#Extended ViewFiles
class ExtendedFiles(models.Model):
    blockid = models.ForeignKey(Blocks, on_delete=models.CASCADE, related_name="blockview")
    tagmenu = models.ManyToManyField(TagsMenu, related_name="files_id")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Заголовок (если необходим)", help_text="Заголовок раздела для поиска")
    tableview = models.BooleanField(default=False, verbose_name="Табличный вид", help_text="Отображение шапки, подписей и т.д.")
    date = models.BooleanField(default=False, verbose_name="Отображение даты публикации в таблице", help_text="(Не работает без табличного вида) Отображает колонку дату публикации")

    class Meta:
        verbose_name = 'Блок файловых элементов'
        verbose_name_plural = 'Блок файловых элементов'

    def __str__(self):
        return self.title
    
class PanelsBlock(models.Model):
    blockid = models.ForeignKey(Blocks, on_delete=models.CASCADE, related_name="aiupanels")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Заголовок (если необходим)", help_text="Заголовок для блока")

    class Meta:
        verbose_name = 'Панель блок ссылок'
        verbose_name_plural = 'Панель блок ссылок'
    
    def __str__(self):
        return self.title
    
    def getblock(self):
        return PanelBlockItem.objects.filter(panelid=self)

class PanelBlockItem(models.Model):
    panelid = models.ForeignKey(PanelsBlock, on_delete=models.CASCADE, related_name="aiupanelblock")
    urls = models.CharField(default="", blank=True, max_length=255, verbose_name="Ссылка", help_text="Ссылка для открытия")
    nowpage = models.BooleanField(default=True, verbose_name="Открывать ссылку в новой вкладке", help_text="Выбор открывать ссылку в новой вкладке или с перезагрузкой в текущей, для пользователей практично в новой вкладке")
    title = models.CharField(default="", blank=True, max_length=255, verbose_name="Текст", help_text="Выводимый текст для ссылки")
    order = models.IntegerField(default=0, verbose_name="Приоритет отображения", help_text="Чем меньше число, тем выше приоритет, как порядковый номер")

    class Meta:
        verbose_name = 'Элементы панели'
        verbose_name_plural = 'Элементы панели'

    def __str__(self):
        return self.title