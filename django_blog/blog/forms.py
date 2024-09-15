from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        # Note: The 'author' field should not be included here if we are setting it in the __init__ method

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs and remove it
        self.user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        # Set the initial value for the 'author' field to the user
        if self.user:
            self.fields['author'].initial = self.user
