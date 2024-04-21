from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .database_utils import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .create_tables import *

UserModel = get_user_model()
create_users_table()
create_students_table()
create_recruiters_table()
create_posts_table()
create_followers_table()
create_likes_table()



# Create your views here.

#TODO: Fill in requests for entering pages - will need to make view functions for queries

def index(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    posts = get_following_posts(current_user)
    print(posts)
    post_data = []
    for post in posts:
        likes_count = get_post_likes(post[0], post[1])  # Adjust parameters accordingly
        poster_type = get_user_type(post[0])
        post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type})
    print(post_data)
    return render(request, 'index.html', {'type': user_type, 'posts': post_data})

def student_profile(request, username):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    if request.method == "POST":
        action = request.POST['follow']
        if action =='unfollow':
            unfollow(username, current_user)
        elif action =='follow':
            follow(username, current_user)
    student = get_student_data(username)
    followers = get_follower_count(username)
    following = get_following_count(username)
    followsList = following_list(current_user)

    return render(request, 'profile-student.html', {'student': student, 'followers': 
                    followers, 'following': following, 'following_list': followsList, 'type': user_type})

def recruiter_profile(request, username):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    if request.method == "POST":
        action = request.POST['follow']
        if action =='unfollow':
            unfollow(username, current_user)
        elif action =='follow':
            follow(username, current_user)
    recruiter = get_recruiter_data(username)
    followers = get_follower_count(username)
    following = get_following_count(username)
    followsList = following_list(current_user)

    return render(request, 'profile-recruiter.html', {'recruiter': recruiter, 
                    'followers': followers, 'following': following, 'following_list': 
                    followsList, 'type': user_type})

def edit_profile(request): 
    current_user = request.user.username
    user_type = get_user_type(current_user)
    return render(request, 'edit-profile.html', {'type': user_type})

def create_recruiter_account(request): 
    if request.method == "POST":
        # Get all data entered in the html form fields
        username = request.POST['userID']
        password = request.POST['password'] # Password hashed with django's built-in make_password()
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
        user = User.objects.create_user(username=username, email=email,   password=password)
        user.save()
        add_user(username, fName, lName, phone, make_password(password), dob, email, about_me)
        add_recruiter(username, company_name, about_company, position, company_link)
        return redirect('login')
    else:
        # Render form html page if GET request
        return render(request, 'create-recruiter-account.html')
    
def create_student_account(request): 
    if request.method == "POST":
        # Get all user data entered in the html form fields
        username = request.POST['userID']
        password = request.POST['password'] # Password hashed with django's built-in make_password()
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
        open_to_work = 'Y' if request.POST['open_to_work'] else 'N'
        # Add the user to the Users table in PostgreSQL
        user = User.objects.create_user(username=username, password=password)
        user.save()
        add_user(username, fName, lName, phone, make_password(password), dob, email, about_me)
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
            print(username)
            print(password)
            auth_user = authenticate(request, username=username, password=password)
            print(auth_user)
            login(request, auth_user)


            # Redirect the user to their account session
            return HttpResponseRedirect('/careercompass/')
        else:
            # Display an error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def create_new_post(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    if request.method == "POST":
        Title = request.POST['Title']
        BodyText = request.POST['BodyText']
        Field = request.POST['Field']
        Link = request.POST['Link'] # May need to change
        create_post(request.user.username, Title, BodyText, Field, Link)
        return redirect('home')
    else:
        # Render form html page if GET request
        return render(request, 'create-post.html', {'type': user_type})