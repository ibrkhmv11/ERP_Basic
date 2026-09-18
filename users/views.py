from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator

# Modellarni import qilish
from .models import User
from courses.models import Course, Group, GroupStudent
from finance.models import Payment
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordChangeForm


# 1. Ro'yxatdan o'tish (Register)
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Ro'yxatdan o'tgach avtomatik tizimga kiradi
            return redirect('dashboard')
        return render(request, 'users/register.html', {'form': form})


# 2. Tizimga kirish (Login)
class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'users/login.html', {'form': form})


# 3. Tizimdan chiqish (Logout)
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def _profile_template(user):
    """Foydalanuvchi roliga qarab profil templateini qaytaradi."""
    if user.is_admin:
        return 'users/profile_admin.html'
    elif user.is_mentor:
        return 'users/profile_mentor.html'
    return 'users/profile_student.html'


# 4. Foydalanuvchi profili (Profile)
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        return render(request, _profile_template(request.user), {
            'profile_form': profile_form,
            'password_form': password_form,
        })


# 4a. Profil ma'lumotlarini yangilash (ProfileUpdate)
class ProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma'lumotlari muvaffaqiyatli yangilandi!")
            return redirect('profile')
        password_form = CustomPasswordChangeForm(user=request.user)
        return render(request, _profile_template(request.user), {
            'profile_form': form,
            'password_form': password_form,
            'active_tab': 'profile',
        })


# 4b. Parolni o'zgartirish (PasswordChange)
class PasswordChangeView(LoginRequiredMixin, View):
    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Sessionni yangilash — parol o'zgarsa avtomatik logout bo'lmasligi uchun
            update_session_auth_hash(request, user)
            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")
            return redirect('profile')
        profile_form = ProfileUpdateForm(instance=request.user)
        return render(request, _profile_template(request.user), {
            'profile_form': profile_form,
            'password_form': form,
            'active_tab': 'password',
        })


# 5. Dashboard (Asosiy panel va statistikalar)
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {}

        # 1. ADMIN DASHBOARD
        if user.is_admin:
            context = {
                'total_students': User.objects.filter(role='STUDENT').count(),
                'total_mentors': User.objects.filter(role='MENTOR').count(),
                'total_courses': Course.objects.count(),
                'total_groups': Group.objects.filter(is_active=True).count(),
                'total_revenue': Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
            }
            return render(request, 'dashboard/admin_dashboard.html', context)

        # 2. MENTOR DASHBOARD
        elif user.is_mentor:
            # Mentor biriktirilgan guruhlar
            mentor_groups = Group.objects.filter(mentor=user, is_active=True)
            context = {
                'my_groups': mentor_groups,
            }
            return render(request, 'dashboard/mentor_dashboard.html', context)

        # 3. STUDENT DASHBOARD
        else:
            # Talaba a'zo bo'lgan guruhlar va to'lovlari
            enrolled_groups = GroupStudent.objects.filter(student=user)
            my_payments = Payment.objects.filter(student=user).order_by('-created_at')

            # Shaxsiy qarzdorlik hisob-kitobi
            total_paid = my_payments.aggregate(Sum('amount'))['amount__sum'] or 0
            total_course_fee = sum([eg.group.course.price for eg in enrolled_groups])
            debt = total_course_fee - total_paid

            context = {
                'enrolled_groups': enrolled_groups,
                'my_payments': my_payments,
                'debt': debt,
            }
            return render(request, 'dashboard/student_dashboard.html', context)


# 6. Admin uchun foydalanuvchilar rollarini boshqarish
class UserManagementView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Faqat admin yoki superuser kira oladi
        return self.request.user.is_authenticated and (self.request.user.is_admin or self.request.user.is_superuser)

    def get(self, request):
        users_qs = User.objects.all().order_by('-date_joined')

        # Qidiruv (ism yoki email bo'yicha)
        search_query = request.GET.get('q', '').strip()
        if search_query:
            users_qs = users_qs.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        # Rol bo'yicha filter
        role_filter = request.GET.get('role', '').strip().upper()
        if role_filter in ['ADMIN', 'MENTOR', 'STUDENT']:
            users_qs = users_qs.filter(role=role_filter)

        # Pagination — har sahifada 15 ta
        paginator = Paginator(users_qs, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'users': page_obj,  # Templateda users deb ishlatilgan eski nom uchun
            'search_query': search_query,
            'role_filter': role_filter,
            'total_count': users_qs.count(),
        }
        return render(request, 'users/user_management.html', context)

    def post(self, request):
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('new_role')

        target_user = get_object_or_404(User, id=user_id)

        if new_role in ['ADMIN', 'MENTOR', 'STUDENT']:
            target_user.role = new_role
            if new_role == 'ADMIN':
                target_user.is_staff = True
            target_user.save()
            messages.success(request, f"{target_user.username} ning roli {new_role} ga o'zgartirildi!")

        return redirect('user_management')