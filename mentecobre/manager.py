from abc import ABC, abstractmethod

from .models import Articles

EXCLUDED_TYPE = ['RD', 'DIS', 'SUB']
PRIORITY_OPTIONS = [1, 2, 3]


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
