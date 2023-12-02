from django import forms
from .models import PostComments

class CommentPostForm(forms.ModelForm):


    class Meta:
        model = PostComments
        fields = ['comment']

class SearchForm(forms.Form):
    query = forms.CharField()