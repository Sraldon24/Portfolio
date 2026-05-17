"""Attach a cover image to a project, matched by English title.

Usage:  python manage.py set_project_image "VerifIA" /path/to/image.jpg
"""

from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from main.models import Project


class Command(BaseCommand):
    help = "Set a project's cover image (matched by English title)."

    def add_arguments(self, parser):
        parser.add_argument("title", help="English title of the project.")
        parser.add_argument("image_path", help="Local path to the image file.")

    def handle(self, *args, **options):
        title = options["title"]
        image_path = Path(options["image_path"])
        if not image_path.is_file():
            raise CommandError(f"Image not found: {image_path}")

        project = Project.objects.filter(translations__title=title).first()
        if not project:
            raise CommandError(f"No project with title '{title}'.")

        with image_path.open("rb") as fh:
            project.image.save(image_path.name, File(fh), save=True)
        self.stdout.write(
            self.style.SUCCESS(f"Image set for '{title}': {project.image.name}")
        )
