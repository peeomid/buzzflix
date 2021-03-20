from django.urls import path


from .api import HomeListView, MovieListView

urlpatterns = [
    path('home/', HomeListView.as_view(), name="home_list"),
    path('movies/', MovieListView.as_view(), name="movies"),
    ]