import contextlib
import logging
import sys
import threading

from deep_translator import GoogleTranslator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from parler.models import TranslatableModel, TranslatedFields

logger = logging.getLogger(__name__)

# Background threads racing SQLite during tests cause "database is locked"
# errors. Skip scheduling when running the test suite.
_RUNNING_TESTS = "test" in sys.argv or getattr(settings, "TESTING", False)


def _do_auto_translate(instance):
    """
    Core EN->FR translation. Runs off the request thread — NEVER call from save().
    Only triggers when current language is EN and FR translation is missing.
    """
    try:
        if instance.get_current_language() != "en":
            return
        if instance.has_translation("fr"):
            return

        translator = GoogleTranslator(source="en", target="fr")
        en_trans = instance.get_translation("en")

        instance.set_current_language("fr")
        for field in instance._parler_meta.get_translated_fields():
            value = getattr(en_trans, field, None)
            if value and isinstance(value, str):
                try:
                    translated_value = translator.translate(value)
                    setattr(instance, field, translated_value)
                except Exception:
                    logger.exception("Translation failed for field %s", field)
        # Persist the FR translation without triggering the auto-translate loop again
        # (guarded by has_translation("fr") above on re-entry).
        try:
            instance.save_translations()
        except Exception:
            logger.exception("save_translations failed on %s", instance)
        instance.set_current_language("en")
    except Exception:
        logger.exception("Auto-translation error")
        with contextlib.suppress(Exception):
            instance.set_current_language("en")


def schedule_auto_translate(instance):
    """Fire-and-forget background translation so form.save() returns immediately."""
    if _RUNNING_TESTS:
        return
    t = threading.Thread(target=_do_auto_translate, args=(instance,), daemon=True)
    t.start()


# Singleton Model Mixin
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"There can be only one {self.__class__.__name__} instance")
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if not obj.has_translation("en"):
            obj.set_current_language("en")
            obj.name = "Your Name"
            obj.bio = "Welcome to my portfolio."
            obj.save()
        return obj


class Profile(SingletonModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        bio=models.TextField(blank=True),
    )
    profile_picture = models.ImageField(upload_to="profile/", blank=True, null=True)
    resume = models.FileField(upload_to="resume/", blank=True)

    # Background Settings
    HERO_BG_CHOICES = [
        ("GRADIENT", "Gradient (Default)"),
        ("IMAGE", "Static Image"),
        ("VIDEO", "Video"),
        ("SLIDESHOW", "Slideshow"),
    ]
    hero_bg_type = models.CharField(
        max_length=20,
        choices=HERO_BG_CHOICES,
        default="GRADIENT",
        verbose_name="Hero Background Type",
    )
    hero_static_image = models.ImageField(
        upload_to="hero/static/", blank=True, null=True, verbose_name="Static Hero Image"
    )
    hero_video_file = models.FileField(
        upload_to="hero/video/", blank=True, null=True, verbose_name="Hero Video (MP4/WebM)"
    )
    hero_overlay_opacity = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.5,
        help_text="Overlay opacity (0.0 to 1.0). Higher = darker.",
    )

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or "Profile"


class HeroSlide(models.Model):
    profile = models.ForeignKey(Profile, related_name="hero_slides", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hero/slides/")
    caption = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Slide {self.order} for {self.profile}"


class ContactInfo(SingletonModel):
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, defaults={"email": "contact@example.com"})
        if not obj.email:
            obj.email = "contact@example.com"
            obj.save()
        return obj

    def __str__(self):
        return "Contact Details"


class Skill(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    proficiency = models.PositiveIntegerField(help_text="1-100")

    class Meta:
        ordering = ["-proficiency"]

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class Project(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        description=models.TextField(blank=True),
    )
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    code_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True, verbose_name="Demo Link (Optional)")
    created_date = models.DateField(verbose_name="Creation Date", db_index=True)
    tech_stack = models.CharField(
        max_length=300,
        blank=True,
        default="",
        help_text="Comma-separated tags e.g. Python, Django, Docker",
    )

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)


class Experience(TranslatableModel):
    translations = TranslatedFields(
        job_title=models.CharField(max_length=200),
        company=models.CharField(max_length=200),
        description=models.TextField(blank=True),
    )
    start_date = models.DateField(verbose_name="Start Date", db_index=True)
    end_date = models.DateField(
        null=True, blank=True, verbose_name="End Date (Leave blank for 'Present')"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default="",
        choices=[
            ("fa-solid fa-briefcase", "Briefcase"),
            ("fa-solid fa-building", "Building"),
            ("fa-solid fa-laptop-code", "Laptop Code"),
            ("fa-solid fa-code", "Code"),
            ("fa-solid fa-microchip", "Microchip"),
            ("fa-solid fa-server", "Server"),
            ("fa-solid fa-database", "Database"),
            ("fa-solid fa-desktop", "Desktop"),
            ("fa-solid fa-user-tie", "User Tie"),
            ("fa-solid fa-handshake", "Handshake"),
            ("fa-solid fa-chart-line", "Chart Line"),
            ("fa-solid fa-pen-nib", "Pen Nib"),
        ],
        help_text="Select a built-in icon",
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.safe_translation_getter('job_title', any_language=True)} at {self.safe_translation_getter('company', any_language=True)}"


class Education(TranslatableModel):
    translations = TranslatedFields(
        degree=models.CharField(max_length=200),
        institution=models.CharField(max_length=200),
    )
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(
        null=True, blank=True, verbose_name="End Date (Leave blank for 'Present')"
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.safe_translation_getter('degree', any_language=True)} at {self.safe_translation_getter('institution', any_language=True)}"


class Hobby(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(blank=True),
    )
    icon = models.ImageField(
        upload_to="hobbies/",
        blank=True,
        help_text="Upload custom icon/image (optional if built-in selected)",
    )
    font_awesome_icon = models.CharField(
        max_length=50,
        blank=True,
        default="",
        choices=[
            ("fa-solid fa-gamepad", "Gamepad"),
            ("fa-solid fa-music", "Music"),
            ("fa-solid fa-book", "Book"),
            ("fa-solid fa-camera", "Camera"),
            ("fa-solid fa-plane", "Plane"),
            ("fa-solid fa-bicycle", "Bicycle"),
            ("fa-solid fa-palette", "Palette"),
            ("fa-solid fa-utensils", "Utensils"),
            ("fa-solid fa-film", "Film"),
            ("fa-solid fa-basketball", "Basketball"),
            ("fa-solid fa-futbol", "Soccer"),
            ("fa-solid fa-dumbbell", "Dumbbell"),
            ("fa-solid fa-campground", "Camping"),
            ("fa-solid fa-code", "Code"),
            ("fa-solid fa-chess", "Chess"),
            ("fa-solid fa-guitar", "Guitar"),
            ("fa-solid fa-running", "Running"),
            ("fa-solid fa-swimmer", "Swimming"),
        ],
        help_text="Select a built-in icon (overrides custom image if set)",
    )

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"


class Testimonial(TranslatableModel):
    name = models.CharField(max_length=100, verbose_name="Your Name")

    translations = TranslatedFields(
        role_company=models.CharField(
            max_length=100, blank=True, verbose_name="Role / Company (Optional)"
        ),
        quote=models.TextField(verbose_name="Testimonial"),
    )

    is_approved = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_approved", "-created_at"])]

    def __str__(self):
        return f"Testimonial from {self.name}"
