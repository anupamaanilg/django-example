from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from login_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index.html")

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('login_app:index'))
            else:
                return HttpResponseRedirect("Account Not Active.")
        else:
            print("Someone tried to logged in and Failed.")
            print("username{} and password{}".format(username,password))
            return HttpResponseRedirect("Invalid login details")
    else:
        return render(request,"login.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:index'))

@login_required
def special(request):
    return HttpResponseRedirect("You ARE Logged In.")

def registration(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user =user

            if 'picture' in request.FILES:
                profile.profile_pic = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,"register.html", {'user_form':user_form,'profile_form':profile_form,'registered':registered})
