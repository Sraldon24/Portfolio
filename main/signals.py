from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactMessage, Testimonial


@receiver(post_save, sender=ContactMessage)
def notify_new_message(sender, instance, created, **kwargs):
    """
    Email notifications have been disabled.
    Contact messages are stored in the database and surfaced via the admin UI
    and in-app toast messages only.
    """
    if created:
        # Intentionally do nothing to avoid any email sending / configuration issues.
        return


@receiver(post_save, sender=Testimonial)
def notify_new_testimonial(sender, instance, created, **kwargs):
    """
    Email notifications have been disabled.
    Testimonials are stored in the database and surfaced via the admin UI
    and in-app toast messages only.
    """
    if created:
        # Intentionally do nothing to avoid any email sending / configuration issues.
        return

