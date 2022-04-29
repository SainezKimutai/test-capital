from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.deletion import SET_NULL

from django_extensions.db.models import TimeStampedModel


class AuthBaseEntity(TimeStampedModel):
    """
        An abstract base class model that provides "created_by", "modified_by", "created" and "modified" fields
        to track changes to model instances.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default=None,
        editable=False,
        related_name="created_by_%(app_label)s_%(class)s_set",
        verbose_name="created by")

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default=None,
        editable=False,
        related_name="modified_by_%(app_label)s_%(class)s_set",
        verbose_name="modified by")

    class Meta:
        abstract = True
