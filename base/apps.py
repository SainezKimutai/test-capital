# -*- coding: utf-8 -*-
import sys

from django.apps import AppConfig
from django.db import Error


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        from django.conf import settings  # noqa
        from django.contrib.auth.models import Group  # noqa

        if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
            try:
                for _group_var, group_name in settings.GROUPS:
                    _new_group = Group.objects.get_or_create(name=group_name) # noqa
            except Error:
                # ignore group creation fails for some reason
                pass
