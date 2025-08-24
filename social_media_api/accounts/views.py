from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomerUserModel
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.decorators import action
from notifications.models import Notification


# User Registration
class RegisterView(generics.CreateAPIView):
    queryset = CustomerUserModel.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


# User Login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


# User Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing user profiles and managing follows.
    Provides `list` and `retrieve` actions by default.
    """

    queryset = CustomerUserModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="follow")
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        current_user = request.user

        if user_to_follow == current_user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_user.following.add(user_to_follow)

        Notification.objects.create(
            recipient=user_to_follow, actor=current_user, verb="started following you"
        )

        return Response(
            {"status": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        current_user = request.user

        current_user.following.remove(user_to_unfollow)
        return Response(
            {"status": f"You have unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK,
        )
