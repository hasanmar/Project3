from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('categories', views.CategoryList.as_view(), name='categories'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='categories_detail')
]