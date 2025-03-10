from django.urls import path
from .views import bot_webhook

urlpatterns = [
    path('telegram-webhook/<str:token>/', bot_webhook, name='telegram_bot_webhook'),
]