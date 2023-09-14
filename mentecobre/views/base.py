
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import ListView


from datetime import date

from mentecobre.forms import TranslateArticleForm, AssignArticleForm, ReviewArticleForm, ReReviewArticleForm, \
    ProblemArticleForm
from mentecobre.models import Glossary, Articles, Category
from mentecobre.manager import TranslateManager, ReviewManager, ReReviewManager, HomeManager, DatabaseManager, \
    CoppermindManager
from login_app.models import Universe

import locale

locale.setlocale(locale.LC_TIME, 'es_ES')

# Create your views here.
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'mentecobre/category.html'
    context_object_name = 'category_list'

class CopperproblemView(LoginRequiredMixin, View):
    def __init__(self):
        self.manager = CoppermindManager()
        self.databasemanager = DatabaseManager()

    def get(self, request):

        if not request.user.is_superuser:
            raise PermissionDenied

        inprogressCopper, reviewedCopper = self.manager.get_coppermind_values()
        reviewed_articles = self.databasemanager.get_qs_articles_reviewed()
        assigned_and_not_reviewed_articles = self.databasemanager.get_qs_articles_assigned_not_reviewed()

        num_reviewed = self.databasemanager.get_num_articles(reviewed_articles)
        num_assigned_and_not_reviewed = self.databasemanager.get_num_articles(assigned_and_not_reviewed_articles)
        num_inprogressCopper = len(inprogressCopper)
        num_reviewedCopper = len(reviewedCopper)

        articles_reviewed_list = list(reviewed_articles.values_list('pageidEs', 'titleEs'))
        assigned_and_not_reviewed_articles_list = list(
            assigned_and_not_reviewed_articles.values_list('pageidEs', 'titleEs')
        )

        error_qs, error_list = self.manager.assigned_and_reviewed_cross_check(
            inprogressCopper, assigned_and_not_reviewed_articles_list, reviewedCopper, articles_reviewed_list
        )

        return render(
            request,
            'mentecobre/problemCopper.html',
            context={'num_reviewed': num_reviewed, 'num_assigned_and_not_reviewed': num_assigned_and_not_reviewed,
                     'num_inprogressCopper': num_inprogressCopper, 'num_reviewedCopper': num_reviewedCopper,
                     'error_qs': error_qs, 'error_list':error_list}
        )

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

        if 'form-fix-problemCopper' in request.POST:
            form = ProblemArticleForm(request.POST)
            if form.is_valid():
                article_id = form.cleaned_data["articleID"]
                Articles.objects.filter(pk=article_id).update(problemCopper=None)

        return redirect('copperproblem')


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

class HomeView(View):
    def __init__(self):
        self.manager = HomeManager()
        self.databasemanager = DatabaseManager()

    @xframe_options_exempt
    def get(self, request):

        num_articles_total = self.databasemanager.get_num_articles(self.databasemanager.get_qs_articles_all())
        num_articles_translated = self.databasemanager.get_num_articles(
            self.databasemanager.get_qs_articles_translate())
        num_articles_reviewed = self.databasemanager.get_num_articles(self.databasemanager.get_qs_articles_reviewed())

        translated_progress = self.manager.obtain_progress(num_articles_total, num_articles_translated)
        reviewed_progress = self.manager.obtain_progress(num_articles_total, num_articles_reviewed)
        diff_progress = translated_progress - reviewed_progress

        universes_chart = self.manager.get_universes_chart()
        month_chart = self.manager.get_month_chart()

        return render(
            request,
            'mentecobre/index.html',
            context={'num_articles_total': num_articles_total, 'num_articles_translated': num_articles_translated,
                     'num_articles_reviewed': num_articles_reviewed, 'translated_progress': translated_progress,
                     'reviewed_progress': reviewed_progress,'diff_progress':diff_progress,
                     'universes_chart': universes_chart, 'month_chart': month_chart}
        )

class RereviewView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    def get(self, request):
        user = request.user

        if not user.is_superuser:
            raise PermissionDenied

        userid = user.id
        username = user.username
        universes = user.universe

        article_assigned = ReReviewManager.get_assigned_articles_for_user(userid)
        list_next_articles_to_assign = ReReviewManager().get_list_next_article_to_assign(universes, userid)

        return render(
            request,
            'mentecobre/rereviews.html',
            context={"user": username, "article_assigned": article_assigned,
                     "next_articles_to_assign": list_next_articles_to_assign},
        )
    def post(self, request):

        if not request.user.is_superuser():
            raise PermissionDenied


        if 'form-rereview' in request.POST:
            form = ReReviewArticleForm(request.POST)
            if form.is_valid():
                article_id = form.cleaned_data["articleID"]
                Articles.objects.filter(pk=article_id).update(engregoriado=True)

        elif 'form-assign-rereview' in request.POST:
            form = AssignArticleForm(request.POST)
            if form.is_valid():
                universe_id = form.cleaned_data["articleUniverseID"]
                userid = request.user.id

                article_assigned = ReReviewManager.get_assigned_articles_for_user(userid)
                if article_assigned:
                    messages.error(request, 'Ya tienes un artículo asignado')

                else:
                    universe = Universe.objects.get(id=universe_id)
                    ReReviewManager().assign_article_to_user(universe, userid)
                    messages.info(request, 'Se ha asignado el artículo con éxito')

        return redirect('rereview')

class ReviewView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        user = request.user
        userid = user.id
        username = user.username
        universes = user.universe

        if not user.is_reviewer():
            raise PermissionDenied

        article_assigned = ReviewManager.get_assigned_articles_for_user(userid)
        list_next_articles_to_assign = ReviewManager().get_list_next_article_to_assign(universes, userid)

        return render(
            request,
            'mentecobre/reviews.html',
            context={"user": username, "article_assigned": article_assigned,
                     "next_articles_to_assign": list_next_articles_to_assign},
        )

    def post(self, request):

        if not request.user.is_reviewer():
            raise PermissionDenied

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

class TranslateView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

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