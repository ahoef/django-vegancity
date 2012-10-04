from django import forms

from models import Vendor

from django.contrib.auth.forms import UserCreationForm

class VegUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=10, label="Email (optional)", 
                             help_text="for password restoration ONLY.")


class NewVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ('latitude','longitude','approved',)
