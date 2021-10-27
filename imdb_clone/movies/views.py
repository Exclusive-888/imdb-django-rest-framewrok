from django.db.models import Count, Prefetch
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from movies.models import Movie
from movies.procedure import get_random_movies_limited




class MovieDetailView(DetailView):
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.object.name
        context['title_alt'] = _('Movie')
        context['random_movies'] = get_random_movies_limited(3)
        return context


class MovieListView(ListView):
    model = Movie

    def get_queryset(self):
        qs = super().get_queryset().only(
            'slug', 'name', 'image', 'release_date',
            'imdb_rating', 'duration')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Movies')
        context['random_movies'] = get_random_movies_limited(3)
        return context


class TopMovieListView(ListView):
    model = Movie

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('imdb_rating')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Top Movies')
        context['description'] = _('Top Rated Movies of IMDB')
        context['random_movies'] = get_random_movies_limited(3)
        return context

