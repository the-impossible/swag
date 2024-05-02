from .base import *

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['swingacademicgame.com', 'www.swingacademicgame.com']


# Media files
STATIC_ROOT = '/home/kadpwtrj/swingacademicgame.com/static'
MEDIA_ROOT = '/home/kadpwtrj/swingacademicgame.com/media'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

# Payment
FLUTTERWAVE_SECRET_KEY = config("FLUTTERWAVE_SECRET_KEY")

HTTP = 'https://'