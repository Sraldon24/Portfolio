from django import template
from main.models import Testimonial

register = template.Library()

@register.simple_tag
def get_pending_counts():
    """
    Returns the count of pending items (currently only unapproved testimonials).
    This is used in the admin sidebar or header to show notification badges.
    """
    return Testimonial.objects.filter(is_approved=False).count()
