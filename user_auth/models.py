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
class Member(models.Model):
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
