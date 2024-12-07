
from django import forms
from .models import Subscription
from .models import AuthorProfile


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email']


class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ['profile_picture', 'about', 'twitter_url', 'facebook_url', 'linkedin_url', 'instagram_url', 'website_url', 'display_on_article']
