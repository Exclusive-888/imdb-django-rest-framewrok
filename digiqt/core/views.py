from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, TemplateView

from celebs.procedure import (
    get_latest_celebs, get_featured_celebs, get_random_celebs)
from celebs.models import Celebrity, Duty
from movies.procedure import (
    get_latest_movies, get_featured_movies, get_random_movies)
from movies.models import Genre, Movie, PgRating

class Home(TemplateView):
    """Homepage return featured & latest movies"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = _('IMDB Clone')

        # movies context
        context['featured_movies'] = get_featured_movies(8)
        # context['latest_movies'] = get_latest_movies(13)
        # context['random_movies'] = get_random_movies()

        # celebrities context
        context['featured_celebs'] = get_featured_celebs(3)

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
        context['celebs_title'] = _('Celebrities')
        context['celebs'] = Celebrity.objects.filter(
            name__icontains=query)

        context['duties'] = Duty.objects.filter(name__icontains=query)
        context['genres'] = Genre.objects.filter(name__icontains=query)
        context['pg_ratings'] = PgRating.objects.filter(
            name__icontains=query)
        
        context['random_movies'] = get_random_movies(3)
        context['random_celebs'] = get_random_celebs(3)

        return context
