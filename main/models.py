from django.db import models
from django.core.exceptions import ValidationError
from parler.models import TranslatableModel, TranslatedFields

# Singleton Model Mixin
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"There can be only one {self.__class__.__name__} instance")
        return super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Profile(SingletonModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        bio=models.TextField(),
    )
    profile_picture = models.ImageField(upload_to='profile/', blank=True)
    resume = models.FileField(upload_to='resume/', blank=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Profile"

class ContactInfo(SingletonModel):
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Optional: If address needs translation, we can add it properly
    # For now, keeping it universal as per standard requirements, 
    # but user mentioned "all text fields". Contact info usually is universal 
    # except maybe labels which are handled by gettext.
    # If address is physical and changes by language (rare), we'd need it.
    # Let's assume standard universal contact info for now unless specified.
    
    def __str__(self):
        return "Contact Details"

class Skill(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    proficiency = models.PositiveIntegerField(help_text="1-100")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

class Project(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        description=models.TextField(),
    )
    image = models.ImageField(upload_to='projects/')
    code_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True, verbose_name="Demo Link (Optional)")
    created_date = models.DateField(verbose_name="Creation Date")

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

class Experience(TranslatableModel):
    translations = TranslatedFields(
        job_title=models.CharField(max_length=200),
        company=models.CharField(max_length=200),
        description=models.TextField(),
    )
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date (Leave blank for 'Present')")

    def __str__(self):
        return f"{self.safe_translation_getter('job_title', any_language=True)} at {self.safe_translation_getter('company', any_language=True)}"

class Education(TranslatableModel):
    translations = TranslatedFields(
        degree=models.CharField(max_length=200),
        institution=models.CharField(max_length=200),
    )
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date (Leave blank for 'Present')")

    def __str__(self):
        return f"{self.safe_translation_getter('degree', any_language=True)} at {self.safe_translation_getter('institution', any_language=True)}"

class Hobby(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(),
    )
    icon = models.ImageField(upload_to='hobbies/', blank=True) # Or CharField for font-awesome class

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Your Name")
    role_company = models.CharField(max_length=100, blank=True, verbose_name="Role / Company (Optional)")
    quote = models.TextField(verbose_name="Testimonial")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.name}"
