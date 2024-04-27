from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .database_utils import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .create_tables import *
from datetime import datetime
from .forms import *

UserModel = get_user_model()
create_users_table()
create_students_table()
create_recruiters_table()
create_posts_table()
create_followers_table()
create_likes_table()

# with connection.cursor() as cursor:
#         cursor.execute("""
#             DROP TABLE Likes;
#             DROP TABLE Followers;
#             DROP TABLE Posts;
#             DROP TABLE Recruiters;
#             DROP TABLE Students;
#             DROP TABLE Users;
#             DELETE FROM auth_user;                      
#         """)



#Create your views here.

#TODO: Fill in requests for entering pages - will need to make view functions for queries

def index(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    posts = get_following_posts(current_user)
    post_data = []
    if posts:
        for post in posts:
            has_liked = check_liked_post(request.user.username, post[0], post[1])
            likes_count = get_like_count(post[0], post[1])
            poster_type = get_user_type(post[0])
            post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type, 'has_liked': has_liked})
    return render(request, 'index.html', {'type': user_type, 'posts': post_data})


def post(request, postedBy, date):
    try:
        current_user = request.user.username
        user_type = get_user_type(current_user)
        date = datetime.strptime(date, '%Y-%m-%d-%H-%M-%S-%f')
        post = get_post(postedBy, date)
        current_user = request.user.username
        if request.method == "POST":
                if 'like' in request.POST:
                    action = request.POST['like']
                    if action =='like':
                        liked(current_user, postedBy, date)
                    elif action =='unlike':
                        unlike(current_user, postedBy, date)
                elif 'delete' in request.POST:
                    delete_post(postedBy, date)
                    return redirect('home')

        has_liked = check_liked_post(request.user.username, post[0], post[1])
        likes_count = get_like_count(post[0], post[1])
        poster_type = get_user_type(post[0])
        print(poster_type)
        return render(request, 'post.html', {'post': post, 'likes_count': likes_count, 'has_liked': has_liked, 'user_type': poster_type, 'type': user_type})
    except:
        return redirect('home')


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
    posts = get_user_posts(username)
    total_num_likes = get_user_likes_count(username)
    post_data = []
    print(student)
    if posts:
        for post in posts:
            has_liked = check_liked_post(request.user.username, post[0], post[1])
            likes_count = get_like_count(post[0], post[1])
            poster_type = get_user_type(post[0])
            post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type, 'has_liked': has_liked})

    return render(request, 'profile-student.html', {'student': student, 'followers': 
                    followers, 'following': following, 'following_list': followsList, 
                    'type': user_type, 'posts': post_data, 'total_likes': total_num_likes})

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
    posts = get_user_posts(username)
    total_num_likes = get_user_likes_count(username)
    post_data = []
    if posts:
        for post in posts:
            has_liked = check_liked_post(request.user.username, post[0], post[1])
            likes_count = get_like_count(post[0], post[1])
            poster_type = get_user_type(post[0])
            post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type, 'has_liked': has_liked})

    return render(request, 'profile-recruiter.html', {'recruiter': recruiter, 
                    'followers': followers, 'following': following, 'following_list': 
                    followsList, 'type': user_type, 'posts': post_data, 'total_likes': total_num_likes})

def edit_profile(request): 
    current_user = request.user.username
    user_type = get_user_type(current_user)
    checked_password = True
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        UserID = request.POST.get('userID', None)
        OldPassword = request.POST.get('old_password', None)
        Password = request.POST.get('password', None)
        if Password != '':
            user = get_user(current_user)
            checked_password = check_password(OldPassword, user[3])
        if not checked_password:
                messages.error(request, "Old password is incorrect.")
                return render(request, 'edit-profile.html', {'type': user_type, 'form': form, 'password_check': checked_password})
        if form.is_valid():
            UserID = form.cleaned_data['userID']
            Password = form.cleaned_data['password']
            FirstName = form.cleaned_data['fName']
            LastName = form.cleaned_data['lName']
            email = form.cleaned_data['email']
            about_me = form.cleaned_data['about_me']
            user_type = get_user_type(current_user)
            if user_type[0] == 'R':
                company_name = form.cleaned_data['company_name']
                about_company = form.cleaned_data['about_company']
                position = form.cleaned_data['position']
                update_recruiter(company_name, about_company, position, current_user)
                update_user(UserID, FirstName, LastName, '' if Password == '' else make_password(Password), about_me, email, current_user)
            else:
                university = form.cleaned_data['university']
                degree = form.cleaned_data['degree']
                current_year = form.cleaned_data['current_year']
                expected = form.cleaned_data['expected']
                gpa = form.cleaned_data['gpa']
                open_to_work = form.cleaned_data['open_to_work']
                update_student(university, degree, current_year, expected, gpa, open_to_work, current_user)
                update_user(UserID, FirstName, LastName,  '' if Password == '' else make_password(Password), about_me, email, current_user)

            if UserID != '':
                user = User.objects.get(username = current_user)
                user.username = UserID
                user.save()
                auth_user = authenticate(request, username=UserID, password=user.password)
                if auth_user is not None:
                    login(request, auth_user)
            else:
                UserID = current_user
            if Password != '':
                user = User.objects.get(username=UserID)
                user.set_password(Password)
                user.save()
                auth_user = authenticate(request, username=current_user, password=Password)
                if auth_user is not None:
                    login(request, auth_user)

            return redirect('home')
        else:
            print(form.errors)
    else:
        form = EditProfileForm()

    return render(request, 'edit-profile.html', {'type': user_type, 'form': form, 'password_check': checked_password})


