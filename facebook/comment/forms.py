from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media_url', 'parent_comment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Écrivez un commentaire...'}),
            'media_url': forms.URLInput(attrs={'placeholder': 'Lien vers un média (facultatif)'}),
        }
