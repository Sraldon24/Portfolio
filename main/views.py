import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm, TestimonialForm
from .models import (
    ContactInfo,
    Education,
    Experience,
    Hobby,
    Profile,
    Project,
    Recognition,
    Skill,
    Testimonial,
)

logger = logging.getLogger(__name__)


@ratelimit(key="ip", rate="5/h", method="POST", block=False)
def home(request):
    contact_form = ContactForm(prefix="contact")
    testimonial_form = TestimonialForm(prefix="testimonial")

    if request.method == "POST":
        if getattr(request, "limited", False):
            messages.error(request, _("Too many submissions. Please try again later."))
            return redirect("home")

        if "submit_contact" in request.POST:
            # Honeypot check FIRST — from raw POST, before form validation
            # (so nothing is persisted for bot submissions).
            if request.POST.get("contact-nickname"):
                return redirect("home")

            contact_form = ContactForm(request.POST, prefix="contact")
            if contact_form.is_valid():
                try:
                    contact_form.save()
                    messages.success(request, _("Your message has been sent successfully!"))
                except Exception:
                    logger.exception("Contact form save failed")
                    messages.error(
                        request,
                        _("Sorry, we couldn't save your message. Please try again in a moment."),
                    )
                return redirect("home")
            else:
                messages.error(
                    request, _("There was an error sending your message. Please check the form.")
                )

        elif "submit_testimonial" in request.POST:
            # Honeypot check FIRST
            if request.POST.get("testimonial-nickname"):
                return redirect("home")

            testimonial_form = TestimonialForm(request.POST, prefix="testimonial")
            if testimonial_form.is_valid():
                try:
                    testimonial_form.save()
                    messages.success(
                        request, _("Thank you! Your testimonial has been submitted for review.")
                    )
                except Exception:
                    logger.exception("Testimonial form save failed")
                    messages.error(
                        request,
                        _(
                            "Sorry, we couldn't save your testimonial. "
                            "Please try again in a moment."
                        ),
                    )
                return redirect("home")
            else:
                messages.error(request, _("There was an error submitting your testimonial."))

    context = {
        "profile": Profile.load(),
        "contact_info": ContactInfo.load(),
        "skills": Skill.objects.prefetch_related("translations"),
        "projects": Project.objects.prefetch_related("translations", "tech_tags").order_by(
            "-created_date"
        ),
        "experiences": Experience.objects.prefetch_related("translations", "tech_used").order_by(
            "-start_date"
        ),
        "educations": Education.objects.prefetch_related("translations").order_by("-start_date"),
        "recognitions": Recognition.objects.prefetch_related("translations").order_by("order"),
        "hobbies": Hobby.objects.prefetch_related("translations"),
        "testimonials": Testimonial.objects.filter(is_approved=True)
        .prefetch_related("translations")
        .order_by("-created_at"),
        "contact_form": contact_form,
        "testimonial_form": testimonial_form,
    }
    return render(request, "main/home.html", context)
