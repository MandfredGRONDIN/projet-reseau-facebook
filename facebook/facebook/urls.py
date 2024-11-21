from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profile.urls')),
    path('', include('authentication.urls')),
    path('post/', include('post.urls')),
    path('friendship/', include('friendship.urls')),
    path('comment/', include('comment.urls')),
    path('reaction/', include('reaction.urls')),
    path('share/', include('share.urls')),
    path('story/', include('story.urls')),
]
