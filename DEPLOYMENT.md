# Deployment Guide

This guide outlines the necessary configuration changes to take your portfolio application from development to production, with a focus on **AWS SES** for emails.

## 1. Environment Variables (`.env`)

In production, you **must not** rely on default settings. Your `.env` file is the source of truth for secrets.

**Do NOT commit `.env` to GitHub.**

Create a `.env` file on your production server with the following values:

```bash
# Security
DEBUG=False
SECRET_KEY=your-super-long-secure-random-string-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (If using PostgreSQL/MySQL instead of SQLite)
# DATABASE_URL=postgres://user:password@hostname:5432/dbname

# Email (AWS SES via SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=AKIAXXXXXXXXXXXXXXXX  # Your SES SMTP Username
EMAIL_HOST_PASSWORD=BnX...           # Your SES SMTP Password
DEFAULT_FROM_EMAIL=contact@yourdomain.com
SERVER_EMAIL=system@yourdomain.com
```

> **Note**: `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are **NOT** your AWS Access Key ID and Secret Access Key. You must generate specific SMTP credentials in the AWS SES Console under "SMTP Settings".

## 2. Django Settings Configuration

Your `portfolio_core/settings.py` needs to read these new values.

### Update `settings.py`

Modify the email section in `portfolio_core/settings.py` to use environment variables instead of hardcoded defaults.

```python
import os

# ... existing code ...

# Email Configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 25))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'root@localhost')
```

## 3. AWS SES Setup Checklist

1.  **Verify Domain**: Go to AWS SES > *Identities* > *Create Identity*. Enter your domain (e.g., `yourdomain.com`) and add the DNS records (DKIM) to your DNS provider.
2.  **Move out of Sandbox**: By default, you can only send to verified emails. Request a "Production Access" limit increase in SES to send emails to anyone.
3.  **Create SMTP Credentials**:
    *   Go to SES > *SMTP Settings*.
    *   Click "Create My SMTP Credentials".
    *   This creates an IAM user. **Download the credentials**. These are what go into your `.env`.

## 4. Final Steps

1.  **Collect Static Files**:
    ```bash
    python manage.py collectstatic
    ```

2.  **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

3.  **Create Superuser** (if not done):
    ```bash
    python manage.py createsuperuser
    ```

4.  **Restart Service**: Use Gunicorn or Systemd to restart your application process.
