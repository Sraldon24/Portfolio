from django import forms
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
from .models import ContactMessage, Testimonial

# Length limits for unbounded TextFields (protects against large submission attacks)
MESSAGE_MAX_LENGTH = 5000
QUOTE_MAX_LENGTH = 1000


class ContactForm(forms.ModelForm):
    nickname = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) > MESSAGE_MAX_LENGTH:
            raise forms.ValidationError(
                _('Message must be %(max)s characters or less.') % {'max': MESSAGE_MAX_LENGTH}
            )
        return message


class TestimonialForm(TranslatableModelForm):
    nickname = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    class Meta:
        model = Testimonial
        fields = ['name', 'role_company', 'quote']

    def clean_quote(self):
        quote = self.cleaned_data.get('quote')
        if quote and len(quote) > QUOTE_MAX_LENGTH:
            raise forms.ValidationError(
                _('Testimonial must be %(max)s characters or less.') % {'max': QUOTE_MAX_LENGTH}
            )
        return quote
