from django.contrib import admin
from .models import Course, Group, GroupStudent
from users.models import User

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_months')
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'mentor', 'start_date', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('name',)

@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ('group', 'student')
    list_filter = ('group',)
    search_fields = ('student__username', 'group__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            # Faqat role='STUDENT' bo'lganlarni olamiz, ADMIN va MENTOR larni qat'iy chiqarib tashlaymiz
            kwargs["queryset"] = User.objects.filter(role='STUDENT').exclude(role__in=['ADMIN', 'MENTOR'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)