# accounts/urls.py

from django.urls import path
from .views import UserViewSet

user_list = UserViewSet.as_view({"get": "list"})
user_detail = UserViewSet.as_view({"get": "retrieve"})
user_follow = UserViewSet.as_view({"post": "follow"})
user_unfollow = UserViewSet.as_view({"post": "unfollow"})


urlpatterns = [
    path("users/", user_list, name="user-list"),
    path("users/<int:user_id>/", user_detail, name="user-detail"),
    path("follow/<int:user_id>/", user_follow, name="user-follow"),
    path("unfollow/<int:user_id>/", user_unfollow, name="user-unfollow"),
]
