from django.urls import path
from . import views as v
from .dash_apps.finished_apps import test

urlpatterns = [
    path('', v.home, name='home'),
]
