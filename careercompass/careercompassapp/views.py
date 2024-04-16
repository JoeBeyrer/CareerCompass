from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .database_utils import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, get_user_model
from django.contrib import messages

UserModel = get_user_model()

# Create your views here.

#TODO: Fill in requests for entering pages - will need to make view functions for queries

def index(request):
    return render(request, 'index.html')

def student_profile(request, username):
    student = get_student_data(username)
    followers = get_follower_count(username)
    following = get_following_count(username)

    return render(request, 'profile-student.html', {'student': student, 'followers': followers, 'following': following})

def recruiter_profile(request, username):
    recruiter = get_recruiter_data(username)
    followers = get_follower_count(username)
    following = get_following_count(username)

    return render(request, 'profile-recruiter.html', {'recruiter': recruiter, 'followers': followers, 'following': following})

def edit_profile(request): 
    return render(request, 'edit-profile.html')

def create_recruiter_account(request): 
    if request.method == "POST":
        # Get all data entered in the html form fields
        username = request.POST['userID']
        password = make_password(request.POST['password']) # Password hashed with django's built-in make_password()
        fName = request.POST['fName']
        lName = request.POST['lName']
        phone = request.POST['phone']
        email = request.POST['email']
        dob = request.POST['dob']
        about_me = request.POST['about_me']
        # Get all recruiter specific data in the html form fields
        company_name = request.POST['company_name']
        about_company = request.POST['about_company']
        position = request.POST['position']
        company_link = request.POST['company_link']
        # Add the user to the Users table in PostgreSQL
        add_user(username, fName, lName, phone, password, dob, email, about_me)
        add_recruiter(username, company_name, about_company, position, company_link)
        return redirect('login')
    else:
        # Render form html page if GET request
        return render(request, 'create-recruiter-account.html')
    
def create_student_account(request): 
    if request.method == "POST":
        # Get all user data entered in the html form fields
        username = request.POST['userID']
        password = make_password(request.POST['password']) # Password hashed with django's built-in make_password()
        fName = request.POST['fName']
        lName = request.POST['lName']
        phone = request.POST['phone']
        email = request.POST['email']
        dob = request.POST['dob']
        about_me = request.POST['about_me']
        # Get all student specific data in the html form fields
        university = request.POST['university']
        degree = request.POST['degree']
        current_year = request.POST['current_year']
        expected = request.POST['expected']
        gpa = request.POST['gpa']
        open_to_work = request.POST['open_to_work']
        # Add the user to the Users table in PostgreSQL
        add_user(username, fName, lName, phone, password, dob, email, about_me)
        add_student(username, university, degree, current_year, expected, gpa, open_to_work)
        return redirect('login')
    else:
        # Render form html page if GET request
        return render(request, 'create-student-account.html')

def user_login(request):
    if request.method == "POST":
        # Get all data entered in the html form fields
        username = request.POST['userID']
        password = request.POST['password']
        # Get the users credentials using a select query and the username
        user = get_user(username)
        if user is not None and check_password(password, user[4]):
            # Set up session for the user
            request.session['user_id'] = user[0]

            # Redirect the user to their account session
            return HttpResponseRedirect('http://127.0.0.1:8000/careercompass/')
        else:
            # Display an error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    return redirect('login')