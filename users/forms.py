import re
from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import User


class RegisterForm(forms.ModelForm):
    # Parol va parolni tasdiqlash uchun alohida inputlar
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Parol"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Parolni tasdiqlang"
    )

    class Meta:
        model = User
        # HTML formaga chiqariladigan ustunlar
        fields = ['username', 'first_name', 'last_name', 'phone']
        labels = {
            'username': 'Login',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'phone': 'Telefon raqam',
        }

    # 1. Ikki parol bir xilligini tekshirish (Validation)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Parollar bir xil emas!")

        return cleaned_data

    # 2. Foydalanuvchini bazaga saqlash
    def save(self, commit=True):
        user = super().save(commit=False)
        # Parolni bazaga shifrlab (hash qilib) saqlaymiz
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Foydalanuvchi profil ma'lumotlarini yangilash formasi"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'avatar']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'phone': 'Telefon raqam',
            'avatar': 'Profil rasmi',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiyangizni kiriting',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone:
            # +998 XX XXX-XX-XX yoki +998XXXXXXXXX formatini tekshirish
            pattern = r'^\+998\d{9}$'
            clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
            if not re.match(pattern, clean_phone):
                raise forms.ValidationError(
                    "Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak (masalan: +998901234567)"
                )
            return clean_phone
        return phone

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size'):
            # Max 2MB
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Rasm hajmi 2MB dan oshmasligi kerak.")
            # Faqat jpg, png, webp
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if hasattr(avatar, 'content_type') and avatar.content_type not in allowed_types:
                raise forms.ValidationError("Faqat JPG, PNG yoki WebP formatidagi rasmlar ruxsat etiladi.")
        return avatar


class CustomPasswordChangeForm(DjangoPasswordChangeForm):
    """Django standart PasswordChangeForm-ni o'zbekcha label-lar bilan kengaytirish"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Joriy parol"
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Joriy parolni kiriting',
            'autocomplete': 'current-password',
        })
        self.fields['new_password1'].label = "Yangi parol"
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yangi parolni kiriting',
            'autocomplete': 'new-password',
        })
        self.fields['new_password1'].help_text = (
            "Parol kamida 8 ta belgidan iborat bo'lishi, "
            "faqat raqamlardan iborat bo'lmasligi kerak."
        )
        self.fields['new_password2'].label = "Yangi parolni tasdiqlang"
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yangi parolni qayta kiriting',
            'autocomplete': 'new-password',
        })
        self.fields['new_password2'].help_text = ""