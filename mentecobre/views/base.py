import random

import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import ListView

from datetime import date

from mentecobre.forms import TranslateArticleForm, AssignArticleForm, ReviewArticleForm, ReReviewArticleForm, \
    ProblemArticleForm, ChangesForm, GregorioForm
from mentecobre.models import Glossary, Articles, Category
from mentecobre.manager import TranslateManager, ReviewManager, ReReviewManager, HomeManager, DatabaseManager, \
    CoppermindManager, GregorioManager
from login_app.models import Universe, CustomUser

import locale

import logging

from mentecobre.views.errors import error_403, error_500, error_400

# Get an instance of a logger
logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_TIME, "es_ES")


# Create your views here.
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "mentecobre/category.html"
    context_object_name = "category_list"


class ChangesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            form = ChangesForm(initial={"start_date": date.today().strftime("%Y-%m-%d"),
                                        "end_date": date.today().strftime("%Y-%m-%d")})
            return render(
                request,
                "mentecobre/changesCopper.html",
                context={"form": form},
            )
        except PermissionDenied:
            logger.error("Permission error - get - ChangesView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - ChangesView")
            logger.error(ex)
            return error_500(request)
    def post(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            form = ChangesForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]

                manager = CoppermindManager()
                dates_list = manager.split_period_in_weeks(start_date, end_date)
                changes_df = manager.get_changes(dates_list)
                new_articles = manager.get_new_articles(changes_df)
                translated_articles = manager.get_translated_articles(changes_df)
                not_assigned_not_translated_articles = manager.get_not_assigned_not_translated_articles(changes_df)
                moved_articles = manager.get_moved_articles(changes_df)

                response = HttpResponse(content_type="application/xlsx")
                response["Content-Disposition"] = "attachment; filename='Cambios.xlsx'"
                with pd.ExcelWriter(response) as writer:
                    new_articles.to_excel(writer, sheet_name="Articulos_nuevos")
                    translated_articles.to_excel(writer, sheet_name="Articulos_traducidos")
                    not_assigned_not_translated_articles.to_excel(writer, sheet_name="Articulos_sin_traducir")
                    moved_articles.to_excel(writer, sheet_name="HTUP")
                    return response
            else:
                raise ValidationError(form.errors)

        except PermissionDenied:
            logger.error("Permission error - post - ChangesView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except ValidationError as err:
            logger.error("Validation error - post - ChangesView")
            logger.error("form is not valid")
            logger.error(err)
            return error_400(request, err)

        except Exception as ex:
            logger.error("Error - post - ChangesView")
            logger.error(ex)
            return error_500(request)

class CopperHopperView(View):
    def __init__(self):
        self.databasemanager = DatabaseManager()

    @xframe_options_exempt
    def get(self, request):
        try:

            articulos_traducidos = self.databasemanager.get_qs_articles_translate()

            random_articles = random.sample(list(articulos_traducidos.values()), 2)
            return render(
                request,
                "mentecobre/copperhopper.html",
                context={"random_articles": random_articles}
            )
        except Exception as ex:
            logger.error("Error - get - CopperHopperView")
            logger.error(ex)
            return error_500(request)


class CopperListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            manager = CoppermindManager()
            copper_list_english = manager.get_articles("en")
            copper_list_spanish = manager.get_articles("es")
            response = HttpResponse(content_type="application/xlsx")
            response["Content-Disposition"] = "attachment; filename='articuloscopper.xlsx'"
            with pd.ExcelWriter(response) as writer:
                copper_list_english.to_excel(writer, sheet_name="Articulos_listado ingles")
                copper_list_spanish.to_excel(writer, sheet_name="Articulos_listado español")

            return response

        except PermissionDenied:
            logger.error("Permission error - get - CopperListView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - CopperListView")
            logger.error(ex)
            return error_500(request)


class CopperProblemView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            manager = CoppermindManager()
            databasemanager = DatabaseManager()

            inprogress_copper, reviewed_copper = manager.get_coppermind_values()
            reviewed_articles = databasemanager.get_qs_articles_reviewed()
            assigned_and_not_reviewed_articles = databasemanager.get_qs_articles_assigned_not_reviewed()

            num_reviewed = databasemanager.get_num_articles(reviewed_articles)
            num_assigned_and_not_reviewed = databasemanager.get_num_articles(assigned_and_not_reviewed_articles)
            num_inprogress_copper = len(inprogress_copper)
            num_reviewed_copper = len(reviewed_copper)

            articles_reviewed_list = list(reviewed_articles.values_list("pageidEs", "titleEs"))
            assigned_and_not_reviewed_articles_list = list(
                assigned_and_not_reviewed_articles.values_list("pageidEs", "titleEs")
            )

            error_qs, error_list = manager.assigned_and_reviewed_cross_check(
                inprogress_copper, assigned_and_not_reviewed_articles_list, reviewed_copper, articles_reviewed_list
            )

            return render(
                request,
                "mentecobre/problemCopper.html",
                context={"num_reviewed": num_reviewed, "num_assigned_and_not_reviewed": num_assigned_and_not_reviewed,
                         "num_inprogressCopper": num_inprogress_copper, "num_reviewedCopper": num_reviewed_copper,
                         "error_qs": error_qs, "error_list": error_list}
            )
        except PermissionDenied:
            logger.error("Permission error - get - CopperProblemView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - CopperProblemView")
            logger.error(ex)
            return error_500(request)

    def post(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            form = ProblemArticleForm(request.POST)
            if form.is_valid():
                article_id = form.cleaned_data["articleID"]
                Articles.objects.filter(pk=article_id).update(problemCopper=None)
                return redirect("copperproblem")
            else:
                raise ValidationError(form.errors)

        except PermissionDenied:
            logger.error("Permission error - post - CopperProblemView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except ValidationError as err:
            logger.error("Validation error - post - CopperProblemView")
            logger.error("form is not valid")
            logger.error(err)
            return error_400(request, err)

        except Exception as ex:
            logger.error("Error - post - CopperProblemView")
            logger.error(ex)
            return error_500(request)


class GlossaryView(View):

    @xframe_options_exempt
    def get(self, request):
        try:
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
                "mentecobre/glossary.html",
                context={"object_list": object_list}
            )
        except Exception as ex:
            logger.error("Error - get - GlossaryView")
            logger.error(ex)
            return error_500(request)

class GregorioView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            users_list = GregorioManager().get_users_list()

            return render(
                request,
                "mentecobre/gregorio.html",
                context={"users_list": users_list},
            )
        except PermissionDenied:
            logger.error("Permission error - get - GregorioView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - GregorioView")
            logger.error(ex)
            return error_500(request)

    def post(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            form = GregorioForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data["username"]
                status = form.cleaned_data["status"]

                today = date.today()
                if status == "Resting":
                    CustomUser.objects.filter(username=username).update(is_resting=True, is_active=False,
                                                                        timeoff_date=today)
                elif status == "Inactive":
                    CustomUser.objects.filter(username=username).update(is_resting=False, is_active=False, is_staff=False,
                                                                        out_date=today)
                elif status == "Active":
                    CustomUser.objects.filter(username=username).update(is_resting=False, is_active=True, out_date=None)
                else:
                    raise Exception("Not valid status")

                return redirect("gregorio")
            else:
                raise ValidationError(form.errors)

        except PermissionDenied:
            logger.error("Permission error - post - GregorioView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except ValidationError as err:
            logger.error("Validation error - post - GregorioView")
            logger.error("form is not valid")
            logger.error(err)
            return error_400(request, err)

        except Exception as ex:
            logger.error("Error - post - GregorioView")
            logger.error(ex)
            return error_500(request)

class HomeView(View):

    @xframe_options_exempt
    def get(self, request):
        try:
            manager = HomeManager()
            databasemanager = DatabaseManager()

            num_articles_total = databasemanager.get_num_articles(databasemanager.get_qs_articles_all())
            num_articles_translated = databasemanager.get_num_articles(
                databasemanager.get_qs_articles_translate())
            num_articles_reviewed = databasemanager.get_num_articles(databasemanager.get_qs_articles_reviewed())

            translated_progress = manager.obtain_progress(num_articles_total, num_articles_translated)
            reviewed_progress = manager.obtain_progress(num_articles_total, num_articles_reviewed)
            diff_progress = translated_progress - reviewed_progress

            universes_chart = manager.get_universes_chart()
            month_chart = manager.get_month_chart()

            return render(
                request,
                "mentecobre/index.html",
                context={"num_articles_total": num_articles_total, "num_articles_translated": num_articles_translated,
                         "num_articles_reviewed": num_articles_reviewed, "translated_progress": translated_progress,
                         "reviewed_progress": reviewed_progress, "diff_progress": diff_progress,
                         "universes_chart": universes_chart, "month_chart": month_chart}
            )

        except Exception as ex:
            logger.error("Error - get - HomeView")
            logger.error(ex)
            return error_500(request)


class RereviewView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        try:

            if not user.is_superuser:
                raise PermissionDenied

            userid = user.id
            username = user.username
            universes = user.universe

            article_assigned = ReReviewManager.get_assigned_articles_for_user(userid)
            list_next_articles_to_assign = ReReviewManager().get_list_next_article_to_assign(universes, userid)

            return render(
                request,
                "mentecobre/rereviews.html",
                context={"user": username, "article_assigned": article_assigned,
                         "next_articles_to_assign": list_next_articles_to_assign},
            )

        except PermissionDenied:
            logger.error("Permission error - get - RereviewView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - RereviewView")
            logger.error(ex)
            return error_500(request)

    def post(self, request):
        user = request.user
        try:
            if not user.is_superuser:
                raise PermissionDenied

            if "form-rereview" in request.POST:
                form = ReReviewArticleForm(request.POST)
                if form.is_valid():
                    article_id = form.cleaned_data["articleID"]
                    Articles.objects.filter(pk=article_id).update(engregoriado=True)
                else:
                    raise ValidationError(form.errors)

            elif "form-assign-rereview" in request.POST:
                form = AssignArticleForm(request.POST)
                if form.is_valid():
                    universe_id = form.cleaned_data["articleUniverseID"]
                    userid = request.user.id

                    article_assigned = ReReviewManager.get_assigned_articles_for_user(userid)
                    if article_assigned:
                        messages.error(request, "Ya tienes un artículo asignado")

                    else:
                        universe = Universe.objects.get(id=universe_id)
                        ReReviewManager().assign_article_to_user(universe, userid)
                        messages.info(request, "Se ha asignado el artículo con éxito")
                else:
                    raise ValidationError(form.errors)

            else:
                raise Exception("There is no form included in POST request")

            return redirect("rereview")
        except PermissionDenied:
            logger.error("Permission error - post - RereviewView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except ValidationError as err:
            logger.error("Validation error - post - RereviewView")
            logger.error("form is not valid")
            logger.error(err)
            return error_400(request, err)

        except Exception as ex:
            logger.error("Error - post - RereviewView")
            logger.error(ex)
            return error_500(request)


class ReviewView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            userid = user.id
            username = user.username
            universes = user.universe

            if not user.is_reviewer():
                raise PermissionDenied

            article_assigned = ReviewManager.get_assigned_articles_for_user(userid)
            list_next_articles_to_assign = ReviewManager().get_list_next_article_to_assign(universes, userid)

            return render(
                request,
                "mentecobre/reviews.html",
                context={"user": username, "article_assigned": article_assigned,
                         "next_articles_to_assign": list_next_articles_to_assign},
            )
        except PermissionDenied:
            logger.error("Permission error - get - ReviewView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - ReviewView")
            logger.error(ex)
            return error_500(request)

    def post(self, request):
        user = request.user
        try:
            if not user.is_reviewer():
                raise PermissionDenied

            if "form-review" in request.POST:
                form = ReviewArticleForm(request.POST)
                if form.is_valid():
                    article_id = form.cleaned_data["articleID"]
                    article_notes = form.cleaned_data["notes"]
                    article_translated_date = date.today()
                    Articles.objects.filter(pk=article_id).update(reviewed=True, reviewedDate=article_translated_date,
                                                                  notes=article_notes, linkcopperen=True)
                else:
                    raise ValidationError(form.errors)
            elif "form-assign-review" in request.POST:
                form = AssignArticleForm(request.POST)
                if form.is_valid():
                    universe_id = form.cleaned_data["articleUniverseID"]
                    userid = request.user.id
                    assigned_date = date.today()

                    article_assigned = ReviewManager.get_assigned_articles_for_user(userid)
                    if article_assigned:
                        messages.error(request, "Ya tienes un artículo asignado")

                    else:
                        universe = Universe.objects.get(id=universe_id)
                        ReviewManager().assign_article_to_user(universe, userid, assigned_date)
                        messages.info(request, "Se ha asignado el artículo con éxito")
                else:
                    raise ValidationError(form.errors)
            else:
                raise Exception("There is no form included in POST request")

            return redirect("review")

        except PermissionDenied as err:
            logger.error("Permission error - post - ReviewView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, err)

        except ValidationError as err:
            logger.error("Validation error - post - ReviewView")
            logger.error("form is not valid")
            logger.error(err)
            return error_400(request, err)

        except Exception as ex:
            logger.error("Error - post - ReviewView")
            logger.error(ex)
            return error_500(request)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username=None):
        try:
            if not username:
                user = request.user
            else:
                if not request.user.is_superuser:
                    raise PermissionDenied
                user = get_object_or_404(CustomUser, username=username)
            userid = user.id
            translator_assigned_articles = None
            translator_assigned_articles_finished_count = 0
            reviewer_assigned_articles = None
            reviewer_assigned_articles_finished_count = 0

            if user.is_translator():
                translator_assigned_articles = DatabaseManager.get_qs_articules_assigned_to_user(userid, "Translator")
                translator_assigned_articles_finished = DatabaseManager.get_qs_articules_assigned_to_user_finished(userid,
                                                                                                                   "Translator")
                translator_assigned_articles_finished_count = DatabaseManager.get_num_articles(
                    translator_assigned_articles_finished)

            if user.is_reviewer():
                reviewer_assigned_articles = DatabaseManager.get_qs_articules_assigned_to_user(userid, "Reviewer")
                reviewer_assigned_articles_finished = DatabaseManager.get_qs_articules_assigned_to_user_finished(userid,
                                                                                                                 "Reviewer")
                reviewer_assigned_articles_finished_count = DatabaseManager.get_num_articles(
                    reviewer_assigned_articles_finished)

            return render(
                request,
                "mentecobre/profile.html",
                context={"user": user,
                         "translator_assigned": translator_assigned_articles,
                         "reviewer_assigned": reviewer_assigned_articles,
                         "num_translated": translator_assigned_articles_finished_count,
                         "num_reviewed": reviewer_assigned_articles_finished_count
                         },
            )
        except PermissionDenied:
            logger.error("Permission error - get - ProfileView")
            logger.error(f"{request.user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - ProfileView")
            logger.error(ex)
            return error_500(request)


class TranslateView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        try:
            if not user.is_translator():
                raise PermissionDenied
            userid = user.id
            username = user.username
            universes = user.universe

            article_assigned = TranslateManager.get_assigned_articles_for_user(userid)
            list_next_articles_to_assign = TranslateManager().get_list_next_article_to_assign(universes)

            return render(
                request,
                "mentecobre/translations.html",
                context={"user": username, "article_assigned": article_assigned,
                         "next_articles_to_assign": list_next_articles_to_assign},
            )

        except PermissionDenied:
            logger.error("Permission error - get - TranslateView")
            logger.error("{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except Exception as ex:
            logger.error("Error - get - TranslateView")
            logger.error(ex)
            return error_500(request)

    def post(self, request):
        user = request.user
        try:
            if not user.is_translator:
                raise PermissionDenied
            if "form-translate" in request.POST:
                form = TranslateArticleForm(request.POST)
                if form.is_valid():
                    article_id = form.cleaned_data["articleID"]
                    article_notes = form.cleaned_data["notes"]
                    article_translated_date = date.today()
                    Articles.objects.filter(pk=article_id).update(translated=True, translatedDate=article_translated_date,
                                                                  notes=article_notes)
                else:
                    raise ValidationError(form.errors)
            elif "form-assign-translate" in request.POST:
                form = AssignArticleForm(request.POST)
                if form.is_valid():
                    universe_id = form.cleaned_data["articleUniverseID"]
                    userid = user.id
                    assigned_date = date.today()

                    article_assigned = TranslateManager.get_assigned_articles_for_user(userid)
                    if article_assigned:
                        messages.error(request, "Ya tienes un artículo asignado")

                    else:
                        universe = Universe.objects.get(id=universe_id)
                        TranslateManager().assign_article_to_user(universe, userid, assigned_date)
                        messages.info(request, "Se ha asignado el artículo con éxito")
                else:
                    raise ValidationError(form.errors)
            else:
                raise Exception("There is no form included in POST request")

            return redirect("translate")

        except PermissionDenied as err:
            logger.error("Permission error - post - TranslateView")
            logger.error(f"{user} has not allowed to access to this view")
            return error_403(request, PermissionDenied)

        except ValidationError as err:
            logger.error("Validation error - post - TranslateView")
            logger.error("form is not valid")
            logger.error(err)
            return error_400(request, err)

        except Exception as ex:
            logger.error("Error - post - TranslateView")
            logger.error(ex)
            return error_500(request)
