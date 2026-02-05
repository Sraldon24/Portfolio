from django import template
from main.models import Testimonial, ContactMessage

register = template.Library()

# Functions used by Unfold (settings.py)
def pending_testimonials_count(request):
    return Testimonial.objects.filter(is_approved=False).count()

def total_messages_count(request):
    return ContactMessage.objects.count()

# Template tag used by admin/base_site.html
@register.simple_tag
def get_pending_counts():
    """
    Returns the count of pending items (currently only unapproved testimonials).
    This is used in the admin sidebar or header to show notification badges.
    """
    return Testimonial.objects.filter(is_approved=False).count()
