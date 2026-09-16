from django import forms
from .models import Course, Group

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'duration_months']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Python Backend'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'course', 'mentor', 'start_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: FN-12'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'mentor': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django import forms
from .models import GroupStudent
from users.models import User

class GroupStudentForm(forms.ModelForm):
    class Meta:
        model = GroupStudent
        fields = ['group', 'student']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faqat roli STUDENT bo'lganlarni chiqaramiz, admin/mentorlarni chiqarmaymiz
        self.fields['student'].queryset = User.objects.filter(role='STUDENT').exclude(role__in=['ADMIN', 'MENTOR'])

