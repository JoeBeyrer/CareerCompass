from django.urls import path
from . import views

# URL configuration - all start with careercompass/
urlpatterns = [
    path('', views.home_page),
    path('profile/', views.profile_page),
    path('edit-profile/', views.edit_profile_page),
    path('login/', views.login_page),
    path('create-account/', views.create_account_page),
    # TODO: Add all pages here
]
