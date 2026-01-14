from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.contrib.auth.models import Group, User
from .models import Profile, ContactInfo, Skill, Project, Experience, Education, Hobby, ContactMessage, Testimonial

admin.site.unregister(Group)
admin.site.unregister(User)

class SingletonAdminMixin:
    """Mixin to prevent adding more than one instance of a Singleton model."""
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Profile)
class ProfileAdmin(SingletonAdminMixin, TranslatableAdmin):
    list_display = ('__str__',)

@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'email')

@admin.register(Skill)
class SkillAdmin(TranslatableAdmin):
    list_display = ('name', 'proficiency')
    search_fields = ('translations__name',)
    list_filter = ('proficiency',)

@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ('title', 'created_date', 'description_snippet', 'link')
    search_fields = ('translations__title', 'translations__description')
    list_filter = ('created_date',)

    def description_snippet(self, obj):
        desc = obj.safe_translation_getter('description', any_language=True)
        return desc[:50] + '...' if desc else ''
    description_snippet.short_description = 'Description'

    def link(self, obj):
        return obj.demo_link or obj.code_link or '-'
    link.short_description = 'Link'

@admin.register(Experience)
class ExperienceAdmin(TranslatableAdmin):
    list_display = ('job_title', 'company', 'start_date', 'end_date')
    search_fields = ('translations__job_title', 'translations__company')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)

@admin.register(Education)
class EducationAdmin(TranslatableAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date')
    search_fields = ('translations__degree', 'translations__institution')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)

@admin.register(Hobby)
class HobbyAdmin(TranslatableAdmin):
    list_display = ('name',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message_snippet', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)

    def message_snippet(self, obj):
        return obj.message[:50] + '...' if obj.message else ''
    message_snippet.short_description = 'Message'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_company', 'quote_snippet', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_testimonials', 'reject_testimonials']
    search_fields = ('name', 'quote', 'role_company')

    def quote_snippet(self, obj):
        return obj.quote[:50] + '...' if obj.quote else ''
    quote_snippet.short_description = 'Quote'

    @admin.action(description='Approve selected testimonials')
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Reject selected testimonials')
    def reject_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
