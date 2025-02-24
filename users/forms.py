from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from tasks.models import Profile
from users.models import CustomUser
from users.services import check_image_size


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not check_image_size(image):
                raise forms.ValidationError(f"Размер изображения превышает 1024 КБ")
        return image