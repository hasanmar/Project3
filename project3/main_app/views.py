from random import randint

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Category, Quiz, Exercise, CustomUser
from main_app.forms import UserCreationForm


def index(request):
    return render(request, "home.html")


class CategoryList(ListView):
    model = Category


# class CategoryDetail(DetailView):
#     model = Category


def take_quiz(request, category_id):
    quiz = Quiz.objects.all().filter(category_id=category_id)
    questions = []
    for q in quiz:
        questions.append(q)
    num = len(questions) - 1
    while len(questions) > 5:
        questions.pop(randint(0, num))
        num -= 1
    messages.info(request, "Good luck")
    # print(questions)
    return render(request, "main_app/quiz.html", {"questions": questions})


def take_exercise(request, category_id):
    exercise = Exercise.objects.all().filter(category_id=category_id)
    if request.method == 'GET':
        questions = []
        for e in exercise:
            questions.append(e)
        num = len(questions) - 1
        while len(questions) > 5:
            questions.pop(randint(0, num))
            num -= 1
        messages.info(request, "Good luck")
    elif request.method == 'POST':
        pass
    else:
        messages.error(request, "Invalid form entries")

    # questions = [questions.append(q) for q in quiz ]
    return render(request, "main_app/exercise.html", {"exercise": exercise})


################################################
##             Authentication                 ##
################################################
## Sign up
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Sign-up Successful! Welcome, {user.username}, to our community."
            )
            return redirect("home")
        else:
            messages.error(request, "Invalid form entries")
    form = UserCreationForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


## Sign in
class CustomLoginView(LoginView):
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username', '')
        messages.success(
            self.request,
            f'Welcome back, {username}! You have successfully signed in.')
        return super().form_valid(form)
