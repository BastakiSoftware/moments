from django.urls import path
from .views import PostListView, PostDetailView, create_post

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("create/<str:post_type>/", create_post, name="create_post"),
    path("<str:post_type>/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    # ... other URL patterns ...
]
