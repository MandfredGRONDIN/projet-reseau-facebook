from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    content = models.TextField("Content", max_length=1000) 
    media_url = models.CharField("Media URL", max_length=255, blank=True, null=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') 
    created_at = models.DateTimeField("Created At", auto_now_add=True)  
    updated_at = models.DateTimeField("Updated At", auto_now=True) 

    def __str__(self):
        return f"Post by {self.user.username} - {self.content[:20]}"  

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"] 
