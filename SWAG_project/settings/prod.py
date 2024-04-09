from .base import *

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['ekitiswagquizcompetition.com']


# Media files
STATIC_ROOT = '/home/kadpmhmu/public_html/static'
MEDIA_ROOT = '/home/kadpmhmu/public_html/media'

# Payment
FLUTTERWAVE_SECRET_KEY = config("FLUTTERWAVE_SECRET_KEY")

HTTP = 'https://'