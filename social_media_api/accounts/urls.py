# accounts/urls.py

from django.urls import path
from .views import UserViewSet

# Manually define view actions
user_list = UserViewSet.as_view({"get": "list"})
user_detail = UserViewSet.as_view({"get": "retrieve"})
user_follow = UserViewSet.as_view({"post": "follow"})
user_unfollow = UserViewSet.as_view({"post": "unfollow"})

urlpatterns = [
    path("users/", user_list, name="user-list"),
    # Use <int:user_id> to match the checker and the updated ViewSet
    path("users/<int:user_id>/", user_detail, name="user-detail"),
    path("users/<int:user_id>/follow/", user_follow, name="user-follow"),
    path("users/<int:user_id>/unfollow/", user_unfollow, name="user-unfollow"),
]
