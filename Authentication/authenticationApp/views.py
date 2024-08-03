from django.shortcuts import render, HttpResponse,redirect,HttpResponseRedirect
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .form import SignUpForm,LoginForm
from rest_framework.response import Response

from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

def home(request):
    return render(request,"home.html")
 


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the user in and issue JWT tokens
            login(request, user)  

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return JsonResponse({
                'access': access_token,
                'refresh': refresh_token
            })
        
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
               
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Return the tokens in the response
                return JsonResponse({
                    'access': access_token,
                    'refresh': refresh_token
                })

        
        return render(request, 'login.html', {'form': form})
    
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
