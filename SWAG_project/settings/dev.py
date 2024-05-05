from .base import *

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'Static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Payment
FLUTTERWAVE_SECRET_KEY = config("FLUTTERWAVE_SECRET_KEY")

# Email
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL=config('EMAIL_USE_SSL')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'richardemmanuel45@gmail.com'
EMAIL_HOST_PASSWORD = 'kqrbbzylrxqpwbmn'