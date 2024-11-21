from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Story(models.Model):
    media_url = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    expiration_date = models.DateTimeField()  
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"Story de {self.user.username} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']
