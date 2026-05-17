"""Context processors — inject site-wide objects into every template.

Used so the base template (including 404/500 error pages) can render SEO
meta, the hero CTA, and profile/contact data without each view re-adding it.
"""

from .models import ContactInfo, Profile, SiteSettings


def site_globals(request):
    """Make profile, contact info, and site settings available everywhere."""
    try:
        return {
            "profile": Profile.load(),
            "contact_info": ContactInfo.load(),
            "site_settings": SiteSettings.load(),
        }
    except Exception:
        # During early migrations the tables may not exist yet — fail soft so
        # management commands and error pages still render.
        return {}
