from django.urls import path
from .views import AddReactionView

urlpatterns = [
    path('react/post/<int:post_id>/', AddReactionView.as_view(), name='add_reaction'),
]