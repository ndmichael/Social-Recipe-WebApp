from django import forms
from .models import Post

class PostSearchForm (forms.Form):
    search = forms.CharField ();