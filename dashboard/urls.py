from django.urls import path
from . import views as v


urlpatterns = [
    path('', v.test, name='test'),
    path('prod/', v.home, name='home'),
]
