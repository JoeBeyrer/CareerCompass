from django.urls import path
from . import views

# URL configuration - all start with careercompass/
urlpatterns = [
    path('', views.index, name='home'),
    path('student/<str:username>/', views.student_profile, name='student-profile'),
    path('recruiter/<str:username>/', views.recruiter_profile, name='recruiter-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('login/', views.user_login, name='login'),
    path('create-recruiter-account/', views.create_recruiter_account, name='create-recruiter-account'),
    path('create-student-account/', views.create_student_account, name='create-student-account'),
    path('logout', views.user_logout, name='logout'),
    path('create-post/', views.create_new_post, name='create-post'),
    path('<str:postedBy>/post/<str:date>', views.post, name='post'),
    path('search', views.search, name='search'),
    path('followers/<str:username>/', views.show_followers_view, name='followers'),
    # TODO: Add all pages here
]
