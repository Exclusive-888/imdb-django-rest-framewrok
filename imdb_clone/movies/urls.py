from django.urls import include, path

from movies.views import ( MovieDetailView, MovieListView, TopMovieListView,)

base_dir = 'html/'

urlpatterns = [
    path('', include([
        path('top/', TopMovieListView.as_view(
            template_name=base_dir + 'movies/movie_list.html'
        ), name='top-movie-list'),
        path('<slug:slug>/', MovieDetailView.as_view(
            template_name=base_dir + 'movies/movie_detail.html'
        ), name='movie-detail'),
        path('', MovieListView.as_view(
            template_name=base_dir + 'movies/movie_list.html'
        ), name='movie-list')
    ])),
]
