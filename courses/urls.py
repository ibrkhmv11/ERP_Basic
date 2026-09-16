from django.urls import path
from .views import (
    CourseListView, CourseCreateView,
    GroupListView, GroupCreateView,
    GroupDetailView,
    assign_student_view  # <--- Yangi funksiyani import qilamiz
)

urlpatterns = [
    # Kurslar
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),

    # Guruhlar
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),

    # Guruhga o'quvchi biriktirish (Maxsus sahifa)
    path('assign-student/', assign_student_view, name='assign_student'),
]