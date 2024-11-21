from django.urls import path
from .views import StoryListView, CreateStoryView, StoryDetailView

urlpatterns = [
    path('', StoryListView.as_view(), name='story_list'),
    path('create/', CreateStoryView.as_view(), name='create_story'),
    path('<int:pk>/', StoryDetailView.as_view(), name='view_story'),
]
