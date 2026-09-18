from django import forms
from .models import Course, Group, GroupStudent
from users.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'duration_months']
        labels = {
            'name': 'Kurs nomi',
            'description': 'Tavsif',
            'price': 'Narxi (so\'m)',
            'duration_months': 'Davomiyligi (oy)',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: Python Backend',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Kurs haqida qisqacha ma\'lumot...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            'duration_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '3',
                'min': '1',
                'max': '36',
            }),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'course', 'mentor', 'start_date', 'is_active']
        labels = {
            'name': 'Guruh nomi',
            'course': 'Kurs',
            'mentor': 'Mentor',
            'start_date': 'Boshlanish sanasi',
            'is_active': 'Faol',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: FN-12',
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
            }),
            'mentor': forms.Select(attrs={
                'class': 'form-select',
            }),
            # Sana validatsiyasi: faqat 2020–2030 oralig'ini qabul qiladi
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': '2020-01-01',
                'max': '2030-12-31',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Select-larga O'zbek tilidagi placeholder
        self.fields['course'].empty_label = "— Kursni tanlang —"
        self.fields['mentor'].empty_label = "— Mentorni tanlang —"


class GroupStudentForm(forms.ModelForm):
    class Meta:
        model = GroupStudent
        fields = ['group', 'student']
        labels = {
            'group': 'Guruh',
            'student': 'Talaba',
        }
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faqat roli STUDENT bo'lganlarni chiqaramiz, admin/mentorlarni chiqarmaymiz
        self.fields['student'].queryset = User.objects.filter(role='STUDENT').exclude(role__in=['ADMIN', 'MENTOR'])
        self.fields['group'].empty_label = "— Guruhni tanlang —"
        self.fields['student'].empty_label = "— Talabani tanlang —"
