from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        widgets = {
            "password1": forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            "password2": forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        }
        help_texts = {  # Убираем help_text (эти подсказки с условиями пароля)
            "password1": "",
            "password2": "",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
