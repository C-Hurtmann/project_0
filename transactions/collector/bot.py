from telebot import TeleBot
from telebot.types import Message

from django.conf import settings
from django.core.files.base import ContentFile

from ..models import StatementFile


bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


def send_message(message: str) -> None:
    admin_id = 345736809
    bot.send_message(admin_id, message)


@bot.message_handler(content_types=['document'])
def handle_csv_file(message: Message) -> None:
    if (
        doc_type := message.document.mime_type
    ) == 'text/comma-separated-values':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_content = ContentFile(downloaded_file)
        statement_file = StatementFile()
        statement_file.file.save(message.document.file_name, file_content)
        statement_file.save()
        bot.reply_to(message, 'File uploaded')
    else:
        bot.reply_to(message, f'Invalid file format - {doc_type}')
