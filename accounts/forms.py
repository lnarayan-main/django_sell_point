from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=False,
        widget=forms.Select()
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    # profile_pic = forms.ImageField(required=False)
    # cover_pic = forms.ImageField(required=False)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    zipcode = forms.CharField(max_length=10, required=False, label="Zip Code")
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = UserProfile
        fields = ['dob', 'address', 'city', 'state', 'country', 'zipcode', 'gender', 'phone_number']



class UserProfileFormWithPic(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=False,
        widget=forms.Select()
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    profile_pic = forms.ImageField(required=False)
    # cover_pic = forms.ImageField(required=False)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    zipcode = forms.CharField(max_length=10, required=False, label="Zip Code")
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = UserProfile
        fields = ['dob', 'address', 'profile_pic', 'city', 'state', 'country', 'zipcode', 'gender', 'phone_number']
