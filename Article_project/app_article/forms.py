from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = ('topic', 'title', 'data')

class EditProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name')
        help_texts = {
            'username': None,
        }

class commentForm(forms.ModelForm):
    class Meta:
        model=comment
        fields=['name','email','body']