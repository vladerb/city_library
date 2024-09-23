from django import forms
from django.utils.text import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# from .models import Tag, Contact

# Rating
class RatingForm(forms.Form):
    RATING_CHOICES = [(i, str(i)) for i in range(5, 0, -1)]
    score = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect(attrs={'class': 'radio_1'}), label='Score')