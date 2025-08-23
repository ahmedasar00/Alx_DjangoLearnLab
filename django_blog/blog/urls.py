from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    # Post URLs
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    # Comment URLs
    path(
        "post/<int:post_pk>/comments/",
        views.CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "post/<int:pk>/comments/new/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:pk>/update/",
        views.CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    #! Added new URL patterns for tag filtering and search results
    path(
        "tags/<slug:tag_slug>/", views.PostListByTag.as_view(), name="post-list-by-tag"
    ),
    path("search/", views.SearchView.as_view(), name="search-results"),
]
