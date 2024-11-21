from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profile.urls')),
    path('', include('authentication.urls')),
    path('', include('post.urls')),
    path('', include('friendship.urls')),
    path('', include('comment.urls')),
    path('', include('reaction.urls')),
    path('', include('share.urls')),
]
