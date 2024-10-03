from django.forms import EmailField
from django import forms
from .models import Mail

class inputform(forms.ModelForm):
    url = EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter any URL....'}))

    class Meta:

        model = Mail
        fields = ['url']                           
