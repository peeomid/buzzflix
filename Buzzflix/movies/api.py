import datetime

from django.db.models import Prefetch

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Category, Movie
from .serializers import CategorySerializer, MovieSerializer

class HomeListView(APIView):
    """View to handle list on home screen
    With highlighted movie and categories and movies
    """
    
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().prefetch_related(
            Prefetch('movies', 
                queryset=Movie.objects.filter(display_on_home=True))
            )

        # Get highlighted movie based on day of year
        # So each day of year should return consistently 1 movie
        today = datetime.datetime.now()
        day_of_year = today.timetuple().tm_yday
        highlighted_movies = Movie.objects.filter(is_highlighted=True)
        count = highlighted_movies.count()
        highlighted_movie = highlighted_movies[day_of_year % count]

        response = {
            'highlighted_movie': MovieSerializer(highlighted_movie).data if highlighted_movie else None,
            'categories': CategorySerializer(categories, many=True).data
        }
        return Response(response)

class MovieListView(generics.ListAPIView):
    """Movie list View
    Used to query movie for each category to get more movies
    """
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def filter_queryset(self, queryset):
        if 'category' in self.request.query_params:
            category_id = self.request.query_params.get('category')
            queryset = queryset.filter(categories__id=category_id)

        return queryset