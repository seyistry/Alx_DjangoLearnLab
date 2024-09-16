from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment
from taggit.forms import TagWidget


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
        fields = ['title', 'content', 'post_tags']  # Include 'tags' in the fields
        widgets = {
            'tags': TagWidget(),  # Use TagWidget for the tags field
        }

    def __init__(self, *args, **kwargs):
        # Extract the logged-in user from kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)

        # Set the author if it's a new post and the user is provided
        if self.user and not post.pk:
            post.author = self.user

        if commit:
            post.save()


class CommentForm(forms.ModelForm):  # create and update forms for comments
    class Meta:
        model = Comment
        fields = ['content']
        # Note: The 'author' field should not be included here if we are setting it in the __init__ method

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs and remove it
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        # Set the initial value for the 'author' field to the user
        if self.user:
            self.fields['author'].initial = self.user
