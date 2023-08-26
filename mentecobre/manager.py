from .models import Articles

EXCLUDED_TYPE = ['RD', 'DIS', 'SUB']
PRIORITY_OPTIONS = [1, 2, 3]



class TranslateManager:

    @staticmethod
    def assigned_articles_for_user(userid):

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
        print('universe_item is', universe_item)
        article = Articles.objects.filter(
            universe=universe_item, translated=False, translator__isnull=True, priority__in=PRIORITY_OPTIONS
        ).exclude(type__in=EXCLUDED_TYPE).order_by('priority', 'titleEn').first()

        return article


    def assign_article_to_user(self, universe, userid, assignedDate):
        print('universe is', universe)
        articulo_asignar = self.get_next_article_to_assign(universe)
        Articles.objects.filter(pk=articulo_asignar.id).update(translator=userid, assignedDate=assignedDate)