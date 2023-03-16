from django.shortcuts import render
from main_app.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category


from django.contrib import messages #import messages


# Create your views here.

def index(request):
    return render(request, 'home.html')






## Sign up
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid form entries')
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

class CategoryList(LoginRequiredMixin, ListView):
    model = Category

class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category

        
