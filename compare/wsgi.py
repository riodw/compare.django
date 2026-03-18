"""
WSGI config for compare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compare.settings")

application = get_wsgi_application()

# Pre-warm the GraphQL schema at startup to avoid gunicorn worker timeout on first request.
# The django_graphene_filters schema build (deepcopy of filter fields) is slow on low-CPU servers.
import compare.schema  # noqa: E402
