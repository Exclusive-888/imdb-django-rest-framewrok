from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, TemplateView
from movies.procedure import ( get_featured_movies, get_random_movies)
from movies.models import  Movie
"""
# TODO: this part is for fast search with postgreSQL.search

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Q
"""


class Home(TemplateView):
    """Homepage return featured & latest movies, celebs"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = _('IMDB Clone')

        # movies context
        context['featured_movies'] = get_featured_movies(8)
        # context['latest_movies'] = get_latest_movies(13)
        # context['random_movies'] = get_random_movies()

        
        return context


class Search(ListView):
    model = Movie

    def get_context_data(self, *args, **kwargs):
        query = str(self.request.GET.get('q')).strip()

        context = super().get_context_data(*args, **kwargs)

        context['q'] = query
        context['title'] = _('Search')
        context['title_page_suffix'] = query
        context['movies_title'] = _('Movies')
        context['movies'] = Movie.objects.filter(name__icontains=query)
       
        context['random_movies'] = get_random_movies(3)
        return context
