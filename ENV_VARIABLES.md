# Environment Variables Documentation

This file explains the purpose of each environment variable used in this project. These variables are stored in the `.env` file for local development or set in your hosting provider's dashboard for production.

## General Settings

| Variable        | Description                                                                                                                   | Example                          |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `DEBUG`         | Toggles debug mode. Set to `True` for development to see detailed error pages. **ALWAYS set to `False` in production.**       | `True` or `False`                |
| `SECRET_KEY`    | A long, random string used by Django for cryptographic signing (sessions, cookies, etc.). **Keep this secret in production.** | `django-insecure-...`            |
| `ALLOWED_HOSTS` | A comma-separated list of domain names that this site can serve. Required when `DEBUG=False`.                                 | `127.0.0.1,localhost,mysite.com` |

## Production Deployment (AWS / DigitalOcean)

> [!IMPORTANT]
> **Ensure you set the following in your AWS/DigitalOcean dashboard:**
>
> - `DEBUG=False`
> - `SECRET_KEY=<a-long-random-string>`
> - `ALLOWED_HOSTS=yourdomain.com`

## Database

| Variable       | Description                                                                                                                                                                                 | Example                             |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------- |
| `DATABASE_URL` | The connection string for your database. If not set, the app defaults to a local SQLite file (`db.sqlite3`). In production (Railway, Heroku, etc.), this is usually provided automatically. | `postgres://user:pass@host:5432/db` |

## Cache (Rate Limiting)

| Variable    | Description                                                                                                                                                                                                 | Example                     |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------- |
| `REDIS_URL` | (Optional) Redis connection URL for rate limiting. django-ratelimit requires a cache with atomic increments; without Redis, LocMemCache is used (correct per-process, but limit applies per worker in production). | `redis://localhost:6379/0`  |

## Admin User Management

These variables are used by the `ensure_admin` command (which runs automatically on startup) to create or update the superuser.

| Variable                    | Description                                                                                                              | Example             |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `DJANGO_SUPERUSER_USERNAME` | The username for the admin account.                                                                                      | `admin`             |
| `DJANGO_SUPERUSER_EMAIL`    | The email address for the admin account.                                                                                 | `admin@example.com` |
| `DJANGO_SUPERUSER_PASSWORD` | The password for the admin account. If the user exists but the password differs, it will be updated to match this value. | `SuperSecret123!`   |

## Email Configuration (AWS SES)

These are optional. If not set, emails (contact form) will be printed to the console instead of being sent.

| Variable                | Description                                                                         | Example                  |
| :---------------------- | :---------------------------------------------------------------------------------- | :----------------------- |
| `AWS_ACCESS_KEY_ID`     | Your AWS IAM user's access key ID.                                                  | `AKIA...`                |
| `AWS_SECRET_ACCESS_KEY` | Your AWS IAM user's secret access key.                                              | `(random string)`        |
| `AWS_SES_REGION_NAME`   | The AWS region where your SES identity is verified.                                 | `us-east-1`              |
| `AWS_SES_FROM_EMAIL`    | The email address that the system will send emails _from_. Must be verified in SES. | `noreply@yourdomain.com` |
