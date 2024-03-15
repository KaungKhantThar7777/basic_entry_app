"""Define URL patterns for accounts"""

from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    # Include default app urls
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name="register")
]