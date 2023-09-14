from abc import ABC, abstractmethod
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import requests

from .models import Articles
from login_app.models import Universe

EXCLUDED_TYPE = ['RD', 'DIS', 'SUB']
EXCLUDED_UNIVERSES = [13]
PRIORITY_OPTIONS = [1, 2, 3]

class CoppermindManager:
    @staticmethod
    def conect_to_coppermind(url, params):
        response = requests.Session().get(url=url, params=params)
        return response.json()

    def assigned_and_reviewed_cross_check(self,inprogress_list, assigned_list, reviewedCopper_list, articles_reviewed_list):
        error_list = []
        error_inprogress = 'Este artículo está en In progress pero no está asignado a nadie'
        error_asigned = 'Este artículo está asignado pero no está en In progress'
        error_translated_page = 'Este artículo está en Translated page pero no está marcado como revisado'
        error_reviewed = 'Este artículo está revisado pero no está en Translated page'

        for inprogress in inprogress_list:
            if tuple(inprogress) not in assigned_list:
                try:
                    article_error = Articles.objects.get(pageidEs=inprogress[0])
                    if article_error.problemCopper:
                        if error_inprogress not in article_error.problemCopper:
                            article_error.problemCopper = f'{article_error.problemCopper} \n{error_inprogress}'
                    else:
                        article_error.problemCopper = error_inprogress
                    article_error.save()
                except ObjectDoesNotExist as e:
                    error_list.append((inprogress[1], 'Tiene un in_progress'))

        for asigned in assigned_list:
            if list(asigned) not in inprogress_list:
                article_error = Articles.objects.get(pageidEs=asigned[0])
                if article_error.problemCopper:
                    if error_asigned not in article_error.problemCopper:
                        article_error.problemCopper = f'{article_error.problemCopper} \n{error_asigned}'
                else:
                    article_error.problemCopper = error_asigned
                article_error.save()

        for reviewedCopper in reviewedCopper_list:
            if tuple(reviewedCopper) not in articles_reviewed_list:
                try:
                    article_error = Articles.objects.get(pageidEs=reviewedCopper[0])
                    if article_error.problemCopper:
                        if error_translated_page not in  article_error.problemCopper:
                            article_error.problemCopper = f'{article_error.problemCopper} \n{error_translated_page}'
                    else:
                        article_error.problemCopper = error_translated_page
                    article_error.save()

                except ObjectDoesNotExist as e:
                    error_list.append((inprogress[1], 'Tiene un Translated page'))

        for reviewed in articles_reviewed_list:
            if list(reviewed) not in reviewedCopper_list:
                article_error = Articles.objects.get(pageidEs=reviewed[0])

                if article_error.problemCopper:
                    if error_reviewed not in article_error.problemCopper:
                        article_error.problemCopper = f'{article_error.problemCopper} \n{error_reviewed}'
                else:
                    article_error.problemCopper = error_reviewed
                article_error.save()

        error_qs = Articles.objects.exclude(Q(problemCopper='')|Q(problemCopper=None))

        return error_qs, error_list
    def get_coppermind_values(self):
        inprogress = self.get_inprogress()
        translatedpage = self.get_translatedpage()
        return inprogress, translatedpage

    def get_inprogress(self):
        template = "24207"  # In-progress Template
        inprogress_list = self.get_template_list(template)

        return inprogress_list

    def get_template_list(self, template):

        url = 'https://es.coppermind.net/w/api.php'
        params = {
            "action": "query",  #action type
            "format": "json",  #output type
            "prop": "transcludedin",  #what is included in template
            "pageids": template,
            "tilimit": "max"
        }

        template_list = []
        response_info = self.conect_to_coppermind(url, params)
        results = response_info["query"]["pages"][template]["transcludedin"]

        for i in range(len(results)):
            template_list.append([results[i]["pageid"], results[i]["title"]])

        try:
            siguiente = response_info["continue"]["ticontinue"]
        except KeyError:
            siguiente = ''

        while siguiente != '':
            params["ticontinue"] = siguiente
            response_info = self.conect_to_coppermind(url, params)
            results = response_info["query"]["pages"][template]["transcludedin"]
            for i in range(len(results)):
                template_list.append([results[i]["pageid"], results[i]["title"]])
            try:
                siguiente = response_info["continue"]["ticontinue"]
            except KeyError:
                siguiente = ''

        return template_list

    def get_translatedpage(self):
        template = "23774"  # Translatedpage template
        translatedpage_list = self.get_template_list(template)

        return translatedpage_list

