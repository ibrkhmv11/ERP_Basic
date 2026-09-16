from django.db import models
from courses.models import GroupStudent

class Attendance(models.Model):
    group_student = models.ForeignKey(
        GroupStudent,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name="Talaba"
    )
    date = models.DateField(verbose_name="Dars sanasi")
    is_present = models.BooleanField(default=True, verbose_name="Keldi/Kelmadi")
    score = models.PositiveIntegerField(default=0, verbose_name="Uy vazifasi bali (0-100)")

    class Meta:
        # Bitta talabaga bir kunda faqat 1 marta davomat qilinadi
        unique_together = ('group_student', 'date')

    def __str__(self):
        status = "Keldi" if self.is_present else "Kelmadi"
        return f"{self.group_student.student.username} - {self.date} ({status})"