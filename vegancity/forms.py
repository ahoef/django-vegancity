# Copyright (C) 2012 Steve Lamb

# This file is part of Vegancity.

# Vegancity is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Vegancity is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Vegancity.  If not, see <http://www.gnu.org/licenses/>.


from django import forms

from models import Vendor, Review, VeganDish

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VegUserCreationForm(UserCreationForm):
    "Form used for creating new users."
    email = forms.EmailField(max_length=10, label="Email (optional)", 
                             help_text="for password restoration ONLY.",
                             required=False)


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

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        chose_best = cleaned_data.get("best_vegan_dish")
        entered_unlisted = cleaned_data.get("unlisted_vegan_dish")

        if chose_best and entered_unlisted:
            raise forms.ValidationError(
                "can't have both \"Best vegan dish\" and \"Favorite Vegan Dish\". Please choose one.")

        return cleaned_data


    class Meta:
        model = Review
        exclude = ('latitude','longitude','approved', 'author')

    
