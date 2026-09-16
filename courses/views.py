from .models import Course, Group
from .forms import CourseForm, GroupForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group, GroupStudent
from .forms import GroupStudentForm

# 1. Kurslar ro'yxati
class CourseListView(LoginRequiredMixin, View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'courses/course_list.html', {'courses': courses})


# 2. Yangi kurs yaratish
class CourseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = CourseForm()
        return render(request, 'courses/course_form.html', {'form': form})

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
        return render(request, 'courses/course_form.html', {'form': form})


# 3. Guruhlar ro'yxati
class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        groups = Group.objects.all()
        return render(request, 'courses/group_list.html', {'groups': groups})


# 4. Yangi guruh yaratish
class GroupCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = GroupForm()
        return render(request, 'courses/group_form.html', {'form': form})

    def post(self, request):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
        return render(request, 'courses/group_form.html', {'form': form})


class GroupDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        students = GroupStudent.objects.filter(group=group)
        form = GroupStudentForm()
        return render(request, 'courses/group_detail.html', {
            'group': group,
            'students': students,
            'form': form
        })

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        form = GroupStudentForm(request.POST)
        if form.is_valid():
            group_student = form.save(commit=False)
            group_student.group = group
            group_student.save()
            return redirect('group_detail', pk=group.pk)

        students = GroupStudent.objects.filter(group=group)
        return render(request, 'courses/group_detail.html', {
            'group': group,
            'students': students,
            'form': form
        })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import GroupStudentForm


def is_admin(user):
    return user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser)


@user_passes_test(is_admin)
def assign_student_view(request):
    if request.method == 'POST':
        form = GroupStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')  # Saqlangandan keyin guruhlar ro'yxatiga o'tadi
    else:
        form = GroupStudentForm()

    return render(request, 'courses/assign_student.html', {'form': form})