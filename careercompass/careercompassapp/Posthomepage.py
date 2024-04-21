from django.shortcuts import render
from .models import Post  # Import your Post model
from .database_utils import get_post_likes, get_user_type

def index(request):
    current_user = request.user.username
    user_type = get_user_type(current_user)
    
    # Retrieve posts from the database
    posts = Post.objects.all()  # Adjust this query based on your Post model structure and any filtering you need
    
    post_data = []
    for post in posts:
        likes_count = get_post_likes(post.posted_by, post.date_posted)  # Adjust parameters accordingly
        poster_type = get_user_type(post.posted_by)
        post_data.append({'post': post, 'likes_count': likes_count, 'user_type': poster_type})
    
    return render(request, 'index.html', {'type': user_type, 'posts': post_data})
