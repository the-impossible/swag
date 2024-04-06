from django.urls import path

from SWAG_basic.views import *

app_name = "basic"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]