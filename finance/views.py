from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils.decorators import method_decorator

from .models import Payment
from .forms import PaymentForm
from courses.models import GroupStudent
from users.decorators import admin_required


@method_decorator(admin_required, name='dispatch')
class PaymentListView(LoginRequiredMixin, View):
    def get(self, request):
        payments = Payment.objects.all().order_by('-created_at')
        form = PaymentForm()

        # Talabalar qarzdorlik hisob-kitobi (Kurs narxi va to'langan summa farqi)
        students_balance = []
        enrolled_students = GroupStudent.objects.select_related('student', 'group', 'group__course').all()

        for gs in enrolled_students:
            course_price = gs.group.course.price
            total_paid = Payment.objects.filter(
                student=gs.student,
                group=gs.group
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            balance = course_price - total_paid

            students_balance.append({
                'student': gs.student,
                'group': gs.group,
                'course_price': course_price,
                'total_paid': total_paid,
                'balance': balance,
            })

        return render(request, 'finance/payments.html', {
            'payments': payments,
            'form': form,
            'students_balance': students_balance
        })

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')

        payments = Payment.objects.all().order_by('-created_at')
        return render(request, 'finance/payments.html', {
            'payments': payments,
            'form': form
        })