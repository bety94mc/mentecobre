from abc import ABC, abstractmethod
from datetime import date, timedelta, datetime

from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import requests

from .models import Articles
from login_app.models import Universe, CustomUser

EXCLUDED_TYPE = ['RD', 'DIS', 'SUB']
EXCLUDED_UNIVERSES = [13]
PRIORITY_OPTIONS = [1, 2, 3]


class CoppermindManager:
    SECTION_TRANSLATE = {
        'Principal': '0',
        'Coppermind': '4',
        'Resumen': '3000',
        'Categorías': '14',
        'Plantillas': '10'
    }

    @staticmethod
    def conect_to_coppermind(url, params):
        response = requests.Session().get(url=url, params=params)
        return response.json()

    @staticmethod
    def get_moved_articles(changes_df):
        all_articles = Articles.objects.all()
        all_articles_df = pd.DataFrame(list(all_articles.values('pageidEn', 'titleEn', 'titleEs')))

        changes_df_with_all_articles = pd.merge(changes_df, all_articles_df, 'left', left_on='PageID',
                                                right_on='pageidEn')

        articles_with_changes = changes_df_with_all_articles[changes_df_with_all_articles['pageidEn'].notnull()]

        articles_moved_full = articles_with_changes.loc[
            articles_with_changes.Page_tittle != articles_with_changes.titleEn]

        articles_moved = articles_moved_full[['PageID', 'Page_tittle', 'titleEn']].drop_duplicates()

        return articles_moved

    @staticmethod
    def get_new_articles(changes_df):
        all_articles = Articles.objects.all()
        all_articles_df = pd.DataFrame(list(all_articles.values('pageidEn', 'titleEn', 'titleEs')))

        changes_df_with_all_articles = pd.merge(changes_df, all_articles_df, 'left', left_on='PageID',
                                                right_on='pageidEn')

        new_articles_full = changes_df_with_all_articles[changes_df_with_all_articles['pageidEn'].isnull()]
        new_articles = new_articles_full[['PageID', 'Page_tittle', ]].drop_duplicates()

        return new_articles

    @staticmethod
    def get_not_assigned_not_translated_articles(changes_df):
        not_assigned_not_translated_articles = Articles.objects.filter(translator__isnull=True).filter(translated=False)

        not_assigned_not_translated_articles_df = pd.DataFrame(
            list(not_assigned_not_translated_articles.values('pageidEn', 'titleEn', 'titleEs'))
        )

        changes_df_with_not_assigned_not_translated_articles = pd.merge(changes_df,
                                                                        not_assigned_not_translated_articles_df, 'left',
                                                                        left_on='PageID', right_on='pageidEn')

        not_assigned_not_translated_articles_full = changes_df_with_not_assigned_not_translated_articles[
            changes_df_with_not_assigned_not_translated_articles['pageidEn'].notnull()]

        not_assigned_not_translated_articles = not_assigned_not_translated_articles_full[
            ['PageID', 'Page_tittle', 'titleEs']].drop_duplicates()

        return not_assigned_not_translated_articles

    @staticmethod
    def get_translated_articles(changes_df):
        assigned_articles = Articles.objects.filter(translator__isnull=False)
        assigned_articles_df = pd.DataFrame(list(assigned_articles.values('pageidEn', 'titleEn', 'titleEs')))

        changes_df_with_assigned_articles = pd.merge(changes_df, assigned_articles_df, 'left', left_on='PageID',
                                                     right_on='pageidEn')
        assigned_articles_full = changes_df_with_assigned_articles[
            changes_df_with_assigned_articles['pageidEn'].notnull()]

        translated_articles_wot = Articles.objects.filter(translator__isnull=True).filter(translated=True)
        translated_articles_wot_df = pd.DataFrame(
            list(translated_articles_wot.values('pageidEn', 'titleEn', 'titleEs')))

        changes_df_with_translated_articles_wot = pd.merge(changes_df, translated_articles_wot_df, 'left',
                                                           left_on='PageID',
                                                           right_on='pageidEn')
        translated_articles_wot_full = changes_df_with_translated_articles_wot[
            changes_df_with_translated_articles_wot['pageidEn'].notnull()]

        translated_articles_full = pd.concat([assigned_articles_full, translated_articles_wot_full])
        translated_articles = translated_articles_full[['PageID', 'Page_tittle', 'titleEs']].drop_duplicates()

        return translated_articles

    @staticmethod
    def turn_date_to_str(datetime_object: date) -> str:
        datetime_str = datetime_object.strftime('%Y-%m-%d')
        return datetime_str

    def assigned_and_reviewed_cross_check(self, inprogress_list, assigned_list, reviewedCopper_list,
                                          articles_reviewed_list):
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
                        if error_translated_page not in article_error.problemCopper:
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

        error_qs = Articles.objects.exclude(Q(problemCopper='') | Q(problemCopper=None))

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
            "action": "query",  # action type
            "format": "json",  # output type
            "prop": "transcludedin",  # what is included in template
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

    def get_articles(self, language):
        pages_df = pd.DataFrame(columns=['PageID', 'Title', 'URL'])
        if language == 'en':
            url = 'https://coppermind.net/w/api.php'
        else:
            url = 'https://es.coppermind.net/w/api.php'

        for section in self.SECTION_TRANSLATE.values():
            new_pages_df = self.get_articles_list(url, section)
            pages_df = pd.concat([pages_df, new_pages_df])

        return pages_df

    def get_articles_list(self, url, section):

        params = {
            "action": "query",
            "format": "json",
            "prop": "info",
            "generator": "allpages",
            "inprop": "url",
            "gapnamespace": section,
            "gaplimit": "max"
        }

        response_info = self.conect_to_coppermind(url, params)
        allpageslist = []

        for id in response_info['query']['pages']:
            allpageslist.append([id, response_info['query']['pages'][id]['title'],
                                 response_info['query']['pages'][id]['fullurl']])

        try:
            next_one = response_info['continue']['gapcontinue']  # 501 value
        except KeyError:
            next_one = ''

        while next_one != "":

            params['gapcontinue'] = next_one
            response_info = self.conect_to_coppermind(url, params)

            for page_id in response_info['query']['pages']:
                allpageslist.append([page_id, response_info['query']['pages'][page_id]['title'],
                                     response_info['query']['pages'][page_id]['fullurl']])

            try:
                next_one = response_info['continue']['gapcontinue']
            except KeyError as err:
                next_one = ''

        pages_df = pd.DataFrame(data=allpageslist, columns=['PageID', 'Title', 'URL'])

        return pages_df

    def get_changes(self, dates_list):
        changes_df = pd.DataFrame(columns=['PageID', 'Page_tittle', 'Page_Revision_ID', 'Change_ID',
                                           'Change_Date', 'Change_type', 'Edited_by'])
        reviewers_list = list(CustomUser.objects.filter(groups__name__in=['Revisores']).values_list('copper_username',
                                                                                                    flat=True).distinct())

        for date_block in dates_list:
            for section in self.SECTION_TRANSLATE.values():
                for minor in ['!minor', 'minor']:
                    new_changes_df = self.get_changes_list(date_block[0], date_block[1], section, minor)
                    changes_df = pd.concat([changes_df, new_changes_df])

        changes_df = changes_df[~changes_df.Edited_by.isin(reviewers_list)]

        return changes_df

    def get_changes_list(self, start_date, end_date, section, minor):

        url = 'https://coppermind.net/w/api.php'
        params = {
            "action": "query",  # action type
            "format": "json",  # output format
            "list": "recentchanges",  # get recent changes
            "rcstart": end_date + "T00:00:00.000Z",  # start_date (most recent value)
            "rcend": start_date + "T00:00:00.000Z",  # end_date (oldest value)
            "rcdir": "older",  # get changes from older to newer
            # namespaces: Principal (0), Coppermind(4), Summary(3000), Categories(14), Templates(10)
            "rcnamespace": section,
            "rcprop": "title|timestamp|ids|user",  # data info to obtain
            "rcshow": minor,
            "rclimit": "max",
            "rctype": "edit|new|log|categorize",  # change type
        }
        response_info = self.conect_to_coppermind(url, params)

        changeslist = []

        for query_info in response_info['query']['recentchanges']:
            try:
                changeslist.append([query_info['pageid'], query_info['title'], query_info['revid'], query_info['rcid'],
                                    query_info['timestamp'], query_info['type'], query_info['user']])

            except KeyError as err:
                query_info[
                    err.args[0]] = ''  # If there is one of fields not present in the query, it is added as empty field
                changeslist.append([query_info['pageid'], query_info['title'], query_info['revid'], query_info['rcid'],
                                    query_info['timestamp'], query_info['type'], query_info['user']])

        try:
            next_one = response_info['continue']['rccontinue']
        except KeyError:
            next_one = ''
        while next_one != "":  # siempre que esté relleno el next_one, iteramos
            params = {
                "action": "query",  # action type
                "format": "json",  # output format
                "list": "recentchanges",  # get recent changes
                "rcstart": end_date + "T00:00:00.000Z",  # start_date (most recent value)
                "rcend": start_date + "T00:00:00.000Z",  # end_date (oldest value)
                "rcdir": "older",  # get changes from older to newer
                # namespaces: Principal (0), Coppermind(4), Summary(3000), Categories(14), Templates(10)
                "rcnamespace": section,
                "rcprop": "title|timestamp|ids|user",  # data info to obtain
                "rcshow": minor,
                "rclimit": "max",
                "rctype": "edit|new|log|categorize",  # change type
                "rccontinue": next_one,  # por si hay más de 500 cambios en el mismo periodo
            }

            response_info = self.conect_to_coppermind(url, params)

            for query_info in response_info['query']['recentchanges']:
                try:
                    changeslist.append(
                        [query_info['pageid'], query_info['title'], query_info['revid'], query_info['rcid'],
                         query_info['timestamp'], query_info['type'], query_info['user']])

                except KeyError as err:
                    query_info[err.args[
                        0]] = ''  # If there is one of fields not present in the query, it is added as empty field
                    changeslist.append(
                        [query_info['pageid'], query_info['title'], query_info['revid'], query_info['rcid'],
                         query_info['timestamp'], query_info['type'], query_info['user']])
            try:
                next_one = response_info['continue']['rccontinue']
            except KeyError as err:
                next_one = ''

        changeslist_df = pd.DataFrame(data=changeslist,
                                      columns=['PageID', 'Page_tittle', 'Page_Revision_ID', 'Change_ID',
                                               'Change_Date', 'Change_type', 'Edited_by'])
        return changeslist_df

    def get_user_last_contributor(self, username):
        url = 'https://es.coppermind.net/w/api.php'
        params = {
            "action": "query",  # action type
            "format": "json",  # output format
            "list": "usercontribs",  # get user contributions
            "uclimit": "1",  # limit to last contribution
            "ucuser": username,  # username to check
            "ucprop": "timestamp",  # interested in just the time of the edition
        }
        response_info = self.conect_to_coppermind(url, params)
        timestamp = response_info['query']['usercontribs'][0]['timestamp']

        date_format = '%Y-%m-%dT%H:%M:%SZ'

        date_obj = datetime.strptime(timestamp, date_format)

        return date_obj

    def split_period_in_weeks(self, start_date: date, end_date: date) -> list:

        dates_list = []
        interim_date_1 = start_date
        interim_date_2 = interim_date_1 + timedelta(days=7)
        while interim_date_2 < end_date:
            interim_date_1_str = self.turn_date_to_str(interim_date_1)
            interim_date_2_str = self.turn_date_to_str(interim_date_2)
            dates_list.append([interim_date_1_str, interim_date_2_str])
            interim_date_1 = interim_date_2
            interim_date_2 = interim_date_1 + timedelta(days=7)
        dates_list.append([self.turn_date_to_str(interim_date_1), self.turn_date_to_str(end_date)])

        return dates_list


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

    @staticmethod
    def get_qs_articules_assigned_to_user(userid, type_user):
        qs = None
        if type_user == 'Translator':
            qs = Articles.objects.filter(
                translator=userid, priority__in=PRIORITY_OPTIONS
            ).exclude(type__in=EXCLUDED_TYPE).order_by('-assignedDate')
        if type_user == 'Reviewer':
            qs = Articles.objects.filter(
                reviewer=userid, priority__in=PRIORITY_OPTIONS
            ).exclude(type__in=EXCLUDED_TYPE).order_by('-reviewerassignedDate')

        return qs

    @staticmethod
    def get_qs_articules_assigned_to_user_finished(userid, type_user):
        qs = None
        if type_user == 'Translator':
            qs = Articles.objects.filter(
                translator=userid, priority__in=PRIORITY_OPTIONS, translated=True
            ).exclude(type__in=EXCLUDED_TYPE).order_by('-assignedDate')
        if type_user == 'Reviewer':
            qs = Articles.objects.filter(
                reviewer=userid, priority__in=PRIORITY_OPTIONS, reviewed=True
            ).exclude(type__in=EXCLUDED_TYPE).order_by('-reviewerassignedDate')

        return qs


