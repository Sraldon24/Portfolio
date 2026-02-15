import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_core.settings')
django.setup()

from main.models import Profile, Project, Skill, Experience, Education, Testimonial

def add_translations():
    # Profile
    try:
        profile = Profile.objects.first()
        if profile:
            profile.set_current_language('fr')
            profile.name = "Amir Sraldon"  # Assuming same name
            profile.bio = "Je suis un développeur passionné avec de l'expérience dans la création d'applications web modernes."
            profile.save()
            print("Profile translated.")
    except Exception as e:
        print(f"Error translating profile: {e}")

    # Skills - assuming some exist, we'll just translate a few common ones if found or generic
    skills = Skill.objects.all()
    for skill in skills:
        skill.set_current_language('fr')
        # Simple heuristic or just same name valid for many tech skills
        if skill.name.lower() == 'python':
            skill.name = 'Python'
        elif skill.name.lower() == 'javascript':
            skill.name = 'JavaScript'
        else:
             skill.name = skill.safe_translation_getter('name', language_code='en') or skill.name
        skill.save()
    print(f"Translated {skills.count()} skills (mostly keeps same name).")

    # Projects
    projects = Project.objects.all()
    for project in projects:
        project.set_current_language('fr')
        project.title = f"{project.safe_translation_getter('title', language_code='en')} (FR)"
        project.description = f"Ceci est la description française pour {project.safe_translation_getter('title', language_code='en')}."
        project.save()
    print(f"Translated {projects.count()} projects.")

    # Experience
    experiences = Experience.objects.all()
    for exp in experiences:
        exp.set_current_language('fr')
        exp.job_title = f"{exp.safe_translation_getter('job_title', language_code='en')} (FR)"
        exp.company = exp.safe_translation_getter('company', language_code='en')
        exp.description = "Description du poste en français."
        exp.save()
    print(f"Translated {experiences.count()} experiences.")

    # Education
    educations = Education.objects.all()
    for edu in educations:
        edu.set_current_language('fr')
        edu.degree = f"{edu.safe_translation_getter('degree', language_code='en')} (FR)"
        edu.institution = edu.safe_translation_getter('institution', language_code='en')
        edu.save()
    print(f"Translated {educations.count()} educations.")
    
    # Testimonials
    testimonials = Testimonial.objects.all()
    for testimonial in testimonials:
        testimonial.set_current_language('fr')
        # Use existing English content as source if not present?
        # Ideally the model's save method handles auto-translation if set up correctly,
        # but here we are forcing it for existing records.
        # The auto_translate_fields function we saw earlier relies on Google Translator.
        # We can trigger a save which should call auto_translate_fields if we are saving in 'fr' 
        # but the logic there checks for 'en' source.
        # Let's just manually call the same logic or just save() and let the model handle it if we switch to EN then save?
        # Actually, let's look at the model save override: 
        # if instance.get_current_language() != 'en': return
        # So it only auto-translates when saving EN.
        
        # So we should iterate, set language to EN, save (to trigger auto translate to FR if missing).
        # But wait, the auto_translate_fields checks if FR exists.
        
        # Strategy: Ensure EN content is there (it is), then save.
        testimonial.set_current_language('en')
        testimonial.save() 
        # The save() method calls auto_translate_fields(self), which checks if FR is missing, 
        # and if so, translates from EN to FR.
    
    print(f"Refreshed {testimonials.count()} testimonials (triggering auto-translation).")

if __name__ == "__main__":
    add_translations()
