from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        # (내가 추가)어떤 필드가 폼에 포함될 것인지에 대한 필드 목록들
