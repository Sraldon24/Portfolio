"""Seed real portfolio content — skills, tech tags, projects, career, education.

Idempotent: re-running updates existing rows (matched by English title/name)
rather than duplicating. Translations are written for both EN and FR.

Usage:  python manage.py seed_content
"""

from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from main.models import Education, Experience, Project, Skill, TechTag

# ─── Skills: (name, category, order) ──────────────────────────────
SKILLS = [
    # Languages
    ("Java", "LANGUAGES", 0),
    ("Python", "LANGUAGES", 1),
    ("JavaScript", "LANGUAGES", 2),
    ("C#", "LANGUAGES", 3),
    ("SQL", "LANGUAGES", 4),
    ("Kotlin", "LANGUAGES", 5),
    ("Swift", "LANGUAGES", 6),
    ("Bash", "LANGUAGES", 7),
    ("HTML", "LANGUAGES", 8),
    ("CSS", "LANGUAGES", 9),
    # Frameworks
    ("Spring Boot", "FRAMEWORKS", 0),
    ("React", "FRAMEWORKS", 1),
    ("Django", "FRAMEWORKS", 2),
    (".NET", "FRAMEWORKS", 3),
    ("Tailwind CSS", "FRAMEWORKS", 4),
    # Infrastructure
    ("PostgreSQL", "INFRA", 0),
    ("MySQL", "INFRA", 1),
    ("MongoDB", "INFRA", 2),
    ("Redis", "INFRA", 3),
    ("Docker", "INFRA", 4),
    ("Azure", "INFRA", 5),
    ("Linux", "INFRA", 6),
    ("Git", "INFRA", 7),
    ("GitHub Actions", "INFRA", 8),
    # AI / ML
    ("LangGraph", "AI_ML", 0),
    ("OpenAI API", "AI_ML", 1),
    ("Tavily", "AI_ML", 2),
    ("RAG", "AI_ML", 3),
    ("Prompt Engineering", "AI_ML", 4),
    ("LLM Evaluation", "AI_ML", 5),
    ("scikit-learn", "AI_ML", 6),
    ("pytest", "AI_ML", 7),
]

# ─── Tech tags (shared by projects + career) ──────────────────────
TECH_TAGS = [
    "Python", "Java", "JavaScript", "C#", "SQL", "Spring Boot", "React",
    "Django", "Tailwind CSS", "LangGraph", "OpenAI API", "Tavily", "RAG",
    "PostgreSQL", "MongoDB", "Redis", "Docker", "Azure", "GitHub Actions",
    "pytest", "JWT",
]


def _set_translation(obj, lang, **fields):
    """Write a set of translated fields for one language on a Parler model."""
    obj.set_current_language(lang)
    for key, value in fields.items():
        setattr(obj, key, value)


