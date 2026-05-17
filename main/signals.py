from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    ContactMessage,
    Education,
    Experience,
    Hobby,
    Profile,
    Project,
    Recognition,
    SiteSettings,
    Skill,
    Testimonial,
    schedule_auto_translate,
)

# Fragment-cache fragment names — kept in sync with {% cache N "name" LANGUAGE_CODE %}
# blocks in home.html. Each {% cache %} block varies on LANGUAGE_CODE, so the real
# cache key is derived per language via make_template_fragment_key().
HOME_FRAGMENT_NAMES = (
    "home.skills",
    "home.recognitions",
    "home.projects",
    "home.career",
    "home.hobbies",
    "home.testimonials",
)

# Languages the {% cache %} blocks can be rendered under.
_LANGUAGES = ("en", "fr")

TRANSLATABLE_MODELS = (
    Profile,
    SiteSettings,
    Skill,
    Project,
    Experience,
    Education,
    Hobby,
    Recognition,
    Testimonial,
)


# ─── Background auto-translate on every translatable save ────────
def _schedule_translate(sender, instance, created, **kwargs):
    schedule_auto_translate(instance)


for _model in TRANSLATABLE_MODELS:
    post_save.connect(_schedule_translate, sender=_model, weak=False)


# ─── Fragment cache invalidation on content changes ──────────────
def _invalidate_home_fragments(sender, **kwargs):
    """Delete every per-language {% cache %} fragment on the home page.

    {% cache %} keys are hashed by Django (make_template_fragment_key), so the
    raw fragment name never matches the stored key. We must reconstruct the key
    for each (fragment name, language) pair — a plain delete_many of the names
    silently does nothing.
    """
    keys = [
        make_template_fragment_key(name, [lang])
        for name in HOME_FRAGMENT_NAMES
        for lang in _LANGUAGES
    ]
    cache.delete_many(keys)


for _model in TRANSLATABLE_MODELS:
    post_save.connect(_invalidate_home_fragments, sender=_model, weak=False)
    post_delete.connect(_invalidate_home_fragments, sender=_model, weak=False)


@receiver(post_save, sender=ContactMessage)
def notify_new_message(sender, instance, created, **kwargs):
    """Placeholder — email notifications disabled; surfaced via admin only."""
    if created:
        return


@receiver(post_save, sender=Testimonial)
def notify_new_testimonial(sender, instance, created, **kwargs):
    """Placeholder — email notifications disabled; surfaced via admin only."""
    if created:
        return
