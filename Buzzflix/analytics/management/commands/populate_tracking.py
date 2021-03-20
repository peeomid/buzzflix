import random
import datetime
from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

from Buzzflix.analytics.models import Tracking
from Buzzflix.movies.models import Movie

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate tracking by fake user and watching data.'

    def handle(self, *args, **options):
        # users = self.populate_users()
        users = User.objects.all()
        movies = Movie.objects.all()
        self.populate_date_range(users, movies)

    def populate_users(self):
        NUM_USERS_TO_POPULATE = 30

        # populate fake users first
        users = []
        for i in range(NUM_USERS_TO_POPULATE):
            user = User.objects.create(
                    first_name='User%dFirstName' % i, 
                    last_name='User%dLastName' % i,
                    username='user%d' % i,
                    email='user%d@mydomain.com' % i,
                    password='pasSw0rd',
                    is_active=True,
                    )
            users.append(user)

        return users

    def populate_date_range(self, users, movies):
        today = timezone.now()
        last_month_date = today - relativedelta(months=1)
        for i in range((today-last_month_date).days):
            date = last_month_date + relativedelta(days=i)
            print('working on date: ', date)
            self.populate_events(date, users, movies)

    def populate_events(self, date, users, movies):
        """populate events in given date
        
        Args:
            users (TYPE): list of users to populate
            date (TYPE): given date to populate
        """
        NUM_EVENTS_TO_POPULATE = 500
        events = settings.DEFINED_ANALYTICS_EVENTS
        watching_types = (
                1,  # watch full movie all at once
                2,  # start watch a movie, and stop in the middle
                2,
                2,
                3,  # continue watching till the end
                4,  # continue watching but stop again
                2,
            )

        for i in range(NUM_EVENTS_TO_POPULATE):
            watching_type = random.choice(watching_types)
            if watching_type == 3 or watching_type == 4:
                # This is to handle in case there's no unfinished tracking
                finished_movies = Tracking.objects.filter(event_name='MOVIE_FINISH').values_list('movie_id', flat=True)
                unfinished_tracking = Tracking.objects.filter(event_name='MOVIE_START').exclude(movie_id__in=finished_movies)

                if unfinished_tracking:
                    select_tracking = random.choice(unfinished_tracking)
                    movie = select_tracking.movie
                    user = select_tracking.user
                else:
                    watching_type = random.choice([1, 2])


            if watching_type == 1:
                # watch full movie all at once
                user = random.choice(users)
                movie = random.choice(movies)
                Tracking.objects.create(
                        event_name='MOVIE_VIEW',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_START',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_FINISH',
                        user=user,
                        movie=movie,
                        created_at=date + datetime.timedelta(hours=1)
                    )
            elif watching_type == 2:
                # start watch a movie, and stop in the middle
                user = random.choice(users)
                movie = random.choice(movies)
                Tracking.objects.create(
                        event_name='MOVIE_VIEW',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_START',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_END',
                        user=user,
                        movie=movie,
                        created_at=date + datetime.timedelta(minutes=30)
                    )
            elif watching_type == 3:
                # continue watching till the end
                Tracking.objects.create(
                        event_name='MOVIE_VIEW',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_START',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_FINISH',
                        user=user,
                        movie=movie,
                        created_at=date + datetime.timedelta(minutes=30)
                    )                
            else:
                # continue watching but stop again
                Tracking.objects.create(
                        event_name='MOVIE_VIEW',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_START',
                        user=user,
                        movie=movie,
                        created_at=date
                    )
                Tracking.objects.create(
                        event_name='MOVIE_END',
                        user=user,
                        movie=movie,
                        created_at=date + datetime.timedelta(minutes=15)
                    )                