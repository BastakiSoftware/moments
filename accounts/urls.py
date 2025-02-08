from django.urls import path
from .views import SignUpView, ProfileEditView, ProfileView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
]
