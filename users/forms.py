from django import forms
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