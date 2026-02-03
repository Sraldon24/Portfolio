from django import forms
from .models import ContactMessage, Testimonial


class ContactForm(forms.ModelForm):
    nickname = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class TestimonialForm(forms.ModelForm):
    nickname = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    class Meta:
        model = Testimonial
        fields = ['name', 'role_company', 'quote']

