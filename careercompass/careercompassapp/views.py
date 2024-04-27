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

# This code is used to create all required tables locally
UserModel = get_user_model()
create_users_table()
create_students_table()
create_recruiters_table()
create_posts_table()
create_followers_table()
create_likes_table()

# This code is used to delete all tables and their data
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

# Home page view
def index(request):
    current_user = request.user.username
    # Get the current users type for link fields
    user_type = get_user_type(current_user)
    # Get all posts from users the current user follows
    posts = get_following_posts(current_user)
    post_data = []
    if posts:
        for post in posts:
            # Check each post for if the user has liked them, the number of likes they have, and the account type of the poster (for profile link field)
            has_liked = check_liked_post(request.user.username, post[0], post[1])
            likes_count = get_like_count(post[0], post[1])
            poster_type = get_user_type(post[0])
            post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type, 'has_liked': has_liked})
    # Render the html with the provided fields
    return render(request, 'index.html', {'type': user_type, 'posts': post_data})

# View for posts
def post(request, postedBy, date):
    # If a post exists, we render it, otherwise we redirect to the home page
    try:
        current_user = request.user.username
        user_type = get_user_type(current_user)
        # Get the timestamp posted from the post link
        date = datetime.strptime(date, '%Y-%m-%d-%H-%M-%S-%f')
        # Get the post from the posts table using the posters ID and the timestamp
        post = get_post(postedBy, date)
        # If the request is a POST - the user has liked or unliked the post
        if request.method == "POST":
                # If the user has already liked the post, this will unlike it - and vice versa
                if 'like' in request.POST:
                    action = request.POST['like']
                    if action =='like':
                        liked(current_user, postedBy, date)
                    elif action =='unlike':
                        unlike(current_user, postedBy, date)
                elif 'delete' in request.POST:
                    delete_post(postedBy, date)
                    return redirect('home')
        # Gather all required data to display the post
        has_liked = check_liked_post(request.user.username, post[0], post[1])
        likes_count = get_like_count(post[0], post[1])
        poster_type = get_user_type(post[0])
        # Render the post with all gathered fields
        return render(request, 'post.html', {'post': post, 'likes_count': likes_count, 'has_liked': has_liked, 'user_type': poster_type, 'type': user_type})
    except:
        return redirect('home')

# Display the students profile using their userID
def student_profile(request, username):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    # A POST request means the user was followed or unfollowed - handle each using the followers table
    if request.method == "POST":
        action = request.POST['follow']
        if action =='unfollow':
            unfollow(username, current_user)
        elif action =='follow':
            follow(username, current_user)
    # Gather all student data
    student = get_student_data(username)
    followers = get_follower_count(username)
    following = get_following_count(username)
    followsList = following_list(current_user)
    # Get all posts made by the user and add their respective metadata
    posts = get_user_posts(username)
    total_num_likes = get_user_likes_count(username)
    post_data = []
    if posts:
        for post in posts:
            has_liked = check_liked_post(request.user.username, post[0], post[1])
            likes_count = get_like_count(post[0], post[1])
            poster_type = get_user_type(post[0])
            post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type, 'has_liked': has_liked})

    return render(request, 'profile-student.html', {'student': student, 'followers': 
                    followers, 'following': following, 'following_list': followsList, 
                    'type': user_type, 'posts': post_data, 'total_likes': total_num_likes})

# Display the recruiters profile using their userID
def recruiter_profile(request, username):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    # A POST request means the user was followed or unfollowed - handle each using the followers table
    if request.method == "POST":
        action = request.POST['follow']
        if action =='unfollow':
            unfollow(username, current_user)
        elif action =='follow':
            follow(username, current_user)
    # Gather all recruiter data
    recruiter = get_recruiter_data(username)
    followers = get_follower_count(username)
    following = get_following_count(username)
    followsList = following_list(current_user)
    # Get all posts made by the user and add their respective metadata
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

