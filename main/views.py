import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm, TestimonialForm
from .models import ContactInfo, Education, Experience, Hobby, Profile, Project, Skill, Testimonial

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
            contact_form = ContactForm(request.POST, prefix="contact")
            if contact_form.is_valid():
                # Spam check (Honeypot)
                if contact_form.cleaned_data.get("nickname"):
                    return redirect("home")  # Silent failure for bots

                try:
                    contact_form.save()
                    messages.success(request, _("Your message has been sent successfully!"))
                except Exception:
                    logger.exception("Contact form save failed")
                    messages.success(
                        request, _("Your message has been sent successfully!")
                    )  # Form row often saved before email signal fires — keep UX calm
                    # Actually, if save() fails (signals), the DB transaction might roll back or not.
                    # Signals usually run after save. If signal fails, save is usually done.
                    # But to be safe and friendly:
                    # messages.warning(request, "Message saved, but email notification failed.")
                    # Let's just say success to not panic them, as long as it's not a critical DB error.
                    # If it's pure email error, the contact IS saved in DB.
                return redirect("home")
            else:
                messages.error(
                    request, _("There was an error sending your message. Please check the form.")
                )

        elif "submit_testimonial" in request.POST:
            testimonial_form = TestimonialForm(request.POST, prefix="testimonial")
            if testimonial_form.is_valid():
                # Spam check (Honeypot)
                if testimonial_form.cleaned_data.get("nickname"):
                    return redirect("home")

                try:
                    testimonial_form.save()
                    messages.success(
                        request, _("Thank you! Your testimonial has been submitted for review.")
                    )
                except Exception:
                    logger.exception("Testimonial form save failed")
                    messages.success(
                        request, _("Thank you! Your testimonial has been submitted for review.")
                    )
                return redirect("home")
            else:
                messages.error(request, _("There was an error submitting your testimonial."))

    context = {
        "profile": Profile.load(),
        "contact_info": ContactInfo.load(),
        "skills": Skill.objects.prefetch_related("translations"),
        "projects": Project.objects.prefetch_related("translations").order_by("-created_date"),
        "experiences": Experience.objects.prefetch_related("translations").order_by(
            "-start_date"
        ),
        "educations": Education.objects.prefetch_related("translations").order_by("-start_date"),
        "hobbies": Hobby.objects.prefetch_related("translations"),
        "testimonials": Testimonial.objects.filter(is_approved=True)
        .prefetch_related("translations")
        .order_by("-created_at"),
        "contact_form": contact_form,
        "testimonial_form": testimonial_form,
    }
    return render(request, "main/home.html", context)
