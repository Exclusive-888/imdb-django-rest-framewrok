from django.core.validators import (
    ValidationError, MaxValueValidator, MinValueValidator)
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from imdb.procedure import (
    get_age, get_duration_humanize, get_extension, random_chars, video_code)
from imdb.models import NameSlugModel


# Create your models here.
def movie_directory_path(instance, filename):
    """The computed upload folder for movie images"""
    file_and_ext = get_extension(filename)
    return f'movies/{instance.id}/{file_and_ext[0].lower()} \
        -{random_chars(5)}{file_and_ext[1]}'


class Movie(NameSlugModel):
    """Movie model"""
    # name field is overriden
    name = models.CharField(
        _('title'), max_length=245, unique=True)
    original_name = models.CharField(
        _('original title'), max_length=245, default='', blank=True)

    is_featured = models.BooleanField(
        _('featured'), default=False)

    # TODO: retrieve release_year from release_date
    release_date = models.DateField(
        _('release date'), blank=True, null=True)

    duration = models.PositiveSmallIntegerField(
        _('duration'), default=0, blank=True, help_text=_('in minutes'))

    imdb_rating = models.FloatField(
        _('IMDB rating'), default=0, blank=True,
        validators=[
            MinValueValidator(0.0, message=_(
                'min. value cannot be negative')),
            MaxValueValidator(10.0, message=_(
                'max. value cannot be more then 10'))],
        help_text=_('e.g. 6.8'))
    imdb_raters_count = models.PositiveIntegerField(  # TODO: if rating 0, this should be 0 also
        _('IMDB raters count'), default=0, blank=True)
    imdb_id = models.CharField(
        _('IMDB Id'), max_length=15, default='', blank=True,
        db_index=True)  # db_index is True for massive imports

   
    intro = models.TextField(
        _('intro'), default='', blank=True, max_length=500)
    content = RichTextField(
        _('content'), default='', blank=True)
    # TODO: MayBe: content_source be transformed into an MTM
    # or Text field
    content_source = models.URLField(
        _('content source'), default='', blank=True)
    # TODO: MayBe: an MTM for more trailers and BE for more
    # video sources
    trailer = models.URLField(
        _('trailer'), default='', blank=True,
        help_text=_('trailer url (ONLY for youtube videos yet)'))
    trailer_info = models.CharField(
        _('trailer info'), max_length=250, default='', blank=True)

    country = models.CharField(
        _('country'), max_length=100, default='', blank=True)
    language = models.CharField(
        _('language'), max_length=100, default='', blank=True)

    image = models.ImageField(
        _('image'), upload_to=movie_directory_path,
        blank=True, null=True)
    image_credit = models.CharField(
        _('image credit'), max_length=250, default='', blank=True)

    
    @cached_property
    def age(self):
        return get_age(self.release_date)

    @cached_property
    def trailer_video(self):
        return video_code(self.trailer)

    @cached_property
    def duration_humanize(self):
        return get_duration_humanize(self.duration)

    @cached_property
    def release_year(self):
        return self.release_date.year

    
    
    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')

    def get_absolute_url(self):
        return reverse('movie-detail', args=[self.slug])

    def clean(self, *args, **kwargs):
        if self.imdb_raters_count == 0 and self.imdb_rating != 0.0:
            raise ValidationError(
                _('With 0 raters, rating cannot be different than 0'))

    

