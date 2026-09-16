from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from courses.models import Group, GroupStudent
from .models import Attendance

class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        students = GroupStudent.objects.filter(group=group)
        today = date.today()

        # Bugungi sana uchun mavjud davomatlarni lug'atga yig'amiz
        attendances = Attendance.objects.filter(group_student__in=students, date=today)
        attendance_dict = {att.group_student_id: att for att in attendances}

        return render(request, 'lms/attendance.html', {
            'group': group,
            'students': students,
            'today': today,
            'attendance_dict': attendance_dict,
        })

    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        students = GroupStudent.objects.filter(group=group)
        today = date.today()

        for gs in students:
            is_present = request.POST.get(f'present_{gs.id}') == 'on'
            score = request.POST.get(f'score_{gs.id}', 0)

            Attendance.objects.update_or_create(
                group_student=gs,
                date=today,
                defaults={
                    'is_present': is_present,
                    'score': int(score) if score else 0
                }
            )

        return redirect('attendance', group_id=group.id)