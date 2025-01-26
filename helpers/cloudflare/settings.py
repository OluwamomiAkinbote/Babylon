import logging
import os
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()


# Check if all required environment variables are present
CLOUDFLARE_R2_CONFIG_OPTIONS = {}

bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET")
endpoint_url = os.getenv("CLOUDFLARE_R2_BUCKET_ENDPOINT")
access_key = os.getenv("CLOUDFLARE_R2_ACCESS_KEY")
secret_key = os.getenv("CLOUDFLARE_R2_SECRET_KEY")

if all([bucket_name, endpoint_url, access_key, secret_key]):
    CLOUDFLARE_R2_CONFIG_OPTIONS = {
        "bucket_name": bucket_name,
        "default_acl": "public-read",  # "private"
        "signature_version": "s3v4",
        "endpoint_url": endpoint_url,
        "access_key": access_key,
        "secret_key": secret_key,
    }

    # Optionally log the successful loading
    logger.info("Cloudflare R2 configuration loaded successfully.")
else:
    logger.error("Missing one or more required Cloudflare R2 environment variables.")
