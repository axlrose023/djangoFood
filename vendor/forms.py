from django import forms

from accounts.validators import allow_only_images_validator
from vendor.models import Vendor, OpeningHour


class VendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}),
                                      validators=[allow_only_images_validator])

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
