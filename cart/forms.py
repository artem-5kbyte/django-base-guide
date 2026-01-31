from django import forms

class CartAddProductForm(forms.Form):
    # Для того щоб вписати кількість товару
    quantity = forms.IntegerField(min_value=1, max_value=30, initial=1, widget = forms.NumberInput(attrs={'class': 'form-control'}))
    # Ключ для cart.py
    override = forms.BooleanField(required=False, initial=False, widget = forms.HiddenInput())


