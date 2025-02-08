from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ProfileForm(UserChangeForm):
    # Remove the password field from the form
    password = None

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "birth_date",
            "profile_picture",
            "phone_number",
            "address",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields["email"].required = True
        # Add CSS classes and placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
