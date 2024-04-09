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