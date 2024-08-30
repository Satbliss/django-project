from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateProfileform, UpdateUserForm

# Create your views here.

def home(request):
    return render(request, 'users/home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        
        return super(RegisterView, self).dispatch(self, request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')
        
        return render(request, self.template_name, {'form': form})
    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'  # template for password reset form
    email_template_name = 'users/password_reset_email.html' # template for the content of password reset email
    subject_template_name = 'users/password_reset_subject' # template for the subject line of password reset email
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      "If you don't receive an email," \
                      "please make sure you've etered the address you registered with, and check you spam folder. " #provides feedback to users after form submission
    success_url = reverse_lazy('users-home') #redirects users to a specific url after successful submission of password reset request

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed your password"
    success_url = reverse_lazy('users-home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileform(request.POST, request.FILES, request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated succesffully')
            return redirect(to = 'users-profile')
    
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileform(instance=request.user.profile)

    
    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
