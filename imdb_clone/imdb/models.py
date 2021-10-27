"""Project-wide base models inherited by other models"""

from .procedure import random_chars
from crum import get_current_user
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator
from unidecode import unidecode

from django.conf import settings

class NameSlugModel(models.Model):
    """name and automatically created slug fields"""
    name = models.CharField(
        _('name'), max_length=245, unique=True, db_index=True)
    slug = models.SlugField(
        _('slug'), max_length=255, blank=True, unique=True, db_index=True)
    extra_chars_count = models.PositiveSmallIntegerField(
        _('extra characters count'), default=5,
        validators=[MaxValueValidator(9, message=_('max value is 9'))],
        help_text=_('''The number of extra random characters be suffixed 
        to slug if needed. default is 0 and it means no extra chars.'''))

    """
    # TODO: this part is for fast search with postgreSQL.search
    name_vector = SearchVectorField(null=True)
    """

    class Meta:
        abstract = True

        """
        # TODO: this part is for fast search with postgreSQL.search
        indexes = [
            GinIndex(fields=['name_vector'])
        ]
        """

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slug is created once at the creation of object, 
        unidecode converts the non-english letters to english ones.
        """
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
            count = self.extra_chars_count
            if count > 0:
                self.slug += '-' + random_chars(count)

        super().save(*args, **kwargs)

