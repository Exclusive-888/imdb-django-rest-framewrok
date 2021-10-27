"""Project base models inherited by other models"""

from .procedure import random_chars
from crum import get_current_user
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator
from unidecode import unidecode

from django.conf import settings
"""
# TODO: this part is for fast search with postgreSQL.search

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
"""


class StampedModel(models.Model):
    """an abstract models fields"""
    added_at = models.DateTimeField(
        _('added date'), editable=False)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        related_name='%(app_label)s_%(class)s_adders',
        verbose_name=_('added by'),
        help_text=_('User who added the db record.'))

    updated_at = models.DateTimeField(
        _('updated date'), editable=False, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        related_name='%(app_label)s_%(class)s_modifiers',
        verbose_name=_('updated by'),
        help_text=_('User who updated the db record.'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """added_by and updated_by fields are filled automatically
        by retrieving the current user. via crum.get_current_user
        """
        user = get_current_user()
        if user and not user.pk:
            user = None
        if self._state.adding:
            self.added_by = user
            self.added_at = timezone.now()
        else:
            self.updated_by = user
            self.updated_at = timezone.now()
        self.full_clean()
        super().save(*args, **kwargs)


class NameSlugModel(models.Model):
    """name and automatically (write)created slug fields"""
    name = models.CharField(
        _('name'), max_length=245, unique=True, db_index=True)
    slug = models.SlugField(
        _('slug'), max_length=255, blank=True, unique=True, db_index=True)
    extra_chars_count = models.PositiveSmallIntegerField(
        _('extra characters count'), default=5,
        validators=[MaxValueValidator(9, message=_('max value is 9'))],
        help_text=_('''The number of extra random characters'''))

    class Meta:
        abstract = True

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


class NameSlugStampedModel(StampedModel, NameSlugModel):
    
    class Meta:
        abstract = True


