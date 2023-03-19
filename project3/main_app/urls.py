from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('categories', views.CategoryList.as_view(), name='categories'),
    # path('category/<int:pk>', views.CategoryDetail.as_view(), name='categories_detail'),
    path('category/<int:category_id>/quiz', views.take_quiz, name='quiz'),
    path('category/<int:category_id>/exercise',
         views.take_exercise,
         name='exercise'),
    
    
    
   ##Add Exercises##
   
    path('categories/<int:category_id>/addexercise', views.AddExercise.as_view(), name='add_exercise'),
    
    ##Add Exercises##
]