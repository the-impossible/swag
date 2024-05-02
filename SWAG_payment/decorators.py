from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

# My App imports
from SWAG_auth.models import (
    User,
)

# Check if the user has updated his or her profile
def has_updated(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.has_updated():
            return func(request, *args, **kwargs)
        else:
            messages.info(request, 'You have to update your profile before proceeding!')
            return redirect('auth:profile', request.user.user_id)
    return wrapper_func