from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Quiz, User
from .models import CustomUser, Exercise, User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView,PasswordResetForm ,SetPasswordForm



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


## Add Exercises ##

class AddExerciseForm(forms.ModelForm):
    body = forms.CharField(required=True)
    
    class Meta:
        model = Exercise
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'correctAnswer']

## Add Exercises ##   



# forms for password Reset and confirmation
class NewPasswordResetForm(PasswordResetForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return new_password2

class NewSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return new_password2
