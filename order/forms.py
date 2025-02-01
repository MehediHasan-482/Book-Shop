from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    DIVISION_CHOICES = (
        ('Dhaka', 'Dhaka'),
        ('Chattagram', 'Chattagram'),
        ('Rajshahi', 'Rajshahi '),
    )

    DISCRICT_CHOICES = (
        ('Dhaka', 'Dhaka'), 
        ('Gazipur', 'Gazipur'),
        ('Narayanganj', 'Narayanganj'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('Rocket', 'Rocket'),
        ('Bkash','Bkash')
    )

    division = forms.ChoiceField(choices=DIVISION_CHOICES)
    district =  forms.ChoiceField(choices=DISCRICT_CHOICES)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())

    # Add placeholders to the fields
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zip code'}))
    account_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Account number'}))
    transaction_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Transaction ID'}))

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'division', 'district', 'zip_code', 'payment_method', 'account_no', 'transaction_id']

