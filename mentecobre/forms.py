from django import forms

class AssignArticleForm(forms.Form):
    articleUniverseID = forms.IntegerField()

class ChangesForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')), label='Fecha inicial')
    end_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')), label='Fecha final')

class GregorioForm(forms.Form):
    username = forms.CharField(required=True)
    status = forms.CharField(required=True)

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


