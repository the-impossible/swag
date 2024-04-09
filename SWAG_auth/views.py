from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.utils import timezone

# My app import
from SWAG_auth.models import *
from SWAG_auth.forms import *
from SWAG_payment.models import *

# Create your views here.
class LoginPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(
                        request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(
            request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')

class RegisterPageView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/register.html"
    success_message = "Registration Successful you can now login"

    def get_success_url(self):
        return reverse("auth:login")

class ResetPasswordPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/reset_password.html')

class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_purchase"] = Payments.objects.filter(status="success").count()
        context["all_users"] = User.objects.filter(is_staff=False).count()
        context["my_purchase"] = Payments.objects.filter(status="success", user=self.request.user).count()
        context["won"] = 0
        return context

class UpdateProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/profile/profile.html"
    form_class = UpdateUserCreationForm
    success_message = 'Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

class CreateUserPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/users/create_update_user.html"
    success_message = "Registration Successful user can login to their account now! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("auth:create_user")

class ManageUsersPageView(LoginRequiredMixin, ListView):
    template_name = "backend/users/manage_users.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')

class DeleteUserView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_message = 'Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_users')

class EditUserView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/users/create_update_user.html"
    form_class = UpdateUserCreationForm
    success_message = 'Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_users")

class CreateAdminPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = AdminCreationForm
    template_name = "backend/admin/create_update_admin.html"
    success_message = "Admin account created successfully! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("auth:create_admin")

    def form_valid(self, form):
        form.instance.is_staff = True
        form = super().form_valid(form)

        return form

class ManageAdminPageView(LoginRequiredMixin, ListView):
    template_name = "backend/admin/manage_admin.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=True).order_by('-date_joined')

class EditAdminView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/admin/create_update_admin.html"
    form_class = UpdateAdminForm
    success_message = 'Admin Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_admin")

class DeleteAdminView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_message = 'Admin Account Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_admin')
