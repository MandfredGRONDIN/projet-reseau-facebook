from django.urls import path
from .views import UserSearchView, SendFriendRequestView, RespondToFriendRequestView

urlpatterns = [
    path('search/', UserSearchView.as_view(), name='search_users'),
    path('friend-request/send/<int:pk>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/<int:pk>/<str:action>/', RespondToFriendRequestView.as_view(), name='respond_to_friend_request'),
]
