from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models.functions import Random
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .models import Category, Quiz, Exercise, UserCategory, CustomUser
from .forms import UserCreationForm, AddExerciseForm


def index(request):
    return render(request, "home.html")


class CategoryList(ListView):
    model = Category


################################################
##                    Quiz                   ##
################################################
def take_quiz(request, category_id):
    if request.method == 'GET':
        print(category_id)
        quiz = Quiz.objects.filter(category_id=category_id,
                                   isApproved=True).order_by(Random())[:5]
        messages.info(request, "Good luck")
        quiz_id = []
        for id in quiz:
            quiz_id.append(id.id)
        request.session['quiz_id'] = quiz_id
        return render(request, "main_app/quiz.html", {"quiz": quiz})
    elif request.method == 'POST':
        answers = []
        questionList = []
        correctAnswers = []
        wrongAnswers = []
        score = 0
        counter = 0
        print('counter', counter)
        for i in range(1, 6):
            answers.append(request.POST.get(f'answer{i}'))
        questions = request.session.get('quiz_id')
        for q in questions:
            print(q)
            questionList.append(Quiz.objects.get(id=q))
            correctAnswers.append(Quiz.objects.get(id=q).correctAnswer)
        for a in answers:
            if a == correctAnswers[counter]:
                score += 20
            elif a != correctAnswers[counter]:
                wrongAnswers.append(f"{questionList[counter].qustion}, {a}")
            counter += 1

        user = request.user.id
        print("user", user)
        category = category_id
        userLevel = CustomUser.objects.get(id=user)
        usercat = UserCategory.objects.filter(user_id=user,
                                              category_id=category)
        if usercat:
            usercat = UserCategory.objects.get(user_id=user,
                                               category_id=category)
            usercat.attempts += 1
            if score == 80:
                userLevel.level += 0.2
                usercat.level += 0.4
                messages.info(request, "0.4 points added to category level")
                messages.info(request, "0.2 points added to overall level")
            elif score == 60:
                userLevel.level += 0.1
                usercat.level += 0.3
                messages.info(request, "0.3 points added to category level")
                messages.info(request, "0.1 points added to overall level")
            elif score == 100:
                userLevel.level += 0.3
                usercat.level += 0.5
                messages.info(request, "0.5 points added to category level")
                messages.info(request, "0.3 points added to overall level")
            else:
                messages.warning(request, "Score too low, level unaffected.")
            usercat.save()
            userLevel.save()
        else:
            usercat = UserCategory(user_id=user, category_id=category)
            usercat.attempts += 1
            if score == 80:
                userLevel.level += 0.2
                usercat.level += 0.4
                messages.info(request, "0.4 points added to category level")
                messages.info(request, "0.2 points added to overall level")
            elif score == 60:
                userLevel.level += 0.1
                usercat.level += 0.3
                messages.info(request, "0.3 points added to category level")
                messages.info(request, "0.1 points added to overall level")
            elif score == 100:
                userLevel.level += 0.3
                usercat.level += 0.5
                messages.info(request, "0.5 points added to category level")
                messages.info(request, "0.3 points added to overall level")
            else:
                messages.warning(request, "Score too low, level unaffected.")
            userLevel.save()
            usercat.save()

        return render(
            request, 'main_app/score.html', {
                'questionList': questionList,
                'wrongAnswers': wrongAnswers,
                'score': score
            })


################################################
##                  Exercise                 ##
################################################
def take_exercise(request, category_id):
    if request.method == 'GET':
        exercise = Exercise.objects.filter(category_id=category_id,
                                           isApproved=True).order_by(
                                               Random())[:5]
        messages.info(request, "Good luck")
        questions = []
        for id in exercise:
            questions.append(id.id)
        request.session['questions'] = questions
        return render(request, "main_app/exercise.html",
                      {"exercise": exercise})
    elif request.method == 'POST':
        answers = []
        questionList = []
        correctAnswers = []
        wrongAnswers = []
        score = 0
        counter = 0
        print('counter', counter)
        for i in range(1, 6):
            answers.append(request.POST.get(f'answer{i}'))
        questions = request.session.get('questions')
        for q in questions:
            questionList.append(Exercise.objects.get(id=q))
            correctAnswers.append(Exercise.objects.get(id=q).correctAnswer)
        for a in answers:
            if a == correctAnswers[counter]:
                score += 20
            elif a != correctAnswers[counter]:
                wrongAnswers.append(f"{questionList[counter].question}, {a}")
            counter += 1
        return render(
            request, 'main_app/score.html', {
                'questionList': questionList,
                'wrongAnswers': wrongAnswers,
                'score': score
            })
        # messages.success(request, "exercise submitted")
        # return redirect('home')


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

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect Username or Password')
        return super().form_invalid(form)


#Add quiz
class AddQuiz(CreateView):
    model = Quiz
    fields = [
        'qustion', 'option1', 'option2', 'option3', 'option4', 'correctAnswer'
    ]
    success_url = '/'

    #function to add quiz
    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_id']
        #self.requset.user is logged user
        form.instance.user = self.request.user
        #Allows createview from valid method to do its normal work
        return super().form_valid(form)


### Add Exercises ###


class AddExercise(CreateView):
    model = Exercise
    fields = [
        'question', 'option1', 'option2', 'option3', 'option4', 'correctAnswer'
    ]

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form entries')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_id']
        form.instance.user = self.request.user
        messages.success(self.request, 'Exercise submitted!')
        return super().form_valid(form)


############################


################################################
##                 contribute                 ##
################################################
class ContributeCategoryList(ListView):
    model = Category
    template_name = "main_app/contribute.html"
