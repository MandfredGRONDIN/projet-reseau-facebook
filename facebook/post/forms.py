from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'media_url'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Qu\'est-ce qui vous passe par la tête ?'}),
        }
        labels = {
            'content': '', 
            'media_url': 'URL du média', 
        }
