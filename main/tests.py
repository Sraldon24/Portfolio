from django.test import TestCase, Client
from django.urls import reverse
from django.utils import translation
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import (
    Profile, ContactInfo, Skill, Project, Experience, 
    Education, Hobby, Testimonial, ContactMessage
)
from .forms import ContactForm, TestimonialForm
import datetime
import sys

class ProfileModelTest(TestCase):
    def test_singleton_profile(self):
        # Create first profile
        profile1 = Profile.objects.create(name="Test Profile", bio="Bio")
        self.assertEqual(profile1.pk, 1)
        
        # Try to create second profile (should fail or return same instance depending on implementation, 
        # but our SingletonModel implementation in models.py raises ValidationError on save if exists)
        # However, looking at the code: if not self.pk and self.__class__.objects.exists(): raise ValidationError
        
        from django.core.exceptions import ValidationError
        profile2 = Profile(name="Second Profile", bio="Bio 2")
        with self.assertRaises(ValidationError):
            profile2.save()

    def test_string_representation(self):
        profile = Profile.objects.create(name="Test Name", bio="Test Bio")
        self.assertEqual(str(profile), "Test Name")

class ContactInfoModelTest(TestCase):
    def test_singleton_contact_info(self):
        contact1 = ContactInfo.objects.create(email="test@example.com")
        self.assertEqual(contact1.pk, 1)
        
        from django.core.exceptions import ValidationError
        contact2 = ContactInfo(email="other@example.com")
        with self.assertRaises(ValidationError):
            contact2.save()

    def test_string_representation(self):
        contact = ContactInfo.objects.create(email="test@example.com")
        self.assertEqual(str(contact), "Contact Details")

class TranslatableModelTest(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(name="Python", proficiency=90)
        self.assertEqual(str(skill), "Python")
        
    def test_project_creation(self):
        project = Project.objects.create(
            title="My Project",
            description="Description",
            created_date=datetime.date.today(),
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        )
        self.assertEqual(str(project), "My Project")

    def test_experience_creation(self):
        exp = Experience.objects.create(
            job_title="Developer",
            company="Tech Corp",
            description="Worked hard",
            start_date=datetime.date(2020, 1, 1)
        )
        self.assertEqual(str(exp), "Developer at Tech Corp")

    def test_education_creation(self):
        edu = Education.objects.create(
            degree="BS CS",
            institution="University",
            start_date=datetime.date(2016, 9, 1)
        )
        self.assertEqual(str(edu), "BS CS at University")

    def test_hobby_creation(self):
        hobby = Hobby.objects.create(name="Reading", description="Books")
        self.assertEqual(str(hobby), "Reading")

class StandardModelTest(TestCase):
    def test_contact_message_creation(self):
        msg = ContactMessage.objects.create(
            name="Sender",
            email="sender@example.com",
            subject="Hello",
            message="World"
        )
        self.assertIn("Message from Sender", str(msg))
        self.assertIn("Hello", str(msg))

    def test_testimonial_creation(self):
        testim = Testimonial.objects.create(
            name="Client",
            quote="Great work",
            is_approved=True
        )
        self.assertEqual(str(testim), "Testimonial from Client")

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        translation.activate('en')
        self.url = reverse('home')
        # Setup require data for the view
        self.profile = Profile.objects.create(name="Dev", bio="Bio")
        self.contact = ContactInfo.objects.create(email="dev@example.com")
        self.skill = Skill.objects.create(name="Django", proficiency=100)
        self.project = Project.objects.create(
            title="Portfolio", 
            description="This site", 
            created_date=datetime.date.today(),
            image=SimpleUploadedFile("img.jpg", b"img", content_type="image/jpeg")
        )

    def test_home_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        self.assertContains(response, "Dev")
        self.assertContains(response, "Django")
        self.assertContains(response, "Portfolio")

    def test_contact_form_submission(self):
        data = {
            'submit_contact': '1',
            'contact-name': 'User',
            'contact-email': 'user@example.com',
            'contact-subject': 'Hi',
            'contact-message': 'Test msg'
        }
        response = self.client.post(self.url, data)
        # Should redirect back to home on success
        self.assertRedirects(response, self.url)
        
        # Verify message created
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().name, 'User')

    def test_testimonial_form_submission(self):
        data = {
            'submit_testimonial': '1',
            'testimonial-name': 'Happy Client',
            'testimonial-role_company': 'CEO',
            'testimonial-quote': 'Awesome!'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        
        self.assertEqual(Testimonial.objects.count(), 1)
        self.assertEqual(Testimonial.objects.first().name, 'Happy Client')

    def test_invalid_contact_form(self):
        # Missing required email
        data = {
            'submit_contact': '1',
            'contact-name': 'User',
            'contact-message': 'Test'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200) # Re-renders page with errors
        # Since we use django messages, we check for error message
        messages = list(response.context['messages'])
        self.assertTrue(any("error" in str(m) for m in messages))
        self.assertEqual(ContactMessage.objects.count(), 0)