# Updates fields on the users profile after edits were made
def edit_profile(request): 
    current_user = request.user.username
    user_type = get_user_type(current_user)
    checked_password = True
    # If the user has saved the changes, we create an EditProfile form with all inputs
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        UserID = request.POST.get('userID', None)
        OldPassword = request.POST.get('old_password', None)
        Password = request.POST.get('password', None)
        # If a changed password was entered, we must ensure the old password field matches the users current password
        if Password != '':
            user = get_user(current_user)
            checked_password = check_password(OldPassword, user[3])
        if not checked_password:
                messages.error(request, "Old password is incorrect.")
                return render(request, 'edit-profile.html', {'type': user_type, 'form': form, 'password_check': checked_password})
        # If the form is falid, we read in all fields and update the users table
        if form.is_valid():
            UserID = form.cleaned_data['userID']
            Password = form.cleaned_data['password']
            FirstName = form.cleaned_data['fName']
            LastName = form.cleaned_data['lName']
            email = form.cleaned_data['email']
            about_me = form.cleaned_data['about_me']
            user_type = get_user_type(current_user)
            # If the user is a recruiter, we add the recruiter inputs from the form and update the users and recruiters tables
            if user_type[0] == 'R':
                company_name = form.cleaned_data['company_name']
                about_company = form.cleaned_data['about_company']
                position = form.cleaned_data['position']
                update_recruiter(company_name, about_company, position, current_user)
                update_user(UserID, FirstName, LastName, '' if Password == '' else make_password(Password), about_me, email, current_user)
            # If the user is a student, we add the student inputs from the form and update the users and students tables
            else:
                university = form.cleaned_data['university']
                degree = form.cleaned_data['degree']
                current_year = form.cleaned_data['current_year']
                expected = form.cleaned_data['expected']
                gpa = form.cleaned_data['gpa']
                open_to_work = form.cleaned_data['open_to_work']
                update_student(university, degree, current_year, expected, gpa, open_to_work, current_user)
                update_user(UserID, FirstName, LastName,  '' if Password == '' else make_password(Password), about_me, email, current_user)
            # If the userID is changed, we must update the user_auth table for authentication and re-login the user
            if UserID != '':
                user = User.objects.get(username = current_user)
                user.username = UserID
                user.save()
                auth_user = authenticate(request, username=UserID, password=user.password)
                if auth_user is not None:
                    login(request, auth_user)
            else:
                UserID = current_user
            # If the password is changed, we must update the user_auth table for authentication and re-login the user
            if Password != '':
                user = User.objects.get(username=UserID)
                user.set_password(Password)
                user.save()
                auth_user = authenticate(request, username=current_user, password=Password)
                if auth_user is not None:
                    login(request, auth_user)

            return redirect('home')
    else:
        form = EditProfileForm()

    return render(request, 'edit-profile.html', {'type': user_type, 'form': form, 'password_check': checked_password})


def create_recruiter_account(request): 
    # When a recruiter account is created, a POST request is made
    if request.method == "POST":
        form = RecruiterForm(request.POST)
        if form.is_valid():
            # Get all user data entered in the html form fields
            username = form.cleaned_data['userID']
            password = form.cleaned_data['password']
            fName = form.cleaned_data['fName']
            lName = form.cleaned_data['lName']
            email = form.cleaned_data['email']
            about_me = form.cleaned_data['about_me']
            # Get all recruiter specific data in the html form fields
            company_name = form.cleaned_data['company_name']
            about_company = form.cleaned_data['about_company']
            position = form.cleaned_data['position']
            
            # Process and save data for user authentication
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Add the user to the users and recruiters tables with a Password hashed by django's built-in make_password()
            add_user(username, fName, lName, make_password(password), email, about_me)
            add_recruiter(username, company_name, about_company, position)
            return redirect('login')
    else:
        form = RecruiterForm()
        
    return render(request, 'create-recruiter-account.html', {'form': form})
    
def create_student_account(request): 
    # When a student account is created, a POST request is made
    if request.method == "POST":
            form = StudentForm(request.POST)
            if form.is_valid():
                # Get all user data entered in the html form fields
                username = form.cleaned_data['userID']
                password = form.cleaned_data['password'] 
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
                # Process and save data for user authentication
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # Add the user to the students and recruiters tables with a Password hashed by django's built-in make_password()
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
    # Simply logout the users session and redirect them to the login page
    logout(request)
    return redirect('login')

def create_new_post(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    if request.method == "POST":
        form = PostForm(request.POST)
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
    # Get the user from the users table
    if get_user(username):
        # Get a list of all the users followers
        followers = get_followers(username)
        follower_data = []
        # Collect metadata for each follower to display
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
    # Get the user from the users table
    if get_user(username):
        # Get a list of all the users followers
        following_list = get_following(username)
        following_data = []
        # Collect metadata for each follower to display
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
    # Set initial search to '' to collect all users for display
    results = search_user('')
    results_data = []
    if request.method == "POST":
        # Get the search query entered when the search button is clicked
        search_query = request.POST['search_query']
        if search_query:  # Check if search query is not empty
            # Return the results from the users database
            results = search_user(search_query)
    if results:
        # Gather user metadata for display and profile links
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
        
        # Ensure the users correct username and password are entered before permanently deleting the user from the database
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
