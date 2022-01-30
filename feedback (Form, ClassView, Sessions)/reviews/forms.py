from django import forms
from django.forms import fields
from .models import Review

# class reviewFrom(forms.Form):
#     user_name = forms.CharField(label="Your Name:", max_length=50, error_messages={
#         "required": "your name should not be empty",
#         "max_length": "less Than 50 pleaase"
#     })

#     review_text = forms.CharField(label="Your Review:", widget=forms.Textarea, max_length=200)
#     rating = forms.IntegerField(min_value=1, max_value=5)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ['rating', 'review_text']
        labels = {
            "user_name":"Your Name:",
            "review_text":"Your Feedback:",
            "rating":"Your rating:"
        }
        
        error_messages = {
            "user_name": {
                "required": "Your name must not be empty",
                "max_length":"Don't type more than 200 char"
            }
        }