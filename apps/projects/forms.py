from django import forms
from .models import Project, JoinRequest, ProjectTask


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'teaser', 'description', 'full_description',
            'required_skills', 'max_team_size', 'deadline',
            'difficulty', 'privacy_level', 'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Amazing Project Name'}),
            'teaser': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'One-line pitch...'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'What is this project about?'}),
            'full_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'Detailed project description...'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, React, ML...'}),
            'max_team_size': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 20}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'difficulty': forms.Select(attrs={'class': 'form-input'}),
            'privacy_level': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }


class JoinRequestForm(forms.ModelForm):
    class Meta:
        model = JoinRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Tell us why you want to join and what you bring to the team...'
            })
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ['title', 'description', 'status', 'assignee']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'assignee': forms.Select(attrs={'class': 'form-input'}),
        }
