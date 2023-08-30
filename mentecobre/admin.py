from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter

from .models import Articles, Glossary, Category


class PrioridadListFilter(MultipleChoiceListFilter):
    title = 'Prioridad'
    parameter_name = 'priority__in'

    def lookups(self, request, model_admin):
        return Articles.priorityOptions

# Register your models here.
@admin.register(Articles)
class ArticlesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_confirm_sidebar.html"
    list_display = ('id', 'titleEn', 'titleEs', 'translator', 'translated', 'reviewer', 'reviewed', 'priority')

    search_fields = ('titleEn', 'titleEs')

    fieldsets = ((None, {'fields': ('pageidEn', 'pageidEs', 'titleEn', 'titleEs', 'type', 'priority', 'universe')}),
                 ('Estado Traducción', {'fields': ('translator', 'assignedDate', 'translated', 'translatedDate')}),
                 ('Estado Revisión', {'fields': (
                 'reviewer', 'reviewed', 'reviewerassignedDate', 'reviewedDate', 'gregorio', 'engregoriado')}),
                 ('Enlaces',{'fields':('urlEn','urlEs','urldrive', 'linkcopperen')}),
                 ('Apuntes', {'fields':('notes','problemCopper')})
                 )

    list_filter = ('translator', 'translated','reviewer', 'reviewed', 'universe',PrioridadListFilter,'linkcopperen')

@admin.register(Glossary)
class GlossaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'wordEn', 'wordEs', 'universe')
    list_filter = ['universe']
    search_fields = ('wordEn', 'wordEs')


@admin.register(Category)
class CategoriaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'catEn', 'catEs',)
    search_fields = ('catEn', 'catEs')