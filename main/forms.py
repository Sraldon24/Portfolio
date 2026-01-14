from django import forms
from .models import ContactMessage, Testimonial

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role_company', 'quote']
