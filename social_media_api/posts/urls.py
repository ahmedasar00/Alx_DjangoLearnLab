from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/like/", PostViewSet.as_view({"post": "like"}), name="like-post"),
    path(
        "<int:pk>/unlike/", PostViewSet.as_view({"post": "unlike"}), name="unlike-post"
    ),
]
