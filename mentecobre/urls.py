from django.urls import path, re_path


from .views import base

urlpatterns = [
    path('',base.GlossaryView.as_view(),name='home'),
    path('glosario',base.GlossaryView.as_view(),name='glossary'),
    path('juegos',base.GlossaryView.as_view(),name='games'),
    path('categorías',base.GlossaryView.as_view(),name='category'),
    path('traducciones',base.TranslateView.as_view(),name='translate'),
    path('revisiones',base.ReviewView.as_view(),name='review'),
    path('rerevisiones', base.RereviewView.as_view(), name='rereview'),
    path('gregorio',base.GlossaryView.as_view(),name='gregorio'),
    path('comparacion',base.GlossaryView.as_view(),name='comparison'),
    path('cambios',base.GlossaryView.as_view(),name='changes'),
    path('perfil',base.GlossaryView.as_view(),name='profile'),
    path('login',base.GlossaryView.as_view(),name='login'),

]