from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Room, Team

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': 'Расскажите о себе...'
            }),
        }

class OptionalPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    def clean(self):
        old = self.cleaned_data.get("old_password")
        new1 = self.cleaned_data.get("new_password1")
        new2 = self.cleaned_data.get("new_password2")

        if not old and not new1 and not new2:
            self._errors.clear()
            return self.cleaned_data

        return super().clean()

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
