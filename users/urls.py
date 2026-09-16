from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    UserLoginView,
    UserLogoutView,
    DashboardView,
    UserManagementView  # <-- Mana bu yerda import qilindi
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  # Bosh sahifa Dashboard bo'ladi
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # YANGI QO'SHILGAN URL:
    path('management/users/', UserManagementView.as_view(), name='user_management'),
]