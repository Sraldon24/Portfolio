from django import template
from main.models import Testimonial, ContactMessage

register = template.Library()

def pending_testimonials_count(request):
    return Testimonial.objects.filter(is_approved=False).count()

def total_messages_count(request):
    return ContactMessage.objects.count()
