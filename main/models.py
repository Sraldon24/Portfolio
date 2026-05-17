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


class SiteSettings(SingletonModel, TranslatableModel):
    """Singleton for site-wide editable copy — hero CTA, tagline, SEO, resume."""

    translations = TranslatedFields(
        availability_text=models.CharField(
            max_length=120,
            default="Available for Summer 2026 internships",
            help_text="Shown in the hero status badge and contact section.",
        ),
        hero_tagline=models.CharField(
            max_length=200,
            blank=True,
            help_text='Subheadline under your name, e.g. "AI Research Intern at '
            'Polytechnique • Incoming SWE at Concordia".',
        ),
        meta_description=models.CharField(
            max_length=300,
            blank=True,
            help_text="SEO meta description + Open Graph description for this language.",
        ),
        og_title=models.CharField(
            max_length=120,
            blank=True,
            help_text="Open Graph / browser tab title. Falls back to name + role if blank.",
        ),
    )
    resume_file = models.FileField(
        upload_to="resume/",
        blank=True,
        help_text="The resume PDF offered for download. Replaceable here without code changes.",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        if not obj.has_translation("en"):
            obj.set_current_language("en")
            obj.availability_text = "Available for Summer 2026 internships"
            obj.save()
        return obj

    def __str__(self):
        return "Site Settings"


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
    CATEGORY_CHOICES = [
        ("LANGUAGES", "Languages"),
        ("FRAMEWORKS", "Frameworks"),
        ("INFRA", "Infrastructure"),
        ("AI_ML", "AI / ML"),
        ("OTHER", "Other"),
    ]

    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="OTHER",
        db_index=True,
        help_text="Group this skill renders under.",
    )
    order = models.IntegerField(
        default=0,
        help_text="Manual sort order within the category (low numbers first).",
    )
    # Deprecated: skills now render as categorized chips, not percentage bars.
    # Kept nullable for backwards compatibility and reversible migrations.
    proficiency = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Deprecated — no longer displayed. Left for backwards compatibility.",
    )

    class Meta:
        ordering = ["category", "order"]

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class TechTag(models.Model):
    """A reusable technology tag — shared by Projects and Experience entries."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        description=models.TextField(blank=True),
        role=models.CharField(
            max_length=120,
            blank=True,
            help_text='Optional, e.g. "Transactions Domain Lead".',
        ),
    )
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    code_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True, verbose_name="Demo Link (Optional)")
    created_date = models.DateField(verbose_name="Creation Date", db_index=True)
    start_date = models.CharField(
        max_length=20,
        blank=True,
        help_text='Free text, e.g. "2025". Optional.',
    )
    end_date = models.CharField(
        max_length=20,
        blank=True,
        help_text='Free text, e.g. "2026" or "Present". Optional.',
    )
    tech_tags = models.ManyToManyField(TechTag, blank=True, related_name="projects")
    # Deprecated: superseded by tech_tags M2M. Kept for backwards compatibility.
    tech_stack = models.CharField(
        max_length=300,
        blank=True,
        default="",
        help_text="Deprecated — use Tech tags instead. Comma-separated legacy field.",
    )

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)

    @property
    def date_range(self):
        """Display string from start/end_date — '2025 → 2026', '2026', or ''."""
        start = (self.start_date or "").strip()
        end = (self.end_date or "").strip()
        if start and end:
            return f"{start} → {end}"
        return start or end


class Experience(TranslatableModel):
    ROLE_TYPE_CHOICES = [
        ("INTERNSHIP", "Internship"),
        ("PART_TIME", "Part-time"),
        ("FULL_TIME", "Full-time"),
        ("TUTORING", "Tutoring"),
        ("RESEARCH", "Research"),
        ("VOLUNTEER", "Volunteer"),
        ("EDUCATION", "Education"),
    ]

    translations = TranslatedFields(
        job_title=models.CharField(max_length=200),
        company=models.CharField(max_length=200),
        description=models.TextField(
            blank=True,
            help_text="Supports Markdown — use '- ' lines for bullet points.",
        ),
    )
    role_type = models.CharField(
        max_length=20,
        choices=ROLE_TYPE_CHOICES,
        blank=True,
        help_text="Shown as a small badge next to the title.",
    )
    is_current = models.BooleanField(
        default=False,
        help_text="If checked, the end date shows '→ Present' automatically.",
    )
    tech_used = models.ManyToManyField("TechTag", blank=True, related_name="experiences")
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


class Recognition(TranslatableModel):
    """Awards, honors, scholarships, hackathon placements — the awards.log section."""

    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        subtitle=models.CharField(max_length=200, blank=True),
        description=models.TextField(blank=True),
    )
    date_text = models.CharField(
        max_length=60,
        blank=True,
        help_text='Free text, e.g. "November 2025" or "Fall 2025".',
    )
    icon_emoji = models.CharField(
        max_length=8,
        blank=True,
        help_text='Optional emoji, e.g. "🏆".',
    )
    order = models.IntegerField(default=0, help_text="Manual sort order (low numbers first).")

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Recognitions"

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or "Recognition"


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
