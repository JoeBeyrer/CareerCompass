from django.shortcuts import render, redirect
from django.http import HttpResponse
from .database_utils import *


# Create your views here.

#TODO: Fill in requests for entering pages - will need to make view functions for queries

def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def edit_profile(request): 
    return render(request, 'edit-profile.html')

def create_account(request): 
    if request.method == "POST":
        username = request.POST['userID']
        password = request.POST['password']
        fName = request.POST['fName']
        lName = request.POST['lName']
        phone = request.POST['phone']
        email = request.POST['email']
        dob = request.POST['dob']
        add_user(username, fName, lName, phone, password, dob, email)
        return redirect('login')
    else:
        # Render form html page if GET request
        return render(request, 'create-account.html')

def user_login(request): 
    return render(request, 'login.html')

def user_logout(request):
    return redirect('login')