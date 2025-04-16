from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import models
import logging

# Настройка логгера для отслеживания отправки писем
logger = logging.getLogger(__name__)

def registration(request):
    return render(request, 'registration.html')

def registration_true(request):
    if request.method != 'POST':
        return HttpResponse("Неверный метод запроса", status=405)

    return HttpResponse(str(request))