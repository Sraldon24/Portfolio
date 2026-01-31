# Professional Portfolio

A modern, bilingual (English/French) portfolio website built with **Django** and **Tailwind CSS**. This application allows you to showcase your projects, skills, and experience while managing content dynamically through a customized Admin interface.

## Features

### 🌍 Internationalization (i18n)

- Fully bilingual support (English & French).
- Language switcher in the navigation bar.
- Localized content for:
    - Static template text (Headers, Buttons, Form labels).
    - Dynamic database content (Project titles, descriptions, etc.) using `django-parler`.

### 🛠 Admin Dashboard Improvements

- **Custom Notification Badge**: Real-time count of pending testimonials and unread messages directly in the Admin header.
- **Enhanced List Views**:
    - Content snippets for Messages and Testimonials (preview content without clicking).
    - Clickable links and description previews for Projects.
    - Improved filtering and sorting for all models.

### 📧 Notifications & Contact

- **Email Alerts**: Admins receive email notifications (console output in dev) for new Contact Messages and Testimonials.
- **Contact Form**: Validation and storage of user messages.
- **Testimonials**: Submission form for visitors; requires admin approval before publishing.

### 🔒 Security & SEO

- **Environment Variables**: Sensitive settings (`SECRET_KEY`, `DEBUG`) are externalized via `.env`.
- **SEO Optimized**: Meta tags, Open Graph (OG) tags for social media previews, and semantic HTML.

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
