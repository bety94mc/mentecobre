from django.db import models


from login_app.models import CustomUser, Universe
# Create your models here.



class Articles(models.Model):
    typeOptions = (('CU', 'Cultura'), ('EVT', 'Eventos y eras'), ('FDV', 'Formas de vida'), ('LIB', 'Libros'),
                    ('LOC', 'Localizaciones'), ('MG', 'Magia'), ('PJ', 'Personajes'), ('OBJ', 'Objetos y materiales'),
                    ('ORG', 'Organización'), ('FAM', 'Familia'), ('MUL', 'Multimedia'), ('WIKI', 'Wiki/otros'),
                    ('DIS', 'Disambiguación'), ('RD', 'Redirección'), ('SUB', 'Subpágina'),)

    priorityOptions = (('1', 'Alta'), ('2', 'Media'), ('3', 'Baja'), ('4', 'TBD'), ('5', 'Siraya'),)

    pageidEn = models.IntegerField(null=True, blank=True, verbose_name='ID Coppermind en inglés')
    pageidEs = models.IntegerField(null=True, blank=True, verbose_name='ID Coppermind en español')
    titleEn = models.CharField(max_length=200, null=True, blank=True, verbose_name='Título inglés')
    titleEs = models.CharField(max_length=200, null=True, blank=True, verbose_name='Título español')
    type = models.CharField(max_length=4, choices=typeOptions, null=True, blank=True, verbose_name='Tipo de artículo')
    priority = models.CharField(max_length=1, choices=priorityOptions, null=True, blank=True,verbose_name='Prioridad')
    translator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   limit_choices_to={'groups__name': "Traductores"}, related_name='translator',
                                   verbose_name='Traductor')
    assignedDate = models.DateField(null=True, blank=True, verbose_name='Fecha asignado traductor')
    translated = models.BooleanField(default=False,verbose_name='Traducido')
    translatedDate = models.DateField(null=True, blank=True,verbose_name='Fecha traducido')
    reviewer = models.ForeignKey(CustomUser, models.DO_NOTHING, null=True, blank=True,
                                 limit_choices_to={'groups__name': "Revisores"}, related_name='reviewer',
                                 verbose_name='Revisor')
    reviewed = models.BooleanField(default=False, verbose_name='Revisado')
    reviewerassignedDate = models.DateField(null=True, blank=True, verbose_name='Fecha asignado revisor')
    reviewedDate = models.DateField(null=True, blank=True, verbose_name='Fecha revisado')
    gregorio = models.ForeignKey(CustomUser, models.DO_NOTHING, null=True, blank=True,
                                 limit_choices_to={'is_superuser': True}, related_name='gregorio')
    engregoriado = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True, verbose_name='notas')
    universe = models.ForeignKey(Universe, models.DO_NOTHING, null=True, blank=True, related_name='article_universe',
                                 verbose_name='Universo')
    urldrive = models.URLField(null=True, blank=True)
    urlEn = models.URLField(null=True, blank=True, verbose_name='Enlace Coppermind en inglés')
    urlEs = models.URLField(null=True, blank=True, verbose_name='Enlace Coppermind en español')
    linkcopperen = models.BooleanField(default=False, verbose_name='Enlazada con la Coppermind en inglés')
    problemCopper = models.TextField(null=True, blank=True, verbose_name='Problemas de la Copper')

    def __str__(self):
        return str(self.titleEs)

    def get_absolute_url(self):
        return reverse('titleEs', args=[str(self.id)])

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'

class Glossary(models.Model):

    wordEn = models.CharField(max_length=200, verbose_name='Palabra inglés')
    wordEs = models.CharField(max_length=200, null=True, blank=True, verbose_name='Palabra español')
    universe = models.ForeignKey(Universe, models.DO_NOTHING, null=True, blank=True, related_name='glossary_universe',
                                 verbose_name='Universo')
    urlEn = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Enlace Coppermind en inglés')
    urlEs = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Enlace Coppermind en español')

    def __str__(self):
        return str(self.wordEs)

    def get_absolute_url(self):
        return reverse('wordEs', args=[str(self.id)])

    class Meta:
        verbose_name = 'Glosario'
        verbose_name_plural = 'Glosario'


class Category(models.Model):

    catEn = models.CharField(max_length=200, verbose_name='Categoría inglés')
    catEs = models.CharField(max_length=200, null=True, blank=True, verbose_name='Categoría español')
    urlEn = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Enlace Coppermind en inglés')
    urlEs = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Enlace Coppermind en español')

    def __str__(self):
        return str(self.catEs)

    def get_absolute_url(self):
        return reverse('catEs', args=[str(self.id)])

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
