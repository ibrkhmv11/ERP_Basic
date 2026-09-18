from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'group', 'amount', 'payment_type']
        labels = {
            'student': 'Talaba',
            'group': 'Guruh',
            'amount': 'Summa (so\'m)',
            'payment_type': 'To\'lov turi',
        }
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 500000', 'min': '0'}),
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O'zbek tilidagi bo'sh tanlov matnlari
        self.fields['student'].empty_label = "— Talabani tanlang —"
        self.fields['group'].empty_label = "— Guruhni tanlang —"