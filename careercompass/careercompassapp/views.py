from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#TODO: Fill in requests for entering pages - will need to make view functions for queries

def home_page(request):
    return HttpResponse('Home Page')

def profile_page(request):
    return HttpResponse('Profile Page')

def profile_edit_page(request): 
    return HttpResponse('Profile Edit Page')