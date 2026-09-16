from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Admin panelda ko'rinadigan ustunlar
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    # Filtrlash uchun maydonlar (roli bo'yicha saralash)
    list_filter = ('role', 'is_staff', 'is_active')

    # 'role' maydonini admin panelda tahrirlash uchun qo'shamiz
    fieldsets = UserAdmin.fieldsets + (
        ('Rolni o\'zgartirish', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('role', 'phone')}),
    )