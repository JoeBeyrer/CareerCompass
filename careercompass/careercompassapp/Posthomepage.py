
from django.shortcuts import render
from .models import Posts, Users  # Import relevant models
from .database_utils import get_user_type, get_following_posts, get_post_likes

def index(request):
    # Get the current user's username
    current_user = request.user.username
    
    # Determine the type of user (e.g., student or recruiter)
    user_type = get_user_type(current_user)
    
    # Retrieve posts from the database for the current user's following list
    following_posts = get_following_posts(current_user)
    
    # Prepare the post data to be passed to the template
    post_data = []
    for post in following_posts:
        # Get the number of likes for each post
        likes_count = get_post_likes(post.PostedBy, post.DatePosted)
        
        # Get the user type who posted the current post
        posted_by_user = Users.objects.get(UserID=post.PostedBy)
        poster_type = get_user_type(posted_by_user.UserID)
        
        # Construct a dictionary containing post details and related data
        post_info = {
            'post': post,               # The Post object itself
            'likes_count': likes_count, # Number of likes for the post
            'user_type': poster_type    # Type of user who posted the post
        }
        
        # Append the post info to the post_data list
        post_data.append(post_info)
    
    # Render the index.html template with the user type and post data
    return render(request, 'index.html', {'type': user_type, 'posts': post_data})
