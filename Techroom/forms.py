from django import forms
from django.forms import ModelForm
from .models import Room, User


# ------------------------------
# RoomForm
# ------------------------------
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']
        exclude = ['host', 'participants']


# ------------------------------
# CustomUserForm (for registration)
# ------------------------------
class CustomUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Secure hashing

        if commit:
            user.save()
        return user


# ------------------------------
# UserForm (for updating profile)
# ------------------------------
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Hash updated password

        if commit:
            user.save()
        return user
