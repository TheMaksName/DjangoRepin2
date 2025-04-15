from django.db import transaction
from psycopg2 import IntegrityError

from .models import UserCode, ActiveUser

import random
import string

def generate_random_code(length=8):
    chars = string.ascii_uppercase + string.digits  # A-Z + 0-9
    return ''.join(random.choices(chars, k=length))

def create_unique_code_for_user(user, max_retries=5):
    for _ in range(max_retries):
        code = generate_random_code()
        try:
            with transaction.atomic():  # Защита от race condition
                user_code, created = UserCode.objects.get_or_create(
                    code=code,
                    defaults={'user': user}  # Привязываем к пользователю
                )
                if created:
                    return user_code
        except IntegrityError:  # На случай, если код уже существует (редко)
            continue
    raise ValueError("Не удалось создать уникальный код после нескольких попыток")