from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views
from .views import UserPostListView, ContributorListView


urlpatterns = [
    path(r'register/', users_views.register, name='register'),
    path(r'profile/<str:username>', users_views.profile, name='profile'),
    path('post/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('<str:username>/contribution/', ContributorListView.as_view(), name='user-contribution'),
    path(r'login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path(r'password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path(r'password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path(r'password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path(r'password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
]