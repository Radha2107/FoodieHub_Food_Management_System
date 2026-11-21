from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Name for delivery"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "10-digit phone number"}))
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "placeholder": "House no., street, area, city"}))
    payment_method = forms.ChoiceField(choices=[("Cash on Delivery", "Cash on Delivery")])