def create_recruiter_account(request): 
    if request.method == "POST":
        form = RecruiterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            # Get cleaned form data
            username = form.cleaned_data['userID']
            password = form.cleaned_data['password']
            fName = form.cleaned_data['fName']
            lName = form.cleaned_data['lName']
            email = form.cleaned_data['email']
            about_me = form.cleaned_data['about_me']
            company_name = form.cleaned_data['company_name']
            about_company = form.cleaned_data['about_company']
            position = form.cleaned_data['position']
            
            # Process and save data
            user = User.objects.create_user(username=username, password=password)
            user.save()
            add_user(username, fName, lName, make_password(password), email, about_me)
            add_recruiter(username, company_name, about_company, position)
            return redirect('login')
    else:
        form = RecruiterForm()
        
    return render(request, 'create-recruiter-account.html', {'form': form})
    
def create_student_account(request): 
    if request.method == "POST":
            form = StudentForm(request.POST)
            print(form.errors)
            if form.is_valid():
                # Get all user data entered in the html form fields
                username = form.cleaned_data['userID']
                password = form.cleaned_data['password'] # Password hashed with django's built-in make_password()
                fName = form.cleaned_data['fName']
                lName = form.cleaned_data['lName']
                email = form.cleaned_data['email']
                about_me = form.cleaned_data['about_me']
                # Get all student specific data in the html form fields
                university = form.cleaned_data['university']
                degree = form.cleaned_data['degree']
                current_year = form.cleaned_data['current_year']
                expected = form.cleaned_data['expected']
                gpa = form.cleaned_data['gpa']
                open_to_work = form.cleaned_data['open_to_work']
                # Add the user to the Users table in PostgreSQL
                user = User.objects.create_user(username=username, password=password)
                user.save()
                add_user(username, fName, lName, make_password(password), email, about_me)
                add_student(username, university, degree, current_year, expected, gpa, open_to_work)
                return redirect('login')
    else:
        form = StudentForm()
    
    return render(request, 'create-student-account.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        # Get all data entered in the html form fields
        username = request.POST['userID']
        password = request.POST['password']
        # Get the users credentials using a select query and the username
        user = get_user(username)
        if user is not None and check_password(password, user[3]):
            # Set up session for the user
            request.session['user_id'] = user[0]
            auth_user = authenticate(request, username=username, password=password)
            login(request, auth_user)


            # Redirect the user to their account session
            return HttpResponseRedirect('/careercompass/')
        else:
            # Display an error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'error': True})
    else:
        return render(request, 'login.html', {'error': False})

def user_logout(request):
    logout(request)
    return redirect('login')

def create_new_post(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    if request.method == "POST":
        form = PostForm(request.POST)
        print(form.errors)
        if form.is_valid():
            Title = form.cleaned_data['Title']
            BodyText = form.cleaned_data['BodyText']
            Field = form.cleaned_data['Field']
            create_post(request.user.username, Title, BodyText, Field)
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create-post.html', {'type': user_type, 'form': form})

def show_followers_view(request, username):
    current_user = request.user.username
    current_user_type = get_user_type(current_user)
    if get_user(username):
        followers = get_followers(username)
        follower_data = []
        if followers:
            for follower in followers:
                follower_type = get_user_type(follower[0])
                follower_data.append({'follower': follower, 'user_type': follower_type})
        return render(request, 'followers.html', {'followers': follower_data, 'username': username,  'type': current_user_type})
    else:
        return redirect('home')

def show_following_view(request, username):
    current_user = request.user.username
    current_user_type = get_user_type(current_user)
    if get_user(username):
        following_list = get_following(username)
        following_data = []
        if following_list:
            for following in following_list:
                following_type = get_user_type(following[0])
                following_data.append({'followed': following, 'user_type': following_type})
        return render(request, 'following.html', {'following_list': following_data, 'username': username, 'type': current_user_type})
    else:
        return redirect('home')

def search(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    results = search_user('')
    results_data = []
    if request.method == "POST":
        search_query = request.POST['search_query']
        if search_query:  # Check if search query is not empty
            results = search_user(search_query)
    if results:
        for result in results:
            result_type = get_user_type(result[0])
            results_data.append({'result': result, 'user_type': result_type})
    return render(request, 'search.html', {'search_results': results_data, 'type': user_type})


def delete_account(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    if request.user.is_authenticated and request.method == "POST":
        userID = request.POST.get('userID')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=current_user)
            if user.check_password(password) and current_user == userID:
                user.delete()
                delete_user(userID)
                logout(request)
                return redirect('login')  # Redirect to home or any other page after successful deletion
            else:
                # Incorrect username or password
                return render(request, 'delete-account.html', {'error': 'Invalid username or password'})
        except User.DoesNotExist:
            # User does not exist
            return render(request, 'delete-account.html', {'error': 'User does not exist'})
        except Exception as e:
            # Handle other exceptions
            return render(request, 'delete-account.html', {'error': str(e)})
    else:
        return render(request, 'delete-account.html', {'type': user_type})
