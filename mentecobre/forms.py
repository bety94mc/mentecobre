from django import forms

class TranslateArticleForm(forms.Form):
    articleID = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea)

class AssignArticleForm(forms.Form):
    articleUniverseID = forms.IntegerField()