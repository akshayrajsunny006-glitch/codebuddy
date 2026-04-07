from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, UserProfile


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your@email.com',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'autocomplete': 'current-password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'age', 'gender', 'college_name', 'year_of_study', 'skills', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your@email.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '20'}),
            'gender': forms.Select(attrs={'class': 'form-input'}),
            'college_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'MIT, Stanford...'}),
            'year_of_study': forms.Select(attrs={'class': 'form-input'}),
            'skills': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, React, ML...'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'bio', 'skills', 'college_name', 'year_of_study', 'available_now', 'preferred_roles', 'profile_photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'skills': forms.TextInput(attrs={'class': 'form-input'}),
            'college_name': forms.TextInput(attrs={'class': 'form-input'}),
            'year_of_study': forms.Select(attrs={'class': 'form-input'}),
            'available_now': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }

    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    linkedin = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    github = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    certificates = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 2}))
