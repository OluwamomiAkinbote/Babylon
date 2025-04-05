from rest_framework import serializers
from advert.models import AdBanner

class AdBannerSerializer(serializers.ModelSerializer):
    image_small_url = serializers.SerializerMethodField()
    image_large_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = AdBanner
        fields = ['id', 'name', 'category', 'image_small_url', 'image_large_url', 'video_url', 'link', 'active', 'date', 'paragraph_positions']

    def get_image_small_url(self, obj):
        return obj.image_small.url if obj.image_small else None

    def get_image_large_url(self, obj):
        return obj.image_large.url if obj.image_large else None

    def get_video_url(self, obj):
        return obj.video.url if obj.video else None
