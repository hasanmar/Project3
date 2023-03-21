from django.urls import path
from . import views
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
    path("contribute/",views.ContributeCategoryList.as_view(),name="contribute"),
    path("categories/<int:category_id>/addexercise", views.AddExercise.as_view(), name='add_exercise'),
    path('account/<int:pk>/profile',views.Profile.as_view(), name='profile'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        views.activate, name='activate'),
 
]
