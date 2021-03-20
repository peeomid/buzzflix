import csv
# import json
import ast

from django.core.management.base import BaseCommand

from Buzzflix.movies.models import Category, Movie


class Command(BaseCommand):
    help = 'Load movies from sample file.'

    def handle(self, *args, **options):
        random_poster_prefix = 'https://buzzflix.com/images'
        all_categories = {}
        with open('movies_metadata.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                try:
                    line_count += 1
                    print(f"processing {line_count}: {row['title']}")
                    categories = []

                    movie_genres = ast.literal_eval(row['genres'])
                    for genre in movie_genres:
                        if genre['name'] in all_categories.keys():
                            category = all_categories[genre['name']]
                        else:
                            category = Category.objects.create(name=genre['name'])
                            all_categories[genre['name']] = category

                        categories.append(category)

                    movie = Movie.objects.create(
                            title=row['title'],
                            synopsis=row['overview'],
                            poster_image=f"{random_poster_prefix}{row['poster_path']}"
                        )

                    movie.categories.add(*categories)
                except Exception as e:
                    print(e)
            print(f'Processed {line_count} lines.')
