from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    ProfileUpdateView,
    PasswordChangeView,
    UserLoginView,
    UserLogoutView,
    DashboardView,
    UserManagementView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  # Bosh sahifa Dashboard bo'ladi
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Profil URL-lari
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/password/', PasswordChangeView.as_view(), name='password_change'),

    # Foydalanuvchilar boshqaruvi (Admin uchun)
    path('management/users/', UserManagementView.as_view(), name='user_management'),
]