from django.apps import AppConfig
from rest_framework.response import Response

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

