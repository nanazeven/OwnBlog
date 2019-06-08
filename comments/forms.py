from django import forms
from .models import Comment


class CommentsForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['text']
