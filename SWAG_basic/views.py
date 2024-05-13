from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from SWAG_basic.forms import *
from SWAG_basic.models import *
from SWAG_auth.utils import *

# Create your views here.

class HomePageView(TemplateView):
    template_name = "frontend/index.html"

class VolunteerPageView(SuccessMessageMixin, CreateView):

    template_name = "frontend/volunteer.html"
    model = Volunteer
    form_class = VolunteerForm
    success_message = "Application submitted you will be contacted shortly!"

    def get_success_url(self):
        return reverse("basic:volunteer")

    def form_valid(self, form):

        # SEND EMAIL
        user_details = {
            'name':form.cleaned_data['name'],
            'email':form.cleaned_data['email'],
            'phone':form.cleaned_data['phone_number'],
            'gender':form.cleaned_data['gender'],
            'occupation':form.cleaned_data['occupation'],
            'age':form.cleaned_data['age'],
            'role_you_want_to_volunteer':form.cleaned_data['role_you_want_to_volunteer'],
        }

        Email.send(user_details, 'volunteer')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error submitting form")
        return super().form_invalid(form)


class TrainingPageView(SuccessMessageMixin, CreateView):
    template_name = "frontend/training.html"
    model = Training
    form_class = TrainingForm
    success_message = "Application submitted you will be contacted shortly!"

    def get_success_url(self):
        return reverse("basic:training")

    def form_valid(self, form):
        entries = Training.objects.count()

        user_details = {
            'name':form.cleaned_data['name'],
            'email':form.cleaned_data['email'],
            'phone':form.cleaned_data['phone_number'],
            'gender':form.cleaned_data['gender'],
            'occupation':form.cleaned_data['occupation'],
            'age':form.cleaned_data['age'],
        }

        # SEND EMAIL
        Email.send(user_details, 'training')

        return super().form_valid(form)