class Command(BaseCommand):
    help = "Seed real portfolio content (skills, tech tags, projects, career)."

    @transaction.atomic
    def handle(self, *args, **options):
        self._seed_skills()
        tags = self._seed_tech_tags()
        self._seed_projects(tags)
        self._seed_career(tags)
        self._seed_education()
        self.stdout.write(self.style.SUCCESS("Content seed complete."))

    # ── Skills ────────────────────────────────────────────────────
    def _seed_skills(self):
        deleted, _ = Skill.objects.all().delete()
        for name, category, order in SKILLS:
            skill = Skill(category=category, order=order)
            skill.set_current_language("en")
            skill.name = name
            skill.save()
            # Skill names are technology proper nouns — identical in FR.
            skill.set_current_language("fr")
            skill.name = name
            skill.save()
        self.stdout.write(
            f"Skills: deleted {deleted} old, created {len(SKILLS)} categorized."
        )

    # ── Tech tags ─────────────────────────────────────────────────
    def _seed_tech_tags(self):
        tags = {}
        for name in TECH_TAGS:
            tag, _ = TechTag.objects.get_or_create(name=name)
            tags[name] = tag
        self.stdout.write(f"Tech tags: {len(tags)} ensured.")
        return tags

    # ── Projects ──────────────────────────────────────────────────
    def _seed_projects(self, tags):
        projects = [
            {
                "title_en": "VerifIA",
                "title_fr": "VerifIA",
                "role_en": "AI Research Intern, Contributor",
                "role_fr": "Stagiaire en recherche IA, Contributeur",
                "desc_en": (
                    "Open-source Python framework for domain-aware ML model "
                    "verification, developed at Polytechnique Montréal's SWAT "
                    "Lab. I contributed a Tavily web-search RAG step that "
                    "grounds LLM-generated verification specifications in "
                    "retrieved knowledge instead of hallucinations. I designed "
                    "16 edit-policy guardrails preventing LLM-proposed domain "
                    "revisions from silently weakening verification criteria, "
                    "and iterated on 27 prompts with few-shot exemplars and a "
                    "contradiction-review evaluation stage. The framework uses "
                    "LangGraph for agent orchestration and integrates with "
                    "multiple LLM providers via a structured router. "
                    "Benchmarked across 7 of 9 TabArena datasets."
                ),
                "desc_fr": (
                    "Cadre open-source Python pour la vérification de modèles "
                    "d'apprentissage machine adaptée au domaine, développé au "
                    "laboratoire SWAT de Polytechnique Montréal. J'ai contribué "
                    "une étape RAG avec recherche web Tavily qui ancre les "
                    "spécifications de vérification générées par LLM dans des "
                    "connaissances réelles plutôt que d'halluciner. J'ai conçu "
                    "16 garde-fous de politique d'édition empêchant les "
                    "modifications de domaine proposées par le LLM d'affaiblir "
                    "silencieusement les critères de vérification, et itéré sur "
                    "27 prompts avec exemples few-shot et une étape "
                    "d'évaluation par revue de contradictions."
                ),
                "start_date": "2026-03",
                "end_date": "",
                "created_date": date(2026, 3, 1),
                "code_link": "",
                "demo_link": "https://verifia.ca",
                "tags": ["Python", "LangGraph", "OpenAI API", "Tavily", "RAG", "pytest"],
            },
            {
                "title_en": "Pet Clinic",
                "title_fr": "Pet Clinic",
                "role_en": "Microservice Owner — Billing Service",
                "role_fr": "Responsable Microservice — Service de Facturation",
                "desc_en": (
                    "Full-stack microservices-based veterinary clinic platform "
                    "built as a team-based Champlain College capstone. I owned "
                    "the Billing service: shipped customer bill-payment "
                    "functionality with JWT-authenticated REST endpoints, "
                    "integration-tested PDF receipt generation, and React "
                    "admin UI components for payment management. Worked across "
                    "cross-service boundaries with Customers, Vets, and Visits "
                    "microservices."
                ),
                "desc_fr": (
                    "Plateforme de clinique vétérinaire full-stack basée sur "
                    "les microservices, construite comme projet d'équipe au "
                    "Collège Champlain. J'ai été responsable du service de "
                    "facturation: paiement de factures clients avec endpoints "
                    "REST authentifiés par JWT, génération de reçus PDF testée "
                    "par intégration, et composants React pour l'interface "
                    "d'administration."
                ),
                "start_date": "2025",
                "end_date": "",
                "created_date": date(2025, 1, 1),
                "code_link": "https://github.com/cgerard321/champlain_petclinic",
                "demo_link": "",
                "tags": ["Spring Boot", "React", "Docker", "MongoDB", "JWT"],
            },
        ]
        for data in projects:
            project = Project.objects.filter(
                translations__title=data["title_en"]
            ).first()
            created = project is None
            if created:
                project = Project(created_date=data["created_date"])
            project.start_date = data["start_date"]
            project.end_date = data["end_date"]
            project.code_link = data["code_link"]
            project.demo_link = data["demo_link"]
            project.save()
            _set_translation(
                project, "en",
                title=data["title_en"], description=data["desc_en"],
                role=data["role_en"],
            )
            project.save()
            _set_translation(
                project, "fr",
                title=data["title_fr"], description=data["desc_fr"],
                role=data["role_fr"],
            )
            project.save()
            project.tech_tags.set([tags[t] for t in data["tags"]])
            verb = "created" if created else "updated"
            self.stdout.write(f"Project {verb}: {data['title_en']}")

        # ── Update existing projects with new fields only ──────────
        self._update_existing_project(
            tags,
            title="CourtierPro",
            role_en="Transactions Domain Lead",
            role_fr="Responsable du domaine des transactions",
            tag_names=["Spring Boot", "React", "PostgreSQL", "Docker", "GitHub Actions"],
        )
        portfolio_fr = (
            "Portfolio single-page bilingue (FR/EN) construit avec Django et "
            "Tailwind, avec un hero configurable, des sections de compétences "
            "et de projets, une chronologie expérience/éducation, des loisirs, "
            "des témoignages, et des formulaires de contact et témoignage "
            "validés, soutenus par un admin personnalisé avec badges de "
            "notification, traduction complète du contenu, formulaires limités "
            "en fréquence et protégés contre le spam, et prêt pour la "
            "production avec Docker/Gunicorn/Whitenoise, cache Redis et tests."
        )
        self._update_existing_project(
            tags,
            title="Portfolio",
            role_en="Solo Developer",
            role_fr="Développeur solo",
            tag_names=["Django", "Tailwind CSS", "Docker", "Redis", "PostgreSQL",
                       "GitHub Actions"],
            desc_fr=portfolio_fr,
        )

    def _update_existing_project(
        self, tags, title, role_en, role_fr, tag_names, desc_fr=None
    ):
        project = Project.objects.filter(translations__title=title).first()
        if not project:
            self.stdout.write(
                self.style.WARNING(f"Project '{title}' not found — skipped.")
            )
            return
        # Role (translated) — keep existing descriptions unless overridden.
        project.set_current_language("en")
        project.role = role_en
        project.save()
        project.set_current_language("fr")
        project.role = role_fr
        if desc_fr is not None:
            project.description = desc_fr
        project.save()
        project.tech_tags.set([tags[t] for t in tag_names])
        self.stdout.write(f"Project updated (fields): {title}")

    # ── Career ────────────────────────────────────────────────────
    def _seed_career(self, tags):
        entries = [
            {
                "title_en": "AI Research Intern",
                "title_fr": "Stagiaire en recherche IA",
                "company": "Polytechnique Montréal — SWAT Lab",
                "role_type": "RESEARCH",
                "start_date": date(2026, 3, 1),
                "end_date": None,
                "is_current": True,
                "desc_en": (
                    "Contributing to VerifIA, an open-source Python framework "
                    "for domain-aware ML model verification. Built a Tavily "
                    "web-search RAG step grounding LLM outputs in retrieved "
                    "knowledge, designed 16 edit-policy guardrails for the "
                    "AI-Based Domain Generation pipeline, and iterated on 27 "
                    "prompts to minimize hallucinations."
                ),
                "desc_fr": (
                    "Contribution à VerifIA, un cadre open-source Python pour "
                    "la vérification de modèles d'apprentissage machine. "
                    "Construction d'une étape RAG avec recherche web Tavily "
                    "ancrant les sorties LLM dans des connaissances réelles, "
                    "conception de 16 garde-fous de politique d'édition pour le "
                    "pipeline de génération de domaine assisté par IA, et "
                    "itération sur 27 prompts pour minimiser les hallucinations."
                ),
                "tags": ["Python", "LangGraph", "OpenAI API", "Tavily", "RAG", "pytest"],
            },
            {
                "title_en": "Peer Tutor, Programming Fundamentals",
                "title_fr": "Tuteur pair, Fondements de programmation",
                "company": "Champlain College Saint-Lambert",
                "role_type": "TUTORING",
                "start_date": date(2025, 9, 1),
                "end_date": date(2025, 11, 30),
                "is_current": False,
                "desc_en": (
                    "Delivered 20+ hours of one-on-one and small-group "
                    "tutoring to a cohort of approximately 20 first-year "
                    "Computer Science students. Focused on breaking down "
                    "technical concepts into plain language and adapting "
                    "explanations to each student's experience level."
                ),
                "desc_fr": (
                    "Livré plus de 20 heures de tutorat individuel et en petits "
                    "groupes à une cohorte d'environ 20 étudiants de première "
                    "année en informatique. Concentration sur la simplification "
                    "de concepts techniques et l'adaptation des explications au "
                    "niveau de chaque étudiant."
                ),
                "tags": [],
            },
        ]
        for data in entries:
            exp = Experience.objects.filter(
                translations__job_title=data["title_en"]
            ).first()
            created = exp is None
            if created:
                exp = Experience(start_date=data["start_date"])
            exp.start_date = data["start_date"]
            exp.end_date = data["end_date"]
            exp.role_type = data["role_type"]
            exp.is_current = data["is_current"]
            exp.save()
            _set_translation(
                exp, "en",
                job_title=data["title_en"], company=data["company"],
                description=data["desc_en"],
            )
            exp.save()
            _set_translation(
                exp, "fr",
                job_title=data["title_fr"], company=data["company"],
                description=data["desc_fr"],
            )
            exp.save()
            if data["tags"]:
                exp.tech_used.set([tags[t] for t in data["tags"]])
            verb = "created" if created else "updated"
            self.stdout.write(f"Career {verb}: {data['title_en']}")

        # Existing "Product Demonstrator" — add role_type only.
        demo = Experience.objects.filter(
            translations__job_title__icontains="Product Demonstrator"
        ).first()
        if demo:
            demo.role_type = "PART_TIME"
            demo.save()
            self.stdout.write("Career updated (role_type): Product Demonstrator")
        else:
            self.stdout.write(
                self.style.WARNING("'Product Demonstrator' not found — skipped.")
            )

    # ── Education ─────────────────────────────────────────────────
    def _seed_education(self):
        # New: Concordia BEng
        concordia = Education.objects.filter(
            translations__institution="Concordia University"
        ).first()
        created = concordia is None
        if created:
            concordia = Education(start_date=date(2026, 9, 1))
        concordia.start_date = date(2026, 9, 1)
        concordia.end_date = date(2030, 6, 1)
        concordia.save()
        _set_translation(
            concordia, "en",
            degree="Bachelor of Engineering, Software Engineering",
            institution="Concordia University",
        )
        concordia.save()
        _set_translation(
            concordia, "fr",
            degree="Baccalauréat en génie logiciel",
            institution="Concordia University",
        )
        concordia.save()
        self.stdout.write(
            f"Education {'created' if created else 'updated'}: Concordia University"
        )

        # Existing: Champlain DEC — update degree text.
        champlain = Education.objects.filter(
            translations__institution__icontains="Champlain"
        ).first()
        if champlain:
            champlain.start_date = date(2023, 8, 1)
            champlain.end_date = date(2026, 6, 1)
            champlain.save()
            _set_translation(
                champlain, "en",
                degree="DEC, Computer Science Technology — 80%+ average, "
                "Honour Roll Fall 2025",
                institution="Champlain College Saint-Lambert",
            )
            champlain.save()
            _set_translation(
                champlain, "fr",
                degree="DEC, Techniques de l'informatique — moyenne 80%+, "
                "Tableau d'honneur automne 2025",
                institution="Champlain College Saint-Lambert",
            )
            champlain.save()
            self.stdout.write("Education updated: Champlain College")
        else:
            self.stdout.write(
                self.style.WARNING("Champlain education not found — skipped.")
            )
