from django.db import models
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

class AdCategory(models.TextChoices):
    LEADERBOARD = 'Leaderboard', 'Leaderboard'
    INLINE = 'Inline', 'Inline Content'
    HOME = 'Home', 'Home-Inline'
    SIDEBAR = 'Sidebar', 'Sidebar Ad'

class AdBanner(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=AdCategory.choices)
    image_small = FilerImageField(blank=True, null=True, related_name='ads_image_small', on_delete=models.CASCADE)
    image_large = FilerImageField(blank=True, null=True, related_name='ads_image_large', on_delete=models.CASCADE)
    video = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name='ads_video')
    link = models.URLField()
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    paragraph_positions = models.JSONField(default=list)

    def __str__(self):
        return f"{self.category} - {self.link}"
