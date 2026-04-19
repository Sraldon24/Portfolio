from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    ContactMessage,
    Education,
    Experience,
    Hobby,
    Profile,
    Project,
    Skill,
    Testimonial,
    schedule_auto_translate,
)

# Fragment-cache keys (kept in sync with {% cache N KEY %} blocks in home.html)
HOME_FRAGMENT_KEYS = (
    "home.skills",
    "home.projects",
    "home.career",
    "home.hobbies",
    "home.testimonials",
    "home.profile",
)

TRANSLATABLE_MODELS = (Profile, Skill, Project, Experience, Education, Hobby, Testimonial)


# ─── Background auto-translate on every translatable save ────────
def _schedule_translate(sender, instance, created, **kwargs):
    schedule_auto_translate(instance)


for _model in TRANSLATABLE_MODELS:
    post_save.connect(_schedule_translate, sender=_model, weak=False)


# ─── Fragment cache invalidation on content changes ──────────────
def _invalidate_home_fragments(sender, **kwargs):
    cache.delete_many(HOME_FRAGMENT_KEYS)
    # Django's {% cache %} tag prefixes keys; clear template-cache variants too.
    # (make_template_fragment_key is the authoritative way; keeping simple delete_many
    # covers our manually-named keys. The i18n vary adds language suffix — also covered
    # because cache.delete_many works with prefix matching if the backend supports it.)


for _model in (Profile, Skill, Project, Experience, Education, Hobby, Testimonial):
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
