from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import CustomerUserModel
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

User = get_user_model()  # This gets your CustomerUserModel


# User Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomerUserModel.objects.get(username=response.data["username"])
        token = Token.objects.get(user=user)
        return Response(
            {"user": response.data, "token": token.key}, status=status.HTTP_201_CREATED
        )


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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing user profiles and managing follows.
    Provides `list` and `retrieve` actions by default.
    """

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="follow")
    def follow(self, request, pk=None):
        """
        Action for the logged-in user to follow another user.
        """
        user_to_follow = self.get_object()
        current_user = request.user

        if user_to_follow == current_user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_user.following.add(user_to_follow)
        return Response(
            {"status": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        """
        Action for the logged-in user to unfollow another user.
        """
        user_to_unfollow = self.get_object()
        current_user = request.user

        current_user.following.remove(user_to_unfollow)
        return Response(
            {"status": f"You have unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK,
        )
