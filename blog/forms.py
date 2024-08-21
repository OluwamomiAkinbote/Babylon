# blog/forms.py

from django import forms
from .models import Comment
from .models import Subscription

class CommentForm(forms.ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_email'].required = False  # Make email field optional for logged-in users

    def clean_parent_comment_id(self):
        parent_comment_id = self.cleaned_data.get('parent_comment_id')
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(pk=parent_comment_id)
                return parent_comment.id
            except Comment.DoesNotExist:
                raise forms.ValidationError("Invalid parent comment ID.")
        return None

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name','email']
