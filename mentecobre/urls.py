from django.contrib.auth.decorators import login_required
from django.urls import path, re_path


from . import views

urlpatterns = [
    path('portada',views.GlossaryView.as_view(),name='home'),
    path('glosario',views.GlossaryView.as_view(),name='glossary'),
    path('juegos',views.GlossaryView.as_view(),name='games'),
    path('categorías',views.GlossaryView.as_view(),name='category'),
    path('traducciones',login_required(views.TranslateView.as_view()),name='translate'),
    path('revisiones',login_required(views.ReviewView.as_view()),name='review'),
    path('rerevisiones', views.GlossaryView.as_view(), name='rereview'),
    path('gregorio',views.GlossaryView.as_view(),name='gregorio'),
    path('comparacion',views.GlossaryView.as_view(),name='comparison'),
    path('cambios',views.GlossaryView.as_view(),name='changes'),
    path('perfil',views.GlossaryView.as_view(),name='profile'),
    path('login',views.GlossaryView.as_view(),name='login'),

]