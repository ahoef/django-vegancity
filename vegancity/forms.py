from django import forms

from models import Vendor, Review, VeganDish

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VegUserCreationForm(UserCreationForm):
    "Form used for creating new users."
    email = forms.EmailField(max_length=10, label="Email (optional)", 
                             help_text="for password restoration ONLY.")


class NewVendorForm(forms.ModelForm):
    "Form used for adding new vendors."
    class Meta:
        model = Vendor
        exclude = ('latitude','longitude','approved',)


class ReviewForm(forms.ModelForm):
    """Form for writing a review of a vendor.

    Takes an optional constructor for creating
    a vendor specific review.  This is the standard
    use case."""

    def __init__(self, vendor=None, *args, **kwargs):
        """Add some steps after instantiation

        Follows the normal process of instantiation
        and filters down the list of selectable 'best
        vegan dishes' by vendor.  If there are none,
        the user cannot select a value at all."""
        
        # call the normal constructor
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        if vendor:
            # can select dish if there are elements for vendor
            dishes = VeganDish.objects.filter(vendor=vendor)
            if dishes:
                self.fields['best_vegan_dish'].queryset = dishes
            else:
                self.fields['best_vegan_dish'].widget = forms.HiddenInput()

            # make vendor hidden.
            # TODO: this feels like a hack.
            self.fields['vendor'].widget = forms.HiddenInput()


    class Meta:
        model = Review
        exclude = ('latitude','longitude','approved', 'entered_by')

    
