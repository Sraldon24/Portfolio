from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage, Testimonial

@receiver(post_save, sender=ContactMessage)
def notify_new_message(sender, instance, created, **kwargs):
    if created:
        pending_testimonials = Testimonial.objects.filter(is_approved=False).count()
        total_messages = ContactMessage.objects.count()
        
        subject = f"New Contact Message from {instance.name}"
        message = (
            f"You have received a new contact message.\n\n"
            f"From: {instance.name} ({instance.email})\n"
            f"Subject: {instance.subject}\n"
            f"Message: {instance.message}\n\n"
            f"--- Stats ---\n"
            f"Pending Testimonials: {pending_testimonials}\n"
            f"Total Messages: {total_messages}"
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin[1] for admin in settings.ADMINS],
            fail_silently=False,
        )

@receiver(post_save, sender=Testimonial)
def notify_new_testimonial(sender, instance, created, **kwargs):
    if created:
        pending_testimonials = Testimonial.objects.filter(is_approved=False).count()
        total_messages = ContactMessage.objects.count()
        
        subject = f"New Testimonial Submitted by {instance.name}"
        message = (
            f"A new testimonial has been submitted for review.\n\n"
            f"From: {instance.name}\n"
            f"Quote: {instance.quote}\n\n"
            f"--- Stats ---\n"
            f"Pending Testimonials: {pending_testimonials}\n"
            f"Total Messages: {total_messages}"
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin[1] for admin in settings.ADMINS],
            fail_silently=False,
        )
