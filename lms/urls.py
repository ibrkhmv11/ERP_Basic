from django.urls import path
from .views import AttendanceView

urlpatterns = [
    path('groups/<int:group_id>/attendance/', AttendanceView.as_view(), name='attendance'),
]