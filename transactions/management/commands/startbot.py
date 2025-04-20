from django.core.management.base import BaseCommand
from transactions.collector.bot import bot


class Command(BaseCommand):
    help = 'Start telegram bot'

    def handle(self, *args, **options):
        print('Starting telegram bot...')
        bot.remove_webhook()
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
