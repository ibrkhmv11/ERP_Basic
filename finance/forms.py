from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'group', 'amount', 'payment_type']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 500000'}),
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
        }