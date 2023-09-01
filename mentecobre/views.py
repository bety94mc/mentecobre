from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt


from datetime import date

from .forms import TranslateArticleForm, AssignArticleForm, ReviewArticleForm
from .models import Glossary, Articles
from .manager import TranslateManager, ReviewManager
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

class ReviewView(View):
    def get(self, request):
        user = request.user
        userid = user.id
        username = user.username
        universes = user.universe

        article_assigned = ReviewManager.get_assigned_articles_for_user(userid)
        list_next_articles_to_assign = ReviewManager().get_list_next_article_to_assign(universes, userid)

        form = ReviewArticleForm()

        return render(
            request,
            'mentecobre/reviews.html',
            context={"user": username, "article_assigned": article_assigned,
                     "next_articles_to_assign": list_next_articles_to_assign, "form":form},
        )

    def post(self, request):
        if 'form-review' in request.POST:
            form = ReviewArticleForm(request.POST)
            if form.is_valid():
                article_id = form.cleaned_data["articleID"]
                article_notes = form.cleaned_data["notes"]
                article_translated_date = date.today()
                Articles.objects.filter(pk=article_id).update(reviewed=True, reviewedDate=article_translated_date,
                                                              notes=article_notes, linkcopperen=True)
        elif 'form-assign-review' in request.POST:
            form = AssignArticleForm(request.POST)
            if form.is_valid():
                universe_id = form.cleaned_data["articleUniverseID"]
                userid = request.user.id
                assigned_date = date.today()

                article_assigned = ReviewManager.get_assigned_articles_for_user(userid)
                if article_assigned:
                    messages.error(request, 'Ya tienes un artículo asignado')

                else:
                    universe = Universe.objects.get(id=universe_id)
                    ReviewManager().assign_article_to_user(universe, userid, assigned_date)
                    messages.info(request, 'Se ha asignado el artículo con éxito')

        return redirect('review')

class TranslateView(View):
    def get(self, request):
        user = request.user
        userid = user.id
        username = user.username
        universes = user.universe

        article_assigned = TranslateManager.get_assigned_articles_for_user(userid)
        list_next_articles_to_assign = TranslateManager().get_list_next_article_to_assign(universes)


        return render(
            request,
            'mentecobre/translations.html',
            context={"user": username, "article_assigned": article_assigned,
                     "next_articles_to_assign": list_next_articles_to_assign},
        )

    def post(self,request):
        if 'form-translate' in request.POST:
            form = TranslateArticleForm(request.POST)
            if form.is_valid():
                article_id =form.cleaned_data["articleID"]
                article_notes =form.cleaned_data ["notes"]
                article_translated_date = date.today()
                Articles.objects.filter(pk=article_id).update(translated=True, translatedDate=article_translated_date,
                                                              notes=article_notes)
        elif 'form-assign-translate' in request.POST:
            form = AssignArticleForm(request.POST)
            if form.is_valid():
                universe_id = form.cleaned_data["articleUniverseID"]
                userid = request.user.id
                assigned_date = date.today()


                article_assigned = TranslateManager.get_assigned_articles_for_user(userid)
                if article_assigned:
                    messages.error(request, 'Ya tienes un artículo asignado')

                else:
                    universe = Universe.objects.get(id=universe_id)
                    TranslateManager().assign_article_to_user(universe, userid, assigned_date)
                    messages.info(request, 'Se ha asignado el artículo con éxito')

        return redirect('translate')