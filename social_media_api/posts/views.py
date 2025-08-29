from rest_framework import viewsets, permissions, status, generics
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
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        """
        This view returns a list of posts for the currently authenticated
        user's feed (posts from followed users and their own posts).
        For detail views, it allows access to any post, with permissions
        handled by IsOwnerOrReadOnly.
        """
        user = self.request.user

        if not user.is_authenticated:
            return Post.objects.none()

        if self.action == "list":  # the process list, create, retrieve
            following_users = user.following.all()
            # A user's feed should contain posts from followed users and their own posts.
            return Post.objects.filter(Q(author__in=following_users) | Q(author=user))
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)

        user = request.user

        if post.author == user:
            return Response(
                {"error": "You cannot like your own post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # If like does not exist, create it and a notification
            Notification.objects.create(
                recipient=post.author, actor=user, verb="liked your post", target=post
            )
            return Response({"status": "Post liked"}, status=status.HTTP_201_CREATED)
        else:
            # If like exists, unlike the post and remove notification
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned comments to a given post,
        by filtering against a `post` query parameter in the URL.
        """
        queryset = Comment.objects.all().order_by("-created_at")
        post_id = self.request.query_params.get("post")
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
