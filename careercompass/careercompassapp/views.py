from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#TODO: Fill in requests for entering pages - will need to make view functions for queries

def home_page(request):
    return render(request, 'index.html')

def profile_page(request):
    return render(request, 'profile.html')

def edit_profile_page(request): 
    return render(request, 'edit-profile.html')

def login_page(request): 
    return render(request, 'login.html')