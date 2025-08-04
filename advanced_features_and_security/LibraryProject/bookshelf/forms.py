from django import forms
from .forms import ExampleForm
class BookSearchForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=False,
    )

    title = forms.CharField(max_length=200, required=False)

    author = forms.CharField(max_length=100, required=False)
