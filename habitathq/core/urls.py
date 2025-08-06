from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('dashboard-test/', views.dashboard, name='dashboard'),

    path('complaint/new/', views.create_complaint, name='create_complaint'),
    path('', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('visitor/add/', views.add_visitor, name='add_visitor'),
    path('security/gate-view/', views.security_view, name='security_view'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('profile/edit/', views.profile_update, name='profile_update'),
]