from django.urls import path
from .views import CommentListView, CommentCreateView

urlpatterns = [
    path('comment/<int:post_id>/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:post_id>/add/', CommentCreateView.as_view(), name='comment_add'),
]
