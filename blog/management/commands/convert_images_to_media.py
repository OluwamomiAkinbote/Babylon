from django.core.management.base import BaseCommand
from blog.models import BlogPost, BlogMedia
from filer.models.filemodels import File
from django.core.files import File as DjangoFile
import os

class Command(BaseCommand):
    help = 'Convert old image field to media table'

    def handle(self, *args, **kwargs):
        count = 0
        failed_posts = []
        
        for post in BlogPost.objects.all():
            if post.image:  # Check if an image exists
                image_path = post.image.file.path  # Get file path
                
                if os.path.exists(image_path):
                    try:
                        with open(image_path, 'rb') as f:
                            django_file = DjangoFile(f, name=os.path.basename(image_path))
                            filer_file = File.objects.create(original_filename=post.image.label, file=django_file)
                            BlogMedia.objects.create(blog_post=post, media=filer_file)
                            count += 1
                    except Exception as e:
                        # Log any errors while processing this post
                        failed_posts.append((post.id, str(e)))
                else:
                    failed_posts.append((post.id, 'Image file does not exist'))

                post.image = None  # Remove the old image reference
                post.save()

        # Output success and any failed posts
        self.stdout.write(self.style.SUCCESS(f'Successfully migrated {count} images to media table.'))

        if failed_posts:
            self.stdout.write(self.style.ERROR(f'Failed to migrate the following posts:'))
            for post_id, error in failed_posts:
                self.stdout.write(self.style.ERROR(f'Post ID {post_id}: {error}'))
