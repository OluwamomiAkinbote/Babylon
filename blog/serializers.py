from rest_framework import serializers
from blog.models import (
    AuthorProfile, Category, BlogPost, Story, StoryMedia,
    Trend,  Subscription, BlogMedia
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class AuthorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = AuthorProfile
        fields = [
            'user', 'profile_picture', 'about', 
            'twitter_url', 'facebook_url', 'linkedin_url',
            'instagram_url', 'website_url', 'display_on_article'
        ]
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    # Optionally, include the parent category's details (e.g., name or slug) in the serialized data
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'show_on_navbar', 'priority', 'parent']
        read_only_fields = ['slug']

class BlogPostSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title','lead', 'content', 'date', 'category',
            'slug', 'author', 'media'
        ]
        read_only_fields = ['slug', 'date']

    def get_category(self, obj):
        if obj.category:
            return CategorySerializer(obj.category).data
        return None

    def get_author(self, obj):
        if hasattr(obj, 'author') and hasattr(obj.author, 'author_profile'):
            return AuthorProfileSerializer(obj.author.author_profile).data
        return None

    def get_media(self, obj):
        media_data = []
        image_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico')
        video_exts = ('.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.wmv', '.mpeg', '.3gp', '.ogv')

        for media in obj.media.all():
            if media.media:
                url = media.media.url
                ext = url.lower()

                if ext.endswith(image_exts):
                    media_type = 'image'
                elif ext.endswith(video_exts):
                    media_type = 'video'
                else:
                    media_type = 'unknown'

                media_data.append({
                    'media_url': url,
                    'type': media_type,
                    'caption': media.caption  # Include caption here
                })

        # Optional: if you want to return just one object if there's only one media
        if len(media_data) == 1:
            return media_data[0]

        return media_data




class StoryMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryMedia
        fields = ['id', 'media', 'caption']

    def to_representation(self, instance):
        # Adjust the media URL to be absolute
        data = super().to_representation(instance)
        if instance.media:
            data['media'] = instance.media.url  # Ensure media URL is a complete path
        return data  # Corrected: return 'data' instead of 'datama'

class StorySerializer(serializers.ModelSerializer):
    media_files = StoryMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'user', 'title', 'date', 'expires_at', 'media_files']

    def to_representation(self, instance):
        # Get the default representation first
        data = super().to_representation(instance)
        
        # Format the 'expires_at' field into the desired string format
        data['expires_at'] = instance.expires_at.strftime('%Y-%m-%dT%H:%M:%S') if instance.expires_at else None
        
        return data

















class TrendSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    file_url = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = Trend
        fields = [
            'id', 'title', 'content', 'author', 
            'file_url', 'file_type', 'date', 'slug'
        ]
        read_only_fields = ['slug', 'date']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request:
            return obj.get_absolute_file_url(request)
        return obj.get_file_url()


    def get_file_type(self, obj):
        if obj.is_image:
            return 'image'
        elif obj.is_video:
            return 'video'
        return None

