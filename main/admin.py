from django.contrib import admin
from django.contrib.auth.models import Group, User
from parler.admin import TranslatableAdmin

from .models import (
    ContactInfo,
    ContactMessage,
    Education,
    Experience,
    HeroSlide,
    Hobby,
    Profile,
    Project,
    Recognition,
    SiteSettings,
    Skill,
    TechTag,
    Testimonial,
)

admin.site.unregister(Group)
admin.site.unregister(User)


class SingletonAdminMixin:
    """Mixin to prevent adding more than one instance of a Singleton model."""

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


class HeroSlideInline(admin.TabularInline):
    model = HeroSlide
    extra = 1


@admin.register(Profile)
class ProfileAdmin(SingletonAdminMixin, TranslatableAdmin):
    inlines = [HeroSlideInline]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "bio", "profile_picture", "resume"),
            },
        ),
        (
            "Hero Background",
            {
                "fields": (
                    "hero_bg_type",
                    "hero_static_image",
                    "hero_video_file",
                    "hero_overlay_opacity",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("__str__",)


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "email")


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdminMixin, TranslatableAdmin):
    list_display = ("__str__",)
    fieldsets = (
        (
            "Hero",
            {"fields": ("availability_text", "hero_tagline", "resume_file")},
        ),
        (
            "SEO / Open Graph",
            {"fields": ("og_title", "meta_description")},
        ),
    )


@admin.register(Skill)
class SkillAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("name", "category", "order")
    # NOTE: no list_editable — it suppresses the action "Go" button in Unfold.
    # Edit `order` on each skill's change page instead.
    search_fields = ("translations__name",)
    list_filter = ("category",)
    ordering = ("category", "order")
    fields = ("name", "category", "order")
    actions = [
        "set_category_languages",
        "set_category_frameworks",
        "set_category_infra",
        "set_category_ai_ml",
        "set_category_other",
    ]

    def _bulk_set_category(self, request, queryset, value, label):
        """Bulk-update category. queryset.update() skips post_save, so the
        skills fragment cache is cleared explicitly here."""
        from .signals import _invalidate_home_fragments

        count = queryset.update(category=value)
        _invalidate_home_fragments(Skill)
        self.message_user(request, f"{count} skill(s) set to {label}.")

    @admin.action(description="Set category → Languages")
    def set_category_languages(self, request, queryset):
        self._bulk_set_category(request, queryset, "LANGUAGES", "Languages")

    @admin.action(description="Set category → Frameworks")
    def set_category_frameworks(self, request, queryset):
        self._bulk_set_category(request, queryset, "FRAMEWORKS", "Frameworks")

    @admin.action(description="Set category → Infrastructure")
    def set_category_infra(self, request, queryset):
        self._bulk_set_category(request, queryset, "INFRA", "Infrastructure")

    @admin.action(description="Set category → AI / ML")
    def set_category_ai_ml(self, request, queryset):
        self._bulk_set_category(request, queryset, "AI_ML", "AI / ML")

    @admin.action(description="Set category → Other")
    def set_category_other(self, request, queryset):
        self._bulk_set_category(request, queryset, "OTHER", "Other")


@admin.register(TechTag)
class TechTagAdmin(admin.ModelAdmin):
    show_add_link = True
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("title", "created_date", "description_snippet", "link")
    search_fields = ("translations__title", "translations__description")
    list_filter = ("created_date",)
    filter_horizontal = ("tech_tags",)
    fields = (
        "title",
        "role",
        "description",
        "image",
        "code_link",
        "demo_link",
        "created_date",
        "start_date",
        "end_date",
        "tech_tags",
    )

    def description_snippet(self, obj):
        desc = obj.safe_translation_getter("description", any_language=True)
        return desc[:50] + "..." if desc else ""

    description_snippet.short_description = "Description"

    def link(self, obj):
        return obj.demo_link or obj.code_link or "-"

    link.short_description = "Link"


@admin.register(Experience)
class ExperienceAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("job_title", "company", "role_type", "start_date", "end_date", "is_current")
    search_fields = ("translations__job_title", "translations__company")
    list_filter = ("role_type", "is_current", "start_date")
    ordering = ("-start_date",)
    filter_horizontal = ("tech_used",)
    fields = (
        "job_title",
        "company",
        "role_type",
        "description",
        "start_date",
        "end_date",
        "is_current",
        "tech_used",
        "icon",
    )


@admin.register(Education)
class EducationAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("degree", "institution", "start_date", "end_date")
    search_fields = ("translations__degree", "translations__institution")
    list_filter = ("start_date", "end_date")
    ordering = ("-start_date",)


@admin.register(Recognition)
class RecognitionAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("title", "date_text", "order")
    list_editable = ("order",)
    search_fields = ("translations__title", "translations__description")
    ordering = ("order",)
    fields = ("title", "subtitle", "date_text", "description", "icon_emoji", "order")


@admin.register(Hobby)
class HobbyAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("name", "font_awesome_icon", "icon")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    show_add_link = True
    list_display = ("name", "email", "subject", "message_snippet", "created_at")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)

    def message_snippet(self, obj):
        return obj.message[:50] + "..." if obj.message else ""

    message_snippet.short_description = "Message"


@admin.register(Testimonial)
class TestimonialAdmin(TranslatableAdmin):
    show_add_link = True
    list_display = ("name", "get_role_company", "quote_snippet", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    actions = ["approve_testimonials", "reject_testimonials"]
    search_fields = ("name", "translations__quote", "translations__role_company")

    def get_role_company(self, obj):
        val = obj.safe_translation_getter("role_company", any_language=True)
        return val or ""

    get_role_company.short_description = "Role / Company"

    def quote_snippet(self, obj):
        val = obj.safe_translation_getter("quote", any_language=True)
        return val[:50] + "..." if val else ""

    quote_snippet.short_description = "Quote"

    @admin.action(description="Approve selected testimonials")
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Reject selected testimonials")
    def reject_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
