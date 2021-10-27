import random
from random import shuffle

from django.db.models import Q, Max, Prefetch

from movies.models import MovieCrew
from .models import Celebrity

number_of_items = 5


def no_objects_exists():
    """Checks  db table has any objects recorded.
    If there is no object, it  return an empty list 
    """
    if not Celebrity.objects.exists():
        return []


def get_celebs_queryset():
    """Retrieves the object' queryset."""
    return Celebrity.objects.only(
        'slug', 'name', 'image')


def get_celebs_list():
    """Some functions need a list of  queryset."""
    return list(get_celebs_queryset())


def get_latest_celebs(num=number_of_items):
    """Retrieves latest added celebrities from db if there is any"""
    # no_objects_exists()

    return get_celebs_queryset()[:num]


def get_featured_celebs(num=number_of_items):
    """Retrieves featured celebrities from db if there is any.
    is_featured is a field in the model. Also the featured item 
    should have either trailer or image.
    """
    # no_objects_exists()

    featured = get_celebs_queryset().filter(
        Q(is_featured=True) & (
            Q(trailer__isnull=False) | Q(image__isnull=False)))
    if len(featured):
        featured = list(featured)  
        shuffle(featured)  # make the list randomly ordered
        return featured[:num]
    else:
        return get_latest_celebs(num)


def get_random_celebs(num=number_of_items):
    """Retrieves 'num' number of random celebs."""
    # no_objects_exists()

    celebs = get_celebs_list()  # list in order to shuffle
    shuffle(celebs)  # make the list randomly ordered
    return celebs[:num]
