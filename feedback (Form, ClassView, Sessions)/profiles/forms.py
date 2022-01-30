from django import forms

class ProfileForm(forms.Form):
    user_profile = forms.ImageField()