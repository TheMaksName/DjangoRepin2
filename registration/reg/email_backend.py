import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class YandexApiEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        success_count = 0
        for message in email_messages:
            try:
                response = requests.post(
                    "https://api.mail.yandex.net/api/v1/messages/send",
                    headers={
                        "Authorization": f"OAuth {settings.YANDEX_OAUTH_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from_name": "Repin Bot",
                        "from_email": message.from_email,
                        "to": [{"email": email} for email in message.to],
                        "subject": message.subject,
                        "body": message.body
                    }
                )
                response.raise_for_status()
                success_count += 1
                logger.info(f"Письмо отправлено через Yandex API: {message.subject}")
            except Exception as e:
                logger.error(f"Ошибка отправки через Yandex API: {str(e)}")
                if not self.fail_silently:
                    raise
        return success_count