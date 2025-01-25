from storages.backends.s3boto3 import S3Boto3Storage

class BunnyStorage(S3Boto3Storage):
    endpoint_url = 'https://storage.bunnycdn.com'
    bucket_name = 'political-images'
    custom_domain = 'https://newstropy.b-cdn.net'
    access_key = 'political-images'  # Storage zone name
    secret_key = '91a4bf5f-7f5d-4cb4-8a7df6c4e775-5207-4f14'  # API password
    querystring_auth = False
