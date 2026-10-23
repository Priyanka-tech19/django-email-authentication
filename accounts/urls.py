from django.urls import path
from .views import register_view,login_view,logout_view,dashboard_view, activate,update_profile
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('register/', register_view, name='register'),
  
    path('login/',login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('dashboard/',dashboard_view, name='dashboard'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    path('update-profile/', update_profile, name='update_profile'),

# enter email for password reset
path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ),
    name='password_reset'
),

# Email sent confirmation page
path('password-reset/done/',
auth_views.PasswordResetDoneView.as_view(
    template_name='accounts/password_reset_done.html'
),
name='password_reset_done'
),

#Set a new password
path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

#Password successfully changed
path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ),
    name='password_reset_complete'

),

    
]