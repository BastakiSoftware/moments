from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm

User = get_user_model()

# Create your views here.


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})


class SignUpView(CreateView):
    """
    View for user registration
    """

    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign Up"
        return context


class ProfileView(DetailView):
    """
    View for displaying user profile
    """

    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    View for editing user profile
    """

    model = User
    template_name = "accounts/profile_edit.html"
    fields = ["username", "email", "first_name", "last_name"]
    success_url = reverse_lazy("profile_edit")

    def get_object(self, queryset=None):
        return self.request.user
