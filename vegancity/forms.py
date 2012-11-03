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

import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VegUserCreationForm(UserCreationForm):
    "Form used for creating new users."
    email = forms.EmailField(max_length=70, label="Email (STRONGLY recommended)", 
                             help_text="for password restoration ONLY.",
                             required=False)

    def save(self, *args, **kwargs):
        user = super(VegUserCreationForm, self).save(*args, **kwargs)
        user.email = self.cleaned_data['email']
        if kwargs.get('commit', False):
            user.save()
        return user
        
    def clean(self):
        cleaned_data = super(VegUserCreationForm, self).clean()
        username = cleaned_data.get("username", "")

        # TODO: username-specific validation should be stored at the field level.
        # this can be done by adding validators to the field instance(?) at form
        # instantiation time.

        if len(username) < 3:
            raise forms.ValidationError(
                "Username must be at least 3 characters.")

            
        if username != username.lower():
            raise forms.ValidationError(
                "Cannot have capital letters in username at this time. Please correct.")

        return cleaned_data
        

##############################
### Vendor Forms
##############################

class _BaseVendorForm(forms.ModelForm):

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            'js/vendor_form.js',
            )

    class Meta:
        model = models.Vendor

class AdminVendorForm(_BaseVendorForm):

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            'http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false',
            'js/vendor_form.js',
            )

    def __init__(self, *args, **kwargs):
        super(AdminVendorForm, self).__init__(*args, **kwargs)
        if not self.instance.created:
            self.fields['approved'].initial = True

class NewVendorForm(_BaseVendorForm):
    "Form used for adding new vendors."

    class Meta(_BaseVendorForm.Meta):
        exclude = ('approved',)
        widgets = {
            'cuisine_tags' : forms.CheckboxSelectMultiple,
            'feature_tags' : forms.CheckboxSelectMultiple,
            }

##############################
### Review Forms
##############################

class _BaseReviewForm(forms.ModelForm):
    """Base Class for making Review forms.

    This class should not be instantiated directly."""

    def clean(self):
        cleaned_data = super(_BaseReviewForm, self).clean()
        chose_best = cleaned_data.get("best_vegan_dish")
        entered_unlisted = cleaned_data.get("unlisted_vegan_dish")

        if chose_best and entered_unlisted:
            raise forms.ValidationError(
                "can't have both \"Best vegan dish\" and \"Favorite Vegan Dish\". Please choose one.")

        return cleaned_data

    def filter_dishes(self, vendor):
        dishes = models.VeganDish.objects.filter(vendor=vendor)
        if dishes:
            self.fields['best_vegan_dish'].queryset = dishes
        else:
            self.fields['best_vegan_dish'].widget = forms.HiddenInput()

    class Meta:
        model = models.Review

class AdminEditReviewForm(_BaseReviewForm):

    def __init__(self, *args, **kwargs):
        super(AdminEditReviewForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.filter_dishes(self.instance.vendor)


class NewReviewForm(_BaseReviewForm):

    def __init__(self, vendor, *args, **kwargs):
        super(NewReviewForm, self).__init__(*args, **kwargs)
        self.filter_dishes(vendor)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            'js/review_form.js',
            )


    class Meta(_BaseReviewForm.Meta):
        exclude = ('approved', 'author',)
        widgets = {
            'vendor' : forms.HiddenInput,
            }
        
