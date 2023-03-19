from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models.functions import Random
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView


from .models import Category, Quiz, Exercise, CustomUser
from main_app.forms import UserCreationForm, AddExerciseForm


def index(request):
    return render(request, "home.html")


class CategoryList(ListView):
    model = Category



################################################
##                    Quiz                   ##
################################################
def take_quiz(request, category_id):
    if request.method == 'GET':
        quiz = Quiz.objects.filter(category_id=category_id).order_by(
            Random())[:5]
        messages.info(request, "Good luck")
        quiz_id = []
        for id in quiz:
            quiz_id.append(id.id)
        request.session['quiz_id'] = quiz_id
        return render(request, "main_app/quiz.html", {"quiz": quiz})
    elif request.method == 'POST':
        messages.success(request, "quiz submitted")
        return redirect('home')


################################################
##                  Exercise                 ##
################################################
def take_exercise(request, category_id):
    if request.method == 'GET':
        exercise = Exercise.objects.filter(category_id=category_id).order_by(
            Random())[:5]
        messages.info(request, "Good luck")
        questions = []
        for id in exercise:
            questions.append(id.id)
        request.session['questions'] = questions
        return render(request, "main_app/exercise.html",
                      {"exercise": exercise})
    elif request.method == 'POST':
        for i in range(1,6):
            print(request.POST.get(f'answer{i}'))
        messages.success(request, "exercise submitted")
        return redirect('home')


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










### Add Exercises ###

class AddExercise(CreateView):
    model = Exercise
    fields = ['question', 'option1', 'option2', 'option3', 'option4', 'correctAnswer']
    success_url = '/'

    # def get_success_url(self):
    #     return reverse()
    
    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_id']
        form.instance.user = self.request.user
        return super().form_valid(form)


############################