class GregorioManager:

    def get_users_list(self):
        users_list = []
        last_month = datetime.today() - timedelta(days=30)

        users = CustomUser.objects.filter(Q(is_active=True) | Q(is_resting=True)).order_by('username')
        for user in users:
            user_dict = {'username': user.username, 'last_movement': '', 'status': '', 'color': 'black'}
            if user.is_active and user.copper_username:
                user_dict['status'] = 'active'
                last_movement = CoppermindManager().get_user_last_contributor(user.copper_username)
                if last_month > last_movement:
                    user_dict['color'] = 'red'
                user_dict['last_movement'] = last_movement

            else:
                user_dict['status'] = 'resting'
                user_dict['last_movement'] = user.timeoff_date

            users_list.append(user_dict)

        return users_list


class HomeManager:
    UNIVERSE_CHART_LEGEND_RENAME = {'num_translated': 'Traducidos y no revisados',
                                    'num_reviewed': 'Traducidos y revisados',
                                    'num_not_translated': 'No traducidos'}

    UNIVERSE_COLOR_DICT = {'Traducidos y no revisados': '#fe9600',
                           'Traducidos y revisados': '#9f5e00',
                           'No traducidos': '#d3d3d3'}

    @staticmethod
    def obtain_progress(denominador, nominador):
        return round(nominador / denominador * 100)

    def get_universes_chart(self):
        qs_translated = DatabaseManager.get_qs_articles_translate().values('universe').annotate(
            num_translated=Count('titleEs'))

        qs_reviewed = DatabaseManager.get_qs_articles_reviewed().values('universe').annotate(
            num_reviewed=Count('titleEs'))

        qs_sintraducir = DatabaseManager.get_qs_articles_not_translated().values('universe').annotate(
            num_not_translated=Count('titleEs'))

        list_universes = Universe.objects.values_list('universe', flat=True)

        empty_dataframe_translated = {'universe': list_universes,
                                      'num_translated': [0] * len(list_universes)}
        empty_dataframe_reviewed = {'universe': list_universes,
                                    'num_reviewed': [0] * len(list_universes)}
        empty_dataframe_not_translated = {'universe': list_universes,
                                          'num_not_translated': [0] * len(list_universes)}

        df_translated = pd.DataFrame.from_records(qs_translated) if qs_translated else pd.DataFrame(
            data=empty_dataframe_translated)
        df_reviewed = pd.DataFrame.from_records(qs_reviewed) if qs_reviewed else pd.DataFrame(
            data=empty_dataframe_reviewed)
        df_not_translated = pd.DataFrame.from_records(qs_sintraducir) if qs_sintraducir else pd.DataFrame(
            data=empty_dataframe_not_translated)

        df_final = df_translated.merge(df_reviewed, on='universe', how='outer').merge(df_not_translated, on='universe',
                                                                                      how='outer')
        df_final = df_final.fillna(0).sort_values('universe')
        df_final['num_translated'] = df_final['num_translated'].astype(int)
        df_final['num_reviewed'] = df_final['num_reviewed'].astype(int)
        df_final['num_not_translated'] = df_final['num_not_translated'].astype(int)
        df_final['num_translated'] = df_final['num_translated'] - df_final['num_reviewed']
        df_final['num_total'] = df_final['num_translated'] + df_final['num_reviewed'] + df_final['num_not_translated']
        df_final = df_final.sort_values('num_total', ascending=False).reset_index(drop=True)

        df_final = df_final[['universe', 'num_reviewed', 'num_translated', 'num_not_translated']].rename(
            columns=self.UNIVERSE_CHART_LEGEND_RENAME)

        df_final['universe'] = df_final['universe'].astype('str')

        for i in df_final.index:
            index_universe = df_final.loc[i, 'universe']
            universe_name = Universe.objects.get(pk=index_universe).universe
            df_final.loc[i, 'universe'] = universe_name

        df_final_melted = pd.melt(df_final, id_vars=['universe'], var_name='type')
        fig = px.bar(df_final_melted, x='value', y='universe', color='type', orientation='h',
                     color_discrete_map=self.UNIVERSE_COLOR_DICT)

        layout = {

            'xaxis_title': '<b>Universo</b>',
            'yaxis': {
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

        return plot({'data': graphs, 'layout': layout}, output_type='div')


class ReviewBaseManager(ABC):
    def assign_article_to_user(self, universe, userid):
        raise NotImplementedError('Método no implementado')

    def get_assigned_articles_for_user(userid):
        raise NotImplementedError('Método no implementado')

    def get_list_next_article_to_assign(self, universes, userid):
        non_assigned_articles = []
        for universe_item in universes.all():
            article = self.get_next_article_to_assign(universe_item, userid)
            if article:
                non_assigned_articles.append(article)

        return non_assigned_articles

    @staticmethod
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
            universe=universe_item, translated=True, reviewed=False, reviewer__isnull=True,
            priority__in=PRIORITY_OPTIONS
        ).exclude(type__in=EXCLUDED_TYPE).exclude(translator=userid).order_by('priority', 'titleEn').first()

        return article


class TranslateManager:

    def assign_article_to_user(self, universe, userid, assignedDate):
        article_to_assign = self.get_next_article_to_assign(universe)
        Articles.objects.filter(pk=article_to_assign.id).update(translator=userid, assignedDate=assignedDate)

    @staticmethod
    def get_assigned_articles_for_user(userid):
        return Articles.objects.filter(translated=False).filter(translator=userid)

    def get_list_next_article_to_assign(self, universes):
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
