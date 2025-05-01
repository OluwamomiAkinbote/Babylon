from rest_framework import serializers
from .models import ComposeNews, Like, Retweet, Bookmark, NewsUser, Interest


# serializers.py

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'continent', 'category', 'public_figure']


class NewsUserSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = NewsUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'profile_image',
            'interests',
            'date_joined',
        ]
        read_only_fields = ['date_joined']


class ComposeNewsSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    retweets_count = serializers.IntegerField(read_only=True)
    bookmarks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ComposeNews
        fields = [
            'id',
            'author',
            'author_username',
            'content',
            'media',
            'is_reply',
            'in_reply_to',
            'created_at',
            'updated_at',
            'likes_count',
            'retweets_count',
            'bookmarks_count',
        ]
        read_only_fields = ['author', 'likes_count', 'retweets_count', 'bookmarks_count']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'news', 'created_at']

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = ['id', 'user', 'original_news', 'comment', 'created_at']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'news', 'created_at']
