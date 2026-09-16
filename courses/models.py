from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kurs nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'm)")
    duration_months = models.PositiveIntegerField(default=1, verbose_name="Davomiyligi (oy)")

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Guruh nomi")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name="Kurs"
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentor_groups',
        limit_choices_to={'role': 'MENTOR'},
        verbose_name="Mentor"
    )
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    def __str__(self):
        return f"{self.name} - ({self.course.name})"

class GroupStudent(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name="Guruh"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrolled_groups',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name="Talaba"
    )
    joined_at = models.DateField(auto_now_add=True, verbose_name="Qo'shilgan sanasi")

    class Meta:
        unique_together = ('group', 'student')

    def __str__(self):
        return f"{self.student.get_full_name() or self.student.username} - {self.group.name}"