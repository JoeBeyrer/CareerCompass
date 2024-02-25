from django.urls import path
from . import views

# URL configuration - all start with careercompass/
urlpatterns = [
    path('', views.home_page),
    path('profile/', views.profile_page),
    path('edit-profile/', views.profile_edit_page),

    # TODO: Add all pages here
]
