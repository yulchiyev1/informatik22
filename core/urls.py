from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # User profile
    path('profile/', views.profile_page, name='profile'),

    # Student posts
    path('create-post/', views.create_post, name='create_post'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('like/<int:pk>/', views.like_post, name='like_post'),

    # Quiz submission
    path('submit-quiz/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),

    # Manual
    path('qollanma/', views.manual_page, name='manual_page'),
]
