from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Rename a category from Global News to World'

    def handle(self, *args, **kwargs):
        try:
            category = Category.objects.get(name="Global News")
            category.name = "World"
            category.save()
            self.stdout.write(self.style.SUCCESS("Renamed 'Global News' to 'World' successfully."))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("Category 'Global News' does not exist."))
