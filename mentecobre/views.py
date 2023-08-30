from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt


from datetime import date

from .models import Glossary, Articles
from .manager import TranslateManager
from login_app.models import Universe


# Create your views here.

class GlossaryView(View):

    @xframe_options_exempt
    def get(self, request):
        search = request.GET.get("q", None)
        if search is not None:
            query = search
            object_list = Glossary.objects.filter(
                Q(wordEn__icontains=query) | Q(wordEs__icontains=query)
            )

        else:
            object_list = None

        return render(
            request,
            'mentecobre/glossary.html',
            context={"object_list": object_list}
        )

class TranslateView(View):
    def get(self, request):
        user = request.user
        userid = user.id
        username = user.username
        universes = user.universe

        article_assigned = TranslateManager.assigned_articles_for_user(userid)
        list_next_articles_to_assign = TranslateManager().get_list_next_article_to_assign(universes)


        return render(
            request,
            'mentecobre/traducciones.html',
            context={"user": username, "article_assigned": article_assigned,
                     "next_articles_to_assign": list_next_articles_to_assign},
        )

    def post(self,request):
        if 'form-translate' in request.POST:
            article_id = request.POST.get("articleID", None)
            article_notes = request.POST.get("notes")
            article_translated_date = date.today()
            Articles.objects.filter(pk=article_id).update(translated=True, translatedDate=article_translated_date,
                                                          notes=article_notes)
        elif 'form-next-article' in request.POST:
            userid = request.user.id
            universe_id = request.POST.get("nextArticleUniverse", None)
            assigned_date = date.today()


            article_assigned = TranslateManager.assigned_articles_for_user(userid)
            if article_assigned:
                messages.error(request, 'Ya tienes un artículo asignado')

            else:
                universe = Universe.objects.get(id=universe_id)
                TranslateManager().assign_article_to_user(universe, userid, assigned_date)
                messages.info(request, 'Se ha asignado el artículo con éxito')

        return redirect('translate')