from django import forms
from .models import Story
from django.forms.widgets import DateTimeInput

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['media_url', 'expiration_date']
        widgets = {
            'expiration_date': DateTimeInput(attrs={'type': 'datetime-local'})
        }
