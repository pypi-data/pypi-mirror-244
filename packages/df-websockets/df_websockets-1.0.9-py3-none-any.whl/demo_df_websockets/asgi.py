"""
ASGI config for demo_df_websockets project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

#  Copyright (c) 2023.
#
#  This file asgi.py is part of cookiecutter-django.
#  Please check the LICENSE file for sharing or distribution permissions.
#

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_df_websockets.settings")

application = get_asgi_application()
