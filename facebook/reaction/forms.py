from django import forms
from .models import Reaction

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['type']

    type = forms.ChoiceField(choices=Reaction.REACTION_CHOICES, widget=forms.RadioSelect)
