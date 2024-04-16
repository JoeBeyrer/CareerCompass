from django.urls import path
from . import views

# URL configuration - all start with careercompass/
urlpatterns = [
    path('', views.index, name='home'),
    path('student/', views.student_profile, name='student'),
    path('recruiter/', views.recruiter_profile, name='recruiter'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('login/', views.user_login, name='login'),
    path('create-account/', views.create_account, name='create-account'),
    path('logout/', views.user_logout, name='logout'),
    # TODO: Add all pages here
]
