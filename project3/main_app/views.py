import random
from django.shortcuts import render
from main_app.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Quiz, Exercise, CustomUser


from django.contrib import messages  # import messages


# Create your views here.


def index(request):
    return render(request, "home.html")


## Sign up
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid form entries")
    form = UserCreationForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


class CategoryList(ListView):
    model = Category


# class CategoryDetail(DetailView):
#     model = Category 


def take_quiz(request, category_id):
    quiz = Quiz.objects.all().filter(category_id=category_id)
    questions = []
    for q in quiz:
        questions.append(q)
    num = len(questions)-1
    while len(questions) > 5:
        questions.pop(random.randint(0, num))
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
        num = len(questions)-1
        while len(questions) > 5:
            questions.pop(random.randint(0, num))
            num -= 1
        messages.info(request, "Good luck")
    elif request.method == 'POST':
        pass
    else:
        messages.error(request, "Invalid form entries")

    # questions = [questions.append(q) for q in quiz ]
    return render(request, "main_app/exercise.html", {"exercise": exercise})
