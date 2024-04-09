from django.urls import path

from SWAG_auth.views import *

app_name = "auth"

urlpatterns = [
    path('login', LoginPageView.as_view(), name='login'),
    path('register', RegisterPageView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset_password', ResetPasswordPageView.as_view(), name='reset_password'),
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
    path('auth/profile/<str:pk>',
         UpdateProfileView.as_view(), name='profile'),

    # USER
    path('auth/create_user', CreateUserPageView.as_view(), name='create_user'),
    path('auth/manage_users', ManageUsersPageView.as_view(),
         name='manage_users'),
    path('auth/delete_user/<str:pk>',
         DeleteUserView.as_view(), name='delete_user'),
    path('auth/update_user/<str:pk>',
         EditUserView.as_view(), name='update_user'),

    # ADMIN
    path('auth/create_admin', CreateAdminPageView.as_view(), name='create_admin'),
    path('auth/manage_admin', ManageAdminPageView.as_view(), name='manage_admin'),
    path('auth/update_admin/<str:pk>',
         EditAdminView.as_view(), name='update_admin'),
    path('auth/delete_admin/<str:pk>',
         DeleteAdminView.as_view(), name='delete_admin'),

]