from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import Random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from .models import Category, Quiz, Exercise, CustomUser, UserCategory
from django.views.generic import ListView, DetailView, CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserCreationForm
from .tokens import account_activation_token
from django.core.paginator import Paginator, EmptyPage



def index(request):
    return render(request, "home.html")


def learn(request):
    return render(request, "learn.html")


class CategoryList(ListView):
    model = Category


################################################
##                    Quiz                   ##
################################################
@login_required
def take_quiz(request, category_id):
    if request.method == 'GET':
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
        all_answers = []
        score = 0
        counter = 0
        for i in range(1, 6):
            answers.append(request.POST.get(f'answer{i}'))
        questions = request.session.get('quiz_id')
        for q in questions:
            questionList.append(Quiz.objects.get(id=q))
            correctAnswers.append(Quiz.objects.get(id=q).correctAnswer)
        for a in answers:
            if a == correctAnswers[counter]:
                score += 20
                all_answers.append([True, questionList[counter].qustion])
            elif a != correctAnswers[counter]:
                all_answers.append([False, questionList[counter].qustion])
            counter += 1

        user = request.user.id
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
        return render(request, 'main_app/score.html', {
            'all_answers': all_answers,
            'score': score
        })


################################################
##                  Exercise                 ##
################################################
@login_required
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
        all_answers = []
        score = 0
        counter = 0
        for i in range(1, 6):
            answers.append(request.POST.get(f'answer{i}'))
        questions = request.session.get('questions')
        for q in questions:
            questionList.append(Exercise.objects.get(id=q))
            correctAnswers.append(Exercise.objects.get(id=q).correctAnswer)
        for a in answers:
            if a == correctAnswers[counter]:
                score += 20
                all_answers.append([True, questionList[counter].question])
            elif a != correctAnswers[counter]:
                all_answers.append([False, questionList[counter].question])
            counter += 1
        return render(request, 'main_app/score.html', {
            'all_answers': all_answers,
            'score': score
        })


################################################
##             Authentication                 ##
################################################
## Sign up
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string(
                'acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            login(request, user)
            messages.success(
                request,
                f"Sign-up Successful! Welcome, {user.username}, to our community."
            )
            messages.success(
                request, f"Activation link has been sent to your email id.")
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


################################################
##                  Add Quiz                  ##
################################################
class AddQuiz(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = [
        'qustion', 'option1', 'option2', 'option3', 'option4', 'correctAnswer'
    ]

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form entries')
        return super().form_invalid(form)

    def form_valid(self, form):
        print(self.request.user)
        form.instance.category_id = self.kwargs['category_id']
        form.instance.user = self.request.user
        messages.success(self.request, 'Quiz submitted!')
        return super().form_valid(form)


################################################
##              Add Exercises                 ##
################################################
class AddExercise(LoginRequiredMixin, CreateView):
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


################################################
##                 contribute                 ##
################################################
class ContributeCategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = "main_app/contribute.html"


################################################
##                 Email Verification         ##
################################################


def activate(request, uidb64, token):
    user = CustomUser()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Your email has been confirmed. Welcome to our website!')
        return redirect('home')
    else:
<<<<<<< HEAD
        return HttpResponse('Activation link is invalid!')
=======
        return HttpResponse('Activation link is invalid!')   
    
    
class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise
>>>>>>> 987a2fce37277d948fa4683c7b70925f7e8cb4c2


################################################
##                 Profile Page               ##
################################################


class Profile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        PAGES_NUM = 5
        context = super(Profile, self).get_context_data(**kwargs)
        id = int(self.kwargs.get('pk'))
        categories = UserCategory.objects.filter(user_id=id)
<<<<<<< HEAD
        quiz = Quiz.objects.filter(user_id=id)
        exercise = Exercise.objects.filter(user_id=id)

        paginator1 = Paginator(quiz, PAGES_NUM)
        paginator2 = Paginator(exercise, PAGES_NUM)

        page1 = self.request.GET.get('page1')
        try:
            quiz_obj = paginator1.get_page(page1)
        except PageNotAnInteger:
            quiz_obj = paginator1.get_page(1)
        except EmptyPage:
            quiz_obj = paginator1.get_page(paginator1.num_pages)

        page2 = self.request.GET.get('page2')
        try:
            exercise_obj = paginator2.get_page(page2)
        except PageNotAnInteger:
            exercise_obj = paginator2.get_page(1)
        except EmptyPage:
            exercise_obj = paginator2.get_page(paginator2.num_pages)

=======
        page = self.request.GET.get('page', 1)
        print('categories', categories)
        paginator = self.paginator_class(categories, 4)
        categories = paginator.page(page)
>>>>>>> 987a2fce37277d948fa4683c7b70925f7e8cb4c2
        context['userCategories'] = categories
        context['quiz'] = quiz_obj
        context['exercise'] = exercise_obj

        return context


################################################
##                  Edit Quiz                  ##
################################################
class UpdateQuiz(LoginRequiredMixin, UpdateView):
    model = Quiz
    fields = [
        'qustion', 'option1', 'option2', 'option3', 'option4', 'correctAnswer'
    ]

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user_id})

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form entries')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.isApproved = False
        messages.success(self.request, 'Quiz Updated!')
        return super().form_valid(form)


################################################
##               Delete Quiz                  ##
################################################
class DeleteQuiz(LoginRequiredMixin, DetailView):
    model = Quiz

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user_id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


################################################
##              Update Exercise               ##
################################################
class UpdateExercise(LoginRequiredMixin, UpdateView):
    model = Exercise
    fields = [
        'question', 'option1', 'option2', 'option3', 'option4', 'correctAnswer'
    ]

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user_id})

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form entries')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.isApproved = False
        messages.success(self.request, 'Exercise Updated!')
        return super().form_valid(form)


################################################
##               Delete Exercise              ##
################################################
class DeleteExercise(LoginRequiredMixin, DetailView):
    model = Exercise

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user_id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class LeaderboardView(ListView):
    model = CustomUser
    fields = '__all__'
<<<<<<< HEAD

    class Meta:
        ordering = ['-level']

    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        cats = []
        for i in range(1, 11):
            cats.append(
                UserCategory.objects.filter(
                    category_id=i).order_by('-level')[:5])
        print(cats)
        context['userCategories'] = cats
=======
    ordering = ["-level"] 
        
    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        cats =[]
        categories = Category.objects.all()
        for i in range(1,11):
            cats.append(UserCategory.objects.filter(category_id = i).order_by('-level')[:5]) 
        print(cats)
        context['userCategories'] = cats 
        context['categories'] = categories 
        context['loop_times'] = range(0,5)
>>>>>>> 987a2fce37277d948fa4683c7b70925f7e8cb4c2
        return context


## IMAGE POST##

# def profile(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ImageForm(instance=request.user.profile)
#     return render(request, 'profile.html', {'form': form})