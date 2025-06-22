# serializers.py

from rest_framework import serializers
from .models import Member, Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'continent', 'category', 'public_figure']


class MemberSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = Member
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
