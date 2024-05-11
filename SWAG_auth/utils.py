# My django imports
import threading #for enhancing page functionality
from django.core.mail import send_mail #for sending mails
from django.conf import settings #to gain access to variables from the settings
from django.http import request #to gain access to the request object
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import get_template #used for getting html template
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib import messages #for sending messages
from django.conf import settings

# My App imports

class EmailThread(threading.Thread):
    def __init__(self, email_subject, email_body, receiver):
        self.email_subject = email_subject
        self.email_body = email_body
        self.sender = settings.EMAIL_HOST_USER
        self.receiver = receiver
        threading.Thread.__init__(self)

    def run(self):
        print(f"SENDING OUT MAILS NOW!!")
        send_mail(
            self.email_subject,
            self.email_body,
            self.sender,
            self.receiver,
            html_message=self.email_body,
            fail_silently=False
        )

class AppTokenGenerator(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id)+text_type(timestamp))

email_activation_token = AppTokenGenerator()

class Mailer(View):


    def send(self, user_details, which):
        welcome = 'Welcome to SWAG! Get Ready to Compete with Students from Your State 🏆'
        reset = 'Reset Your SWAG Account Password'
        volunteer = 'A volunteer just applied'
        training = 'A user just applied for training'

        if which == 'welcome':

            activation_path = 'backend/email/intro_mail.html'
            receiver = [user_details['email']]
            email_subject = welcome
            context_data = {'name': user_details['name'],}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'reset':

            link = reverse('auth:reset_password_activation', kwargs={'uidb64':user_details['uid'], 'token':user_details['token']})
            activation_url = settings.HTTP+user_details['domain']+link
            activation_path = 'backend/email/reset_password.html'
            receiver = [user_details['email']]
            email_subject = reset
            context_data = {'name': user_details['name'], 'reset': activation_url}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'volunteer' or which == 'training':

            activation_path = 'backend/email/volunteer.html'

            receiver = ["swag4africa@gmail.com"]

            context_data = {
                'name': user_details['name'],
                'email':user_details['email'],
                'phone':user_details['phone'],
                'gender':user_details['gender'],
                'occupation':user_details['occupation'],
                'age': user_details['age'],
            }

            if which == 'volunteer':
                email_subject = volunteer
                context_data['role'] = user_details['role_you_want_to_volunteer']
                context_data['type'] = "volunteer"

            if which == 'training':
                email_subject = training
                context_data['type'] = "training"

            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        else:

            messages.error(request, 'Unable to process request')

Email = Mailer()