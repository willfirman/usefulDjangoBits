from django.urls import path
from useful_django_bits import views


app_name = 'useful_django_bits'

urlpatterns = [
    path('useful_django_tags/', views.useful_django_tags),
]
