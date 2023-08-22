from django.contrib import admin
import nested_admin
from aiupages.models import *

# Register your models here.
#Extended View File
class ExtendedFilesInline(nested_admin.NestedTabularInline):
    extra = 0
    model = ExtendedFiles

#Tags Files
class TagsItemInline(nested_admin.NestedTabularInline):
    extra = 0
    model = TagsItem

class TagsMenuInline(nested_admin.NestedStackedInline):
    extra = 0
    model = TagsMenu
    inlines = [TagsItemInline]

class TagsMenuAdmin(nested_admin.NestedModelAdmin):
    extra = 0
    model = TagsMenu
    inlines = [TagsItemInline]

#Files
class FilesUploadAdmin(nested_admin.NestedModelAdmin):
    extra = 0
    model = FilesUpload
    list_display = ('title', 'filetype', '_tagsid', '_filesurl')
    list_filter = ['filetype']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        kwargs["queryset"] = TagsItem.objects.all()
        return super(FilesUploadAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def _filesurl(self, row):
        return row.filesUrl.url

    def	_tagsid(self, row):
        return ', \n\r'.join([x.titleitem for x in row.tagsid.all()])

class DiagrElemInline(nested_admin.NestedTabularInline):
    extra = 0
    model = DiagrElement

#Column in Row Diagram
class DiagrColumnInline(nested_admin.NestedStackedInline):
    extra = 0
    model = DiagrColumn
    inlines = [DiagrElemInline]

#Row in Diagram
class DiagrRowInline(nested_admin.NestedStackedInline):
    extra = 0
    model = DiagrRow
    inlines = [DiagrColumnInline]

#Elements Diagram Structure
class DiagrBlockInline(nested_admin.NestedStackedInline):
    extra = 0
    model = DiagrBlock
    inlines = [DiagrRowInline]

#ModernUI items
class ModernItemInline(nested_admin.NestedTabularInline):
    extra = 0
    model = ModernItem

#Elements ModernUI
class ModernBlockInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ModernBlock
    inlines = [ModernItemInline]

#Elements TXT
class TextBlockInline(nested_admin.NestedStackedInline):
    extra = 0
    model = TextBlock

#Elements contact
class ContactBlockInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ContactBlock

#Block (row) in Container
class BlocksInline(nested_admin.NestedStackedInline):
    extra = 0
    model = Blocks
    inlines = [TextBlockInline, ModernBlockInline, ContactBlockInline, DiagrBlockInline, ExtendedFilesInline]

#Container in Page
class ContainersInline(nested_admin.NestedStackedInline):
    extra = 0
    model = Containers
    inlines = [BlocksInline]

#Page properties
class PagesAdmin(nested_admin.NestedModelAdmin):
    model = Pages
    inlines = [ContainersInline]
    extra = 0

admin.site.register(Pages, PagesAdmin)
admin.site.register(FilesUpload, FilesUploadAdmin)
admin.site.register(TagsMenu, TagsMenuAdmin)

'''
class PagesAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change: # Проверяем что запись только создаётся
            obj.author = request.user # Присваеваем полю автор текущего пользователя
    
        super(PagesAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )
        '''
