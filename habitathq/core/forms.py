
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Complaint, Visitor, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')
        
        
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        # Only show the fields a user needs to fill out
        fields = ['title', 'description'] 
        
        
        
class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['full_name', 'contact_number', 'expected_datetime']
        widgets = {
            'expected_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
    'content': forms.Textarea(attrs={
        'rows': 3,
        'placeholder': "What's on your mind?",
        
        'class': 'w-full p-2 border border-gray-300 rounded-md'
    })
        }
        labels = {
            'content': '' # Hide the default "Content" label
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a comment...',
                'class': 'w-full p-2 border rounded-md'
            })
        }
        labels = {
            'content': ''
        }
        
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'date_of_birth', 'phone_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }