from django.db import models
import uuid

# --- Interests ---
class Interest(models.Model):
    CONTINENT_CHOICES = [
        ('Africa', 'Africa'),
        ('North America', 'North America'),
        ('Europe', 'Europe'),
        ('Asia', 'Asia'),
        ('South America', 'South America'),
    ]

    CATEGORY_CHOICES = [
        ('politics', 'Politics'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('business', 'Business'),
        ('tech', 'Tech'),
        ('fashion', 'Fashion'),
        ('health', 'Health'),
        ('travel', 'Travel'),
        ('education', 'Education'),
        ('culture', 'Culture'),
        ('news', 'News'),
        ('finance', 'Finance'),
        ('startup', 'Startup'),
        ('crypto', 'Cryptocurrency'),
        ('automobile', 'Automobile'),
        ('food', 'Food'),
        ('career', 'Career'),
        ('art', 'Art'),
        ('parenting', 'Parenting'),
        ('relationship', 'Relationship'),
    ]

    name = models.CharField(max_length=150)
    continent = models.CharField(max_length=20, choices=CONTINENT_CHOICES, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    public_figure = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

# --- User ---
class NewsUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# --- Compose News ---
class ComposeNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(NewsUser, on_delete=models.CASCADE, related_name='composed_news')
    content = models.TextField(max_length=1000, blank=True)
    media = models.FileField(upload_to='news_media/', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    in_reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def retweets_count(self):
        return self.retweets.count()

    @property
    def bookmarks_count(self):
        return self.bookmarks.count()

# --- Like ---
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE, related_name='likes')
    news = models.ForeignKey(ComposeNews, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news')

    def __str__(self):
        return f"{self.user.username} liked a post"

# --- Retweet ---
class Retweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE, related_name='retweets')
    original_news = models.ForeignKey(ComposeNews, on_delete=models.CASCADE, related_name='retweets')
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'original_news')

    def __str__(self):
        return f"{self.user.username} retweeted a post"

# --- Bookmark ---
class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE, related_name='bookmarks')
    news = models.ForeignKey(ComposeNews, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news')

    def __str__(self):
        return f"{self.user.username} bookmarked a post"
