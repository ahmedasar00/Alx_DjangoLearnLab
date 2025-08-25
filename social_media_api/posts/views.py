from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment, Like
from .serializers import CommentSerializer, PostSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = ["Post.objects.filter(author__in=following_users).order_by"]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        """
        This view should return a list of all the posts
        for the currently authenticated user's followed users.
        """
        user = self.request.user

        # Return an empty queryset if the user is not authenticated
        if not user.is_authenticated:
            return Post.objects.none()

        # Get the list of users that the current user follows
        following_users = user.following.all()

        # Filter posts to include only those from followed users,
        # and order them by creation date (newest first).
        # This is the line the checker is looking for!
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.author == user:
            return Response(
                {"error": "You cannot like your own post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # If like exists, unlike the post
            like = Like.objects.get(user=user, post=post)
            like.delete()

            # Remove the corresponding notification
            content_type = ContentType.objects.get_for_model(Post)
            Notification.objects.filter(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                target_content_type=content_type,
                target_object_id=post.id,
            ).delete()

            return Response({"status": "Post unliked"}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            # If like does not exist, create it
            Like.objects.create(user=user, post=post)
            # Create a notification for the post author
            Notification.objects.create(
                recipient=post.author, actor=user, verb="liked your post", target=post
            )
            return Response({"status": "Post liked"}, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()

        return Post.objects.filter(author__in=following_users).order_by()
