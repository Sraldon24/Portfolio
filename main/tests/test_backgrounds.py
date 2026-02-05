from django.test import TestCase, RequestFactory
from main.models import Profile, HeroSlide
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string

class DynamicBackgroundTest(TestCase):

    def setUp(self):
        # Create Profile using Parler's API just to be safe, 
        # or standard create + attribute setting if TranslatableModel is standard.
        # Parler models usually work with .create() if using the manager, 
        # but let's be explicit to avoid "name" field errors since it's translated.
        self.profile = Profile.objects.create()
        self.profile.set_current_language('en')
        self.profile.name = "Test Profile"
        self.profile.save()

    def test_gradient_rendering(self):
        """Test the default gradient background."""
        self.profile.hero_bg_type = 'GRADIENT'
        self.profile.save()
        
        # Render template
        # We need to pass 'profile' in context because home.html expects it.
        # Assuming the view passes 'profile' context variable.
        html = render_to_string('main/home.html', {'profile': self.profile})
        
        self.assertIn("bg-blue-500/10", html)
        self.assertIn("bg-emerald-500/10", html)

    def test_image_background(self):
        """Test rendering a static image."""
        self.profile.hero_bg_type = 'IMAGE'
        self.profile.hero_static_image = SimpleUploadedFile(
            name='test_image.jpg', 
            content=b'fakeimagecontent', 
            content_type='image/jpeg'
        )
        self.profile.save()

        html = render_to_string('main/home.html', {'profile': self.profile})
        
        self.assertIn("background-image: url", html)
        self.assertIn(self.profile.hero_static_image.url, html)
        self.assertIn('style="opacity: 0.5;"', html) # Check default overlay

    def test_video_background(self):
        """Test rendering video background."""
        self.profile.hero_bg_type = 'VIDEO'
        self.profile.hero_video_file = SimpleUploadedFile(
            name='test.mp4',
            content=b'fakevideo',
            content_type='video/mp4'
        )
        self.profile.save()

        html = render_to_string('main/home.html', {'profile': self.profile})
        
        self.assertIn("<video", html)
        self.assertIn(self.profile.hero_video_file.url, html)

    def test_slideshow_background(self):
        """Test slideshow rendering."""
        self.profile.hero_bg_type = 'SLIDESHOW'
        self.profile.save()

        # Add Slides
        slide1 = HeroSlide.objects.create(
            profile=self.profile,
            order=1,
            image=SimpleUploadedFile('s1.jpg', b'contents', 'image/jpeg')
        )
        slide2 = HeroSlide.objects.create(
            profile=self.profile,
            order=2,
            image=SimpleUploadedFile('s2.jpg', b'contents', 'image/jpeg')
        )

        html = render_to_string('main/home.html', {'profile': self.profile})

        self.assertIn("slideshow-container", html)
        self.assertIn(slide1.image.url, html)
        self.assertIn(slide2.image.url, html)
        self.assertIn("Slideshow Logic", html)