class DatabaseManager:

    @staticmethod
    def get_num_articles(queryset):
        return queryset.count()

    @staticmethod
    def get_qs_articles_all():
        return Articles.objects.all().filter(priority__in=PRIORITY_OPTIONS). \
            exclude(Q(type__in=EXCLUDED_TYPE) | Q(universe__in=EXCLUDED_UNIVERSES))

    @staticmethod
    def get_qs_articles_translate():
        return Articles.objects.filter(
            translated=True, priority__in=PRIORITY_OPTIONS
        ).exclude(Q(type__in=EXCLUDED_TYPE) | Q(universe__in=EXCLUDED_UNIVERSES))

    @staticmethod
    def get_qs_articles_reviewed():
        return Articles.objects.filter(
            reviewed=True, priority__in=PRIORITY_OPTIONS
        ).exclude(Q(type__in=EXCLUDED_TYPE) | Q(universe__in=EXCLUDED_UNIVERSES))

    @staticmethod
    def get_qs_articles_assigned():
        return Articles.objects.filter(
            translator__isnull=False, priority__in=PRIORITY_OPTIONS
        ).exclude(Q(type__in=EXCLUDED_TYPE) | Q(universe__in=EXCLUDED_UNIVERSES))

    @staticmethod
    def get_qs_articles_assigned_not_reviewed():
        return Articles.objects.filter(
            translator__isnull=False, priority__in=PRIORITY_OPTIONS, reviewed=False
        ).exclude(Q(type__in=EXCLUDED_TYPE) | Q(universe__in=EXCLUDED_UNIVERSES))

    @staticmethod
    def get_qs_articles_not_translated():
        return Articles.objects.filter(priority__in=PRIORITY_OPTIONS, translated=False).exclude(
            Q(type__in=EXCLUDED_TYPE) | Q(universe__in=EXCLUDED_UNIVERSES)
        )

