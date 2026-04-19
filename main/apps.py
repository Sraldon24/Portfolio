from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        # Wire signal handlers (auto-translate + fragment cache invalidation)
        from . import signals  # noqa: F401
