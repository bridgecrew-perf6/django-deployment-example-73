from django.shortcuts import render
from basic_App.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):    
    return render(request,'basic_App/index.html')


@login_required #make sure person is already logged in
def special(request):    
    return HttpResponse("You are logged in , Nice !")

@login_required #make sure person is already logged in
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):    

    registered = False

    if request.method == "POST":

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()  #form info mapped to user database model
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False) #dont save data no to model, check if picture is there
            profile.user = user


            if 'profile_pic' in request.FILES: # for csv, images, pdf
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            register = True
            return render(request,'basic_App/thankyou.html') 
        else:
            print(user_form.errors,profile_form.errors)    

    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_App/registration.html', 
              {'user_form':user_form,
              'profile_form':profile_form,
              'registered':registered})    

def user_login(request):
     if request.method == "POST":
         username = request.POST.get('username')
         password = request.POST.get('password')

         user=authenticate(username=username,password=password)


         if user:
             if user.is_active:
                 login(request,user)
                 return HttpResponseRedirect(reverse('index'))

             else:
                 return HttpResponse('ACCOUNT NOT ACTIVE')    
         else:
            print('Someone tried to login and failed')
            print("Username: {} and password{}".format(username,password))    
            return HttpResponse("Invalid login details supplied!")
     else:
         return render(request, 'basic_App/login.html',{})