class HomeManager:

    UNIVERSE_CHART_LEGEND_RENAME = {'num_translated':'Traducidos y no revisados',
                                    'num_reviewed': 'Traducidos y revisados',
                                    'num_not_translated':'No traducidos'}

    UNIVERSE_COLOR_DICT = {'Traducidos y no revisados': '#fe9600',
                           'Traducidos y revisados': '#9f5e00',
                           'No traducidos': '#d3d3d3'}



    @staticmethod
    def obtain_progress(denominador, nominador):
        return round(nominador/denominador*100)

    def get_universes_chart(self):

        qs_translated = DatabaseManager.get_qs_articles_translate().values('universe').annotate(num_translated=Count('titleEs'))

        qs_reviewed= DatabaseManager.get_qs_articles_reviewed().values('universe').annotate(num_reviewed=Count('titleEs'))

        qs_sintraducir = DatabaseManager.get_qs_articles_not_translated().values('universe').annotate(num_not_translated=Count('titleEs'))

        list_universes = Universe.objects.values_list('universe', flat=True)

        empty_dataframe_translated = {'universe': list_universes,
                                     'num_translated': [0] * len(list_universes)}
        empty_dataframe_reviewed = {'universe': list_universes,
                                    'num_reviewed': [0] * len(list_universes)}
        empty_dataframe_not_translated = {'universe':list_universes,
                                       'num_not_translated': [0] * len(list_universes)}

        df_translated = pd.DataFrame.from_records(qs_translated) if qs_translated else pd.DataFrame(
            data=empty_dataframe_translated)
        df_reviewed = pd.DataFrame.from_records(qs_reviewed) if qs_reviewed else pd.DataFrame(data=empty_dataframe_reviewed)
        df_not_translated = pd.DataFrame.from_records(qs_sintraducir) if qs_sintraducir else pd.DataFrame(
            data=empty_dataframe_not_translated)

        df_final = df_translated.merge(df_reviewed, on='universe', how='outer').merge(df_not_translated, on='universe', how='outer')
        df_final = df_final.fillna(0).sort_values('universe')
        df_final['num_translated'] = df_final['num_translated'].astype(int)
        df_final['num_reviewed'] = df_final['num_reviewed'].astype(int)
        df_final['num_not_translated'] = df_final['num_not_translated'].astype(int)
        df_final['num_translated'] = df_final['num_translated'] - df_final['num_reviewed']
        df_final['num_total'] = df_final['num_translated'] + df_final['num_reviewed'] + df_final['num_not_translated']
        df_final = df_final.sort_values('num_total', ascending=False).reset_index(drop=True)

        df_final = df_final[['universe', 'num_reviewed', 'num_translated', 'num_not_translated']].rename(
            columns=self.UNIVERSE_CHART_LEGEND_RENAME)

        df_final['universe']= df_final['universe'].astype('str')

        for i in df_final.index:
            index_universe= df_final.loc[i, 'universe']
            universe_name = Universe.objects.get(pk=index_universe).universe
            df_final.loc[i,'universe'] = universe_name

        df_final_melted = pd.melt(df_final, id_vars=['universe'], var_name='type')
        fig = px.bar(df_final_melted, x='value', y='universe', color='type', orientation='h',
                     color_discrete_map=self.UNIVERSE_COLOR_DICT)


        layout = {

            'xaxis_title': '<b>Universo</b>',
            'yaxis':{
                'type': 'category',
                'dtick': 1
            },
            'barmode': 'stack',
            'title': {
                'text': '<b>ARTÍCULOS POR UNIVERSO</b>',
                'font_family': 'Open Sans, sans-serif',
                'font_color': '#FFFFFF',
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            'font_family': 'Open Sans, sans-serif',
            'font_color': '#FFFFFF',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
        }
        return plot({'data': fig.data, 'layout': layout}, output_type='div')

    def get_month_chart(self):

        qs_translated_month = DatabaseManager.get_qs_articles_translate().values('translatedDate').annotate(
            num_translated=Count('translatedDate')
        )
        qs_revisado_mes = DatabaseManager.get_qs_articles_reviewed().values('reviewedDate').annotate(
            num_reviewed=Count('reviewedDate')
        )

        df_translated = pd.DataFrame.from_records(qs_translated_month)
        df_translated = df_translated[df_translated.translatedDate.notnull()]
        df_translated['yyyy-mm'] = pd.to_datetime(df_translated['translatedDate']).dt.strftime('%Y-%m')
        df_translated_pivot = pd.pivot_table(df_translated, values='num_translated', index=['yyyy-mm'], aggfunc="sum")

        df_reviewed = pd.DataFrame.from_records(qs_revisado_mes)
        df_reviewed = df_reviewed[df_reviewed.reviewedDate.notnull()]
        df_reviewed['yyyy-mm'] = pd.to_datetime(df_reviewed['reviewedDate']).dt.strftime('%Y-%m')
        df_reviewed_pivot = pd.pivot_table(df_reviewed, values='num_reviewed', index=['yyyy-mm'], aggfunc="sum")

        df_final = df_translated_pivot.merge(df_reviewed_pivot, left_index=True, right_index=True, how='outer')
        df_final = df_final.fillna(0)

        df_reduced = df_final.tail(12)

        x_values = [d.strftime('%B-%Y') for d in pd.to_datetime(df_reduced.index)]

        graphs = [go.Bar(y=df_reduced['num_translated'], x=x_values, name='Traducido', marker_color='#fe9600'),
                 go.Scatter(y=df_reduced['num_reviewed'], x=x_values, name='Revisado', marker_color='#d3d3d3',
                            line={'width': 3})]

        layout = {
            'title': {
                'text': '<b>ARTÍCULOS TRADUCIDOS POR MES</b>',
                'font_family': 'Open Sans, sans-serif',
                'font_color': '#FFFFFF',
                # 'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            'font_family': 'Open Sans, sans-serif',
            'font_color': '#FFFFFF',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'barmode': 'group',
        }

        return plot({'data': graphs, 'layout': layout},  output_type='div')

class ReviewBaseManager(ABC):
    def assign_article_to_user(self, universe, userid):
        raise NotImplementedError('Método no implementado')

    def get_assigned_articles_for_user(userid):
        raise NotImplementedError('Método no implementado')

    def get_list_next_article_to_assign(self,universes, userid):
        non_assigned_articles = []
        for universe_item in universes.all():
            article = self.get_next_article_to_assign(universe_item, userid)
            if article:
                non_assigned_articles.append(article)

        return non_assigned_articles

    @abstractmethod
    def get_next_article_to_assign(universe_item, userid):
        raise NotImplementedError('Método no implementado')


class ReReviewManager(ReviewBaseManager):

    def assign_article_to_user(self, universe, userid):
        article_to_assign = self.get_next_article_to_assign(universe, userid)
        Articles.objects.filter(pk=article_to_assign.id).update(gregorio=userid)

    @staticmethod
    def get_assigned_articles_for_user(userid):
        return Articles.objects.filter(engregoriado=False).filter(gregorio=userid)


    @staticmethod
    def get_next_article_to_assign(universe_item, userid):
        article = Articles.objects.filter(
            universe=universe_item, reviewed=True, gregorio__isnull=True, priority__in=PRIORITY_OPTIONS
        ).exclude(type__in=EXCLUDED_TYPE).exclude(reviewer=userid).order_by('priority', 'titleEn').first()

        return article

class ReviewManager(ReviewBaseManager):

    def assign_article_to_user(self, universe, userid, assignedDate):
        article_to_assign = self.get_next_article_to_assign(universe, userid)
        Articles.objects.filter(pk=article_to_assign.id).update(reviewer=userid, reviewerassignedDate=assignedDate)
    @staticmethod
    def get_assigned_articles_for_user(userid):
        return Articles.objects.filter(reviewed=False).filter(reviewer=userid)

    @staticmethod
    def get_next_article_to_assign(universe_item, userid):
        article = Articles.objects.filter(
            universe=universe_item, translated=True, reviewed=False, reviewer__isnull=True, priority__in=PRIORITY_OPTIONS
        ).exclude(type__in=EXCLUDED_TYPE).exclude(translator=userid).order_by('priority', 'titleEn').first()

        return article

class TranslateManager:

    def assign_article_to_user(self, universe, userid, assignedDate):
        article_to_assign = self.get_next_article_to_assign(universe)
        Articles.objects.filter(pk=article_to_assign.id).update(translator=userid, assignedDate=assignedDate)

    @staticmethod
    def get_assigned_articles_for_user(userid):
        return Articles.objects.filter(translated=False).filter(translator=userid)

    def get_list_next_article_to_assign(self,universes):
        non_assigned_articles = []
        for universe_item in universes.all():
            article = self.get_next_article_to_assign(universe_item)
            if article:
                non_assigned_articles.append(article)

        return non_assigned_articles

    @staticmethod
    def get_next_article_to_assign(universe_item):
        article = Articles.objects.filter(
            universe=universe_item, translated=False, translator__isnull=True, priority__in=PRIORITY_OPTIONS
        ).exclude(type__in=EXCLUDED_TYPE).order_by('priority', 'titleEn').first()

        return article
