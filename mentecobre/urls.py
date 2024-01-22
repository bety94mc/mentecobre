from django.urls import path, re_path


from .views import base

urlpatterns = [
    path('', base.HomeView.as_view(), name='home'),
    path('glosario', base.GlossaryView.as_view(), name='glossary'),
    path('juegos', base.CopperHopperView.as_view(), name='games'),
    path('categorías', base.CategoryListView.as_view(), name='category'),
    path('traducciones', base.TranslateView.as_view(), name='translate'),
    path('revisiones', base.ReviewView.as_view(), name='review'),
    path('rerevisiones', base.RereviewView.as_view(), name='rereview'),
    path('gregorio', base.GregorioView.as_view(), name='gregorio'),
    path('problemasCopper', base.CopperProblemView.as_view(), name='copperproblem'),
    path('cambios', base.ChangesListsView.as_view(), name='changes'),
    # path('cambios/listadocopper', base.CopperListView.as_view(), name='copperlist'),
    path('perfil', base.ProfileView.as_view(), name='profile'),
    path('perfil/<username>/', base.ProfileView.as_view(), name='user-profile'),
    path('login', base.GlossaryView.as_view(), name='login'),
]
