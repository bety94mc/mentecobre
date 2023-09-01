from django import forms

class TranslateArticleForm(forms.Form):
    articleID = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea)

class AssignArticleForm(forms.Form):
    articleUniverseID = forms.IntegerField()

class ReviewArticleForm(forms.Form):
    articleID = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea, required=False)
    linkcoppperen = forms.BooleanField()
