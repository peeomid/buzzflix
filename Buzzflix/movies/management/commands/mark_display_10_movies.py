from django.core.management.base import BaseCommand

from Buzzflix.movies.models import Category, Movie


class Command(BaseCommand):
    help = 'Mark first 10 movies of each category to show on home.'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        for category in categories:
            movies = category.movies.all()[:10]
            Movie.objects.filter(id__in=movies.values_list('id', flat=True)).update(display_on_home=True)
