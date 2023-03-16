from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('accounts/signup', views.signup, name='signup')
]