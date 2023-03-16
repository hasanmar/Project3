from django.urls import path
from . import views


urlpatterns =[
    # Routes
    path('', views.home, name='home'),
]