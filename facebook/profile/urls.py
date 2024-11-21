from django.urls import path
from .views import ProfileView, EditProfileView, DeleteProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)