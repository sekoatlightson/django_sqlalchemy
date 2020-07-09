
from django.urls import path
from . import views

app_name = 'rental'

urlpatterns = [
    path('', views.index,name='index'),
]