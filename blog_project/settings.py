from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os

# settings.py

import os

SECRET_KEY = os.getenv('SECRET_KEY')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = ENVIRONMENT == 'development'

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://newstropy.online",
        "https://ayo.newstropy.online",
        "https://www.newstropy.online",
    ]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "newstropy.onrender.com",
    "newstropy.online",
    "ayo.newstropy.online",
    "www.newstropy.online",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://newstropy.onrender.com",
    "https://newstropy.online",
    "https://ayo.newstropy.online",
    "https://www.newstropy.online",
]

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

CORS_ALLOW_CREDENTIALS = True




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites', 
    "rest_framework", 
    'corsheaders',
    'blog',
    'shop',
    'dashboard',
    'advert',
    'user_auth',
    'file_manager',
    'tailwind',
    'theme',
    'django_browser_reload',
    'tinymce',
    'mptt',
    'polymorphic',
    'easy_thumbnails',
    'filer',
    'storages',
    'whitenoise.runserver_nostatic',
]

SITE_ID = 2
TINYMCE_DEFAULT_CONFIG = {
    'height': '450px',
    'width': '100%',
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'advlist autolink lists link image charmap print preview hr anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table directionality emoticons template paste textpattern code',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen preview save print | insertfile image media template link anchor codesample | code',
    'extended_valid_elements': 'script[charset|src|type], iframe[src|frameborder|width|height|allowfullscreen], blockquote[class]',
    'valid_children': '+body[script], +div[script], +div[iframe]',
    'content_css': 'default',
}




TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ["127.0.0.1"]

FILER_CANONICAL_URL = 'sharing/'

THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_project.wsgi.application'

# Database settings
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,  # Keep database connections open for 600 seconds
        ssl_require=True   # Enforce SSL for secure database connections
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_TZ = True


# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = "boltzmann"
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False


TWITTER_API_KEY =  os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY =  os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_BEARER_TOKEN =  os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_ACCESS_TOKEN =  os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET =  os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


# Static files
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STORAGES = {
    # Media file (image) management   
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'user_login'

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # Default to 587 if not set
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'  # Convert string to boolean
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
