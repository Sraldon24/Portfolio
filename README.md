# Professional Portfolio

A modern, bilingual (English/French) portfolio website built with **Django** and **Tailwind CSS**. This application allows you to showcase your projects, skills, and experience while managing content dynamically through a customized Admin interface.

## Features

### 🎨 User-facing Features

- **Single-page layout**: Modern scrollable portfolio with anchored sections for About, Skills, Projects, Experience, Education, Hobbies, Testimonials, and Contact.
- **Hero / About section**: Profile image, name, bio, and clear calls-to-action (e.g. “Download Resume”, “Get in Touch”).
- **Configurable hero background**: Support for gradient (default), image, video, or slideshow backgrounds controlled from the admin.
- **Skills grid**: List of skills with visual proficiency indicators.
- **Projects gallery**: Project cards with image, title, description, dates, and links for both source code and live demo.
- **Experience & education timeline**: Chronological display of work experience and education entries with optional icons.
- **Hobbies section**: Icon-based grid for hobbies or interests with optional descriptions.
- **Testimonials**: Public testimonials section showing only approved entries.
- **Contact form**: User-friendly contact form with validation; shows key contact info (email, phone) alongside the form.
- **Testimonial submission**: Separate form for visitors to submit testimonials that require admin approval before publishing.
- **Navigation bar**: Fixed navbar with anchor links to all major sections and a responsive hamburger menu on mobile.
- **Language switcher**: EN/FR toggle in the navigation bar that switches both static and dynamic content.
- **Scroll animations**: Smooth fade-in effects for sections as the user scrolls.
- **Toast notifications**: Success and error toasts for form submissions with automatic dismissal after a short delay.

### 🌍 Internationalization (i18n)

- Fully bilingual support (English & French).
- Language switcher in the navigation bar.
- Localized content for:
    - Static template text (headers, buttons, form labels).
    - Dynamic database content (profile, skills, projects, experience, education, hobbies, testimonials) using `django-parler`.
- Automatic fallback translations using `deep-translator` (e.g. auto-translate English content to French when missing).

### 🛠 Admin Dashboard & Content Management

- **Custom notification badge**: Real-time count of pending testimonials (and other items) in the admin header/sidebar.
- **Enhanced list views**:
    - Content snippets for Messages and Testimonials so you can preview content without clicking in.
    - Clickable links and description previews for Projects and other content.
    - Improved filtering and sorting for all major models.
- **Centralized hero configuration**: Manage hero background type (gradient, image, video, slideshow) and assets directly from admin.
- **Media management**: Upload and manage profile image, project images, hobby icons, and hero assets.

### 📧 Notifications, Forms & Anti-spam

- **Email alerts**: Admins receive email notifications (console output in development) for new Contact Messages and Testimonials.
- **Validated forms**: Length limits and validations for contact messages and testimonials to avoid excessively long content.
- **Rate limiting**: Contact and testimonial forms are limited to **5 submissions per hour per IP** using `django-ratelimit` (Redis-backed in production).
- **Spam protection**: Honeypot fields to mitigate bots and automated spam submissions.

### 🔒 Security, Performance & SEO

- **Environment variables**: Sensitive settings (`SECRET_KEY`, `DEBUG`, database credentials, email settings, etc.) are loaded from `.env`.
- **Secure production settings**: HSTS, SSL redirect, secure cookies, and CSRF trusted origins for deployment on platforms like Railway.
- **Caching**: Uses Redis when `REDIS_URL` is set (or local memory cache) to support rate limiting and better performance.
- **Static files**: Whitenoise with compression and manifest storage for efficient static file serving in production.
- **SEO optimized**: Meta description, Open Graph (OG) tags, and Twitter card tags for rich social media previews, plus semantic HTML structure.

### ⚙️ Technical Stack & Tooling

- **Backend**: Django 6.0 (Python 3.13 compatible).
- **Frontend**: Django templates with Tailwind CSS, Font Awesome icons, and modern typography.
- **Internationalization stack**: `django-parler` for translatable models and `deep-translator` for automatic translations.
- **Database**: SQLite by default; `dj-database-url` support for PostgreSQL and other databases in production.
- **Static & media handling**: Whitenoise for static files and Pillow for image processing.
- **Background & environment**: Dockerfile and Gunicorn for production, plus `ensure_admin` management command to create an admin user from environment variables.
- **Testing**: Django test suite covering models, views, forms, rate limiting, and hero background behavior.

## Tech Stack

- **Backend**: Python, Django 6.0
- **Frontend**: HTML5, Django Templates, Tailwind CSS (CDN)
- **Database**: SQLite (Development)
- **Utilities**: django-parler (Translations), Pillow (Image handling)

## Setup Instructions

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/Sraldon24/Portfolio.git
    cd Portfolio
    ```

2.  **Create Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Copy the example environment file:

    ```bash
    cp .env.example .env
    ```

    Edit `.env` and set a secure `SECRET_KEY` and `DEBUG=False` for production.

5.  **Run Migrations**

    ```bash
    python manage.py migrate
    ```

6.  **Create Superuser**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```

## Admin Access

- URL: `/admin/`
- Login with your superuser credentials.
- Look for the **🔔 Notification Badge** in the header for new items!

## Project Structure

- `main/`: Core app containing models, views, and templates.
- `portfolio_core/`: Project settings and configuration.
- `locale/`: Translation files (`.po` / `.mo`).
- `templates/`: Global templates (e.g., admin overrides).
