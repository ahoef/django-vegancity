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

from settings import DEFAULT_CENTER
import models
import search

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VegUserCreationForm(UserCreationForm):
    "Form used for creating new users."
    email_explanation = "VegPhilly is currently under development. We may use your email to contact you ONLY about important changes to your account."
    email = forms.EmailField(max_length=70, label="Email (temporarily required)", 
                             help_text=email_explanation,
                             required=True)
    bio = forms.CharField(label="Bio",
                          help_text="Entering a bio is optional. It will appear to all VegPhilly users along with your username.",
                          required=False,
                          widget=forms.Textarea)
    mailing_list = forms.BooleanField(label="Would you like to join our mailing list?", required=False)
                                      

    def save(self, *args, **kwargs):
        user = super(VegUserCreationForm, self).save(*args, **kwargs)
        user.email = self.cleaned_data['email']
        user_profile = models.UserProfile(user=user)

        user_profile.bio = self.cleaned_data['bio']
        user_profile.mailing_list = self.cleaned_data['mailing_list']
        user_profile.save()
        return user
        
    def clean(self):
        cleaned_data = super(VegUserCreationForm, self).clean()
        username = cleaned_data.get("username", "")

        # TODO: username-specific validation should be stored at the field level.
        # this can be done by adding validators to the field instance(?) at form
        # instantiation time.

        if len(username) < 3:
            raise forms.ValidationError(
                "Your username must be at least three characters.")

        if username != username.lower():
            raise forms.ValidationError(
                "Usernames cannot contain capital letters at this time. Please correct this.")

        return cleaned_data
        

class VegUserEditForm(forms.ModelForm):
    """Form for users to edit their information"""
    
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name',)
        
        
class VegProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('bio', 'mailing_list',)
    
    
##############################
### Vendor Forms
##############################

class AdminVendorForm(forms.ModelForm):

    class Media:
        js = (
            'http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false',
            'http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            'js/vendor_form.js',
            )

    class Meta:
        model = models.Vendor

    def __init__(self, *args, **kwargs):
        super(AdminVendorForm, self).__init__(*args, **kwargs)
        if not self.instance.created:
            self.fields['approval_status'].initial = 'pending'

class NewVendorForm(forms.ModelForm):
    "Form used for adding new vendors."

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            'js/vendor_form.js',
            )

    class Meta:
        model = models.Vendor
        exclude = ('approval_status', 'notes',)
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
                "Can't have both \"Best vegan dish\" and \"Favorite Vegan Dish\". Please choose one.")

        return cleaned_data

    def filter_dishes(self, vendor):
        self.fields['best_vegan_dish'].queryset = vendor.vegan_dishes.all()

    class Meta:
        model = models.Review

class AdminEditReviewForm(_BaseReviewForm):

    def __init__(self, *args, **kwargs):
        super(AdminEditReviewForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.filter_dishes(self.instance.vendor)


class NewReviewForm(_BaseReviewForm):

    def __init__(self, vendor, *args, **kwargs):
        super(NewReviewForm, self).__init__(*args, **kwargs)
        self.filter_dishes(vendor)

    class Meta(_BaseReviewForm.Meta):
        exclude = ('approved', 'author',)
        widgets = {
            'vendor' : forms.HiddenInput,
            }
        


class SearchForm(forms.Form):

    neighborhood = forms.ModelChoiceField(queryset=models.Neighborhood.objects.distinct(),
                                          required=False)
    cuisine = forms.ModelChoiceField(queryset=models.CuisineTag.objects.with_vendors().distinct(),
                                     required=False)
    feature = forms.ModelChoiceField(queryset=models.FeatureTag.objects.with_vendors().distinct(),
                                     required=False)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        # initialize extra values
        self.selected_neighborhood = self.data.get('neighborhood', None)
        self.selected_cuisine = self.data.get('cuisine', None)
        self.selected_feature = self.data.get('feature', None)
        self.query = self.data.get('query', None)
        # TODO: use this later
        self.old_query = self.data.get('old_query', None)
        self.search_type = self.data.get('search_type', None)
        self.vendors = None
        self.has_get_params = (True if self.data else False)
        self.center_latitude, self.center_longitude = DEFAULT_CENTER

        self.checked_feature_filters = []
        for f in models.FeatureTag.objects.with_vendors():
            if self.data.get(f.name) or self.selected_feature == str(f.id):
                self.checked_feature_filters.append(f)

        if self.is_valid():
            self.apply_search()
            self.filter_selections_by_vendors(self.vendors)
        

    def apply_search(self):
        if self.query:
            if self.search_type == 'name':
                self.vendors, _  = search.name_search(self.query, self.get_pre_filtered_vendors())
            elif self.search_type == 'address':
                self.vendors, _  = search.address_search(self.query, self.get_pre_filtered_vendors())
            elif self.search_type == 'tag':
                self.vendors, _  = search.tag_search(self.query, self.get_pre_filtered_vendors())
            else:
                self.vendors, self.search_type = search.master_search(self.query, self.get_pre_filtered_vendors())
        else:
            self.vendors = self.get_pre_filtered_vendors()
    
        # TODO: yikes, I coded myself into a corner here! Fix it!
        if type(self.vendors) == list or type(self.vendors) == set:
            self.vendor_count = len(self.vendors)
        else:
            self.vendor_count = self.vendors.count()

    def filter_selections_by_vendors(self, vendors):
        ids = [vendor.id for vendor in vendors]
        # don't filter these! Causes too many UI bugs!
        # self.fields['neighborhood'].queryset = models.Neighborhood.objects.filter(vendor__in=ids).distinct()
        # self.fields['cuisine'].queryset = models.CuisineTag.objects.filter(vendor__in=ids).distinct()
        self.fields['feature'].queryset = models.FeatureTag.objects.filter(vendor__in=ids).distinct()

    def get_pre_filtered_vendors(self):
        vendors = models.Vendor.approved_objects.all()

        for f in self.checked_feature_filters:
            vendors = vendors.filter(feature_tags__id__exact=f.id)

        if self.selected_neighborhood:
            vendors = vendors.filter(neighborhood__id=self.selected_neighborhood)

        if self.selected_cuisine:
            vendors = vendors.filter(cuisine_tags__id=self.selected_cuisine)

        if self.selected_feature:
            vendors = vendors.filter(feature_tags__id=self.selected_feature)
        return vendors


