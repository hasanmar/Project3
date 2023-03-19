from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Quiz, User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    
class Quizform(forms.ModelForm):
    body = forms.CharField(required=True)
    class Meta:
        model = Quiz
        fields = ['qustion', 'option1', 'option2', 'option3','option4', 'correctAnswer']  
