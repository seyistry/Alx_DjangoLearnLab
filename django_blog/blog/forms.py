from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment
from taggit.forms import TagField


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class PostForm(forms.ModelForm):
    # Update the PostForm to include a field for adding or editing tags
    post_tags = TagField(
        required=False, help_text='Enter tags separated by commas')

    class Meta:
        model = Post
        # 'author' is handled in the form logic, so it's not included here
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs and remove it before passing to the parent class
        self.user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)

        # Set the initial value for the 'author' field to the logged-in user
        if self.user:
            self.instance.author = self.user

        # If the post instance has existing tags, initialize the 'post_tags' field with them
        if self.instance and self.instance.pk:
            self.fields['post_tags'].initial = ', '.join(
                tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        # Override the save method to save the tags
        post = super(PostForm, self).save(commit=False)

        # Save the user as the author if the post is new
        if self.user and not post.pk:
            post.author = self.user

        # Save the post object first
        if commit:
            post.save()

        # Save the tags after the post has been saved
        post.tags.set(*[tag.strip()
                      for tag in self.cleaned_data['post_tags'].split(',')])

        return post


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
