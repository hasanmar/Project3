from django.urls import path
from . import views
from .views import reset_password
urlpatterns = [
    path("", views.index, name="home"),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("categories", views.CategoryList.as_view(), name="categories"),
    # path('category/<int:pk>', views.CategoryDetail.as_view(), name='categories_detail'),
    path('category/<int:category_id>/quiz', views.take_quiz, name='quiz'),
    path('category/<int:category_id>/exercise',
         views.take_exercise,
         name='exercise'),
    path('categories/<int:category_id>/addquiz', views.AddQuiz.as_view(), name='add_quiz'),   

    path("category/<int:category_id>/quiz", views.take_quiz, name="quiz"),
    path("category/<int:category_id>/exercise", views.take_exercise, name="exercise"),
    
    path("category/<int:category_id>/addexercise", views.AddExercise.as_view(), name='add_exercise'),
    path('reset-password/', reset_password, name='reset_password'),
]
