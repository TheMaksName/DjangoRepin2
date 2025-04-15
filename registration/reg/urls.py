
from django.urls import path
from .views import registration_true, registration

urlpatterns = [
    path('', registration ),
    path('root', registration_true),
]
