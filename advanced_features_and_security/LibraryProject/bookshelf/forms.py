from django import forms

class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False, )
    