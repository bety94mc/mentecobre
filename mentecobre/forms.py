from django import forms

class AssignArticleForm(forms.Form):
    articleUniverseID = forms.IntegerField()

class ProblemArticleForm(forms.Form):
    articleID = forms.IntegerField()

class ReReviewArticleForm(forms.Form):
    articleID = forms.IntegerField()

class ReviewArticleForm(forms.Form):
    articleID = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea, required=False)
    linkcoppperen = forms.BooleanField()

class TranslateArticleForm(forms.Form):
    articleID = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea)



