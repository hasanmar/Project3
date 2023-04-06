from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("learn/", views.learn, name="learn"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("categories/", views.CategoryList.as_view(), name="categories"),
    path('category/<int:category_id>/quiz/', views.take_quiz, name='quiz'),
    path('category/<int:category_id>/exercise/',
         views.take_exercise,
         name='exercise'),
    path('categories/<int:category_id>/addquiz/',
         views.AddQuiz.as_view(),
         name='add_quiz'),
    path('leaderboards/', views.LeaderboardView.as_view(),
         name='leaderboards'),
    path("category/<int:category_id>/quiz", views.take_quiz, name="quiz"),
    path("category/<int:category_id>/exercise/",
         views.take_exercise,
         name="exercise"),
    path("contribute/",
         views.ContributeCategoryList.as_view(),
         name="contribute"),
    path("categories/<int:category_id>/addexercise/",
         views.AddExercise.as_view(),
         name='add_exercise'),
    path('account/<int:pk>/profile/', views.Profile.as_view(), name='profile'),
    path("profile/updatequiz/<int:pk>/",
         views.UpdateQuiz.as_view(),
         name="update_quiz"),
    path("profile/deletequiz/<int:pk>/",
         views.DeleteQuiz.as_view(),
         name="delete_quiz"),
    path("profile/updateexercise/<int:pk>/",
         views.UpdateExercise.as_view(),
         name="update_exercise"),
    path("profile/deleteexercise/<int:pk>/",
         views.DeleteExercise.as_view(),
         name="delete_exercise"),
    path(
        'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate,
        name='activate'),
]