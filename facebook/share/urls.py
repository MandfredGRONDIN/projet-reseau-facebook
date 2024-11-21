from django.urls import path
from .views import SharePostView, SharedPostsView

urlpatterns = [
    path('<int:post_id>/', SharePostView.as_view(), name='share_post'),
    path('shared_posts/', SharedPostsView.as_view(), name='shared_posts'),
]
