from django.db import models
from django.contrib.auth.models import User

class Friendship(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    FRIENDSHIP_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    
    user1 = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=FRIENDSHIP_STATUS_CHOICES,
        default=PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1', 'user2') 

    def __str__(self):
        return f"{self.user1} - {self.user2} ({self.status})"
