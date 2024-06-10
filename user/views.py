from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm




from django.db import connection


def home(request):
    return render(request, 'home.html')



#This is the register view 
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} ')

            return redirect(to='registration_under_review')        # Each registration need to be under review of the admin to be able to login 

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        user = form.get_user()    #will get u the users username
        #print(user)
        
        # A Flag to keep track if the user is found in the database
        user_found = False 
        with connection.cursor() as cursor:
            cursor.execute(""" SELECT  auth_user.username,users_userprofile.is_approved          
                                FROM auth_user
                                JOIN  users_userprofile ON auth_user.id = users_userprofile.user_id """)

            rows = cursor.fetchall()
            for row in rows:
                #print(row)
                if str(user) == row[0]:
                    user_found=True
                    #print('yes')
                    if row[1]:
                        return super(CustomLoginView, self).form_valid(form)
            return redirect(to='registration_under_review')


        




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

# to access your profile u need to be login in to the page : add a permission 
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


# Each registration need to be under review of the admin to be able to login so a page registration_under_review will show up to the user until he get accepted


def registration_under_review(request):
    return render(request, 'registration_under_review.html')










