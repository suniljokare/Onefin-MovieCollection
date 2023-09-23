from django.contrib import admin
from app.models import User
from django.apps import apps


exclude_models = ['AbstractUser', 'AbstractBaseUser']
app_models = apps.get_app_config('app').get_models()

for model in app_models:
    if model.__name__ not in exclude_models:
        admin.site.register(model)