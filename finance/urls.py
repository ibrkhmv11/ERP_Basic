from django.urls import path
from .views import PaymentListView

urlpatterns = [
    path('finance/', PaymentListView.as_view(), name='payment_list'),
]