from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.decorators import method_decorator
from SWAG_payment.models import *
from SWAG_payment.forms import *
# from SWAG_payment.decorator import *
from django.conf import settings
import uuid
import requests
# Create your views here.

class MakePaymentView(LoginRequiredMixin, TemplateView):
    template_name = "backend/payment/make_payment.html"

    def get_context_data(self, **kwargs):
        context = super(MakePaymentView, self).get_context_data(**kwargs)
        context['product'] = Product.objects.first()
        return context

def generate_transaction_reference():
    # Generate a random UUID
    unique_id = uuid.uuid4()

    # Create a unique transaction reference by combining the timestamp and UUID
    transaction_reference = f"SWAG-{unique_id}"

    return transaction_reference

class GetPaymentLink(LoginRequiredMixin, View):
    template_name = "payment/make_payment.html"

    def get(self, request):

        # purchase details
        quantity = int(request.GET['quantity'])
        if quantity < 1:
            messages.error(request, 'Quantity has to be greater than 1!')
            return redirect('payment:make_payment')
        amount = Product.objects.first().amount
        total  = amount * quantity

        # Define your API endpoint
        flutterwave_endpoint = "https://api.flutterwave.com/v3/payments"

        # Set your Flutterwave API secret key
        api_secret_key = settings.FLUTTERWAVE_SECRET_KEY

        # Define the data you want to send to Flutterwave (adjust as needed)

        current_site = get_current_site(request).domain

        data = {
            "tx_ref": str(generate_transaction_reference()),
            "amount": str(total),  # Adjust the amount as needed
            "currency": "NGN",  # Currency code
            "redirect_url": "https://swingacademicgame.com/auth/payment/verify_payment",  # Redirect URL after payment
            "meta": {
                'customer_id':str(request.user.phone_number),
                'customer_mac':str(request.user.pk),
            },
            "customer":{
                'email': request.user.email,
                'phone': str(request.user.phone_number),
                'name': request.user.name,
            },
            "customizations":{
                'title':"SWAG Payment",
                'logo':"https://hrcs.spectrum-royalgate.com.ng/wp-content/uploads/2022/05/SPECTRUM-ROYAL-GATE.png",
                'description':'SWAG Game Purchase'
            },
            # Add other required parameters here
            "payment_options": "card, ussd, banktransfer",
        }

        # Set headers with your API key
        headers = {
            "Authorization": f"Bearer {api_secret_key}",
            "Content-Type": "application/json",
        }

        # Make the POST request to create the payment link
        try:
            response = requests.post(flutterwave_endpoint, json=data, headers=headers)

            # Check for a successful response
            if response.status_code == 200:
                # You can parse the response JSON here
                flutterwave_data = response.json()

                # create a payment invoice
                Payments.objects.create(amount=total, tx_ref=data['tx_ref'], user=request.user, status='pending', description="SWAG Game Purchase", quantity=quantity)

                return redirect(flutterwave_data['data']['link'])
            else:
                messages.error(request, 'Failed to initialize payment try again!!')
                return redirect('payment:make_payment')

        except Exception as e:
            messages.error(request, f'An error occurred here!!')
            return redirect('payment:make_payment')

class MyPaymentView(LoginRequiredMixin, ListView):
    model = Payments
    queryset = Payments.objects.all()
    template_name = "backend/payment/my_payments.html"

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user).order_by('-date_created')

class AllPaymentView(LoginRequiredMixin, ListView):
    model = Payments
    queryset = Payments.objects.all().order_by('-date_created')
    template_name = "backend/payment/my_payments.html"

class ReVerifyPayment(LoginRequiredMixin, View):
    template_name = "payment/make_payment.html"

    def get(self, request, payment_id):
        try:
            transaction = Payments.objects.get(payment_id=payment_id)
            verify_payment(request, transaction.tx_ref, transaction.transaction_id, False)

        except Payments.DoesNotExist:
            messages.error(request, f'Failed to Re-query Transaction')

        if request.user.is_staff:
            return redirect('payment:all_payments')

        return redirect('payment:my_payments')


def verify_payment(request, tx_ref, transaction_id, fresh=True):
    try:

        transaction_details = Payments.objects.get(tx_ref=tx_ref)


        if fresh:
            transaction_details.transaction_id=transaction_id
            # Define your API endpoint
            flutterwave_endpoint = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
        else:
            flutterwave_endpoint = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={transaction_details.tx_ref}"

        # Set your Flutterwave API secret key
        api_secret_key = settings.FLUTTERWAVE_SECRET_KEY

        # Set headers with your API key
        headers = {
            "Authorization": f"Bearer {api_secret_key}",
            "Content-Type": "application/json",
        }

        # Send a GET request to Flutterwave's verification endpoint
        response = requests.get(flutterwave_endpoint, headers=headers)

        # Check for a successful response
        if response.status_code == 200:
            # You can parse the response JSON here
            flutterwave_data = response.json()

            if (
                flutterwave_data["data"]["status"] == "successful"
                and flutterwave_data["data"]["amount"] >= transaction_details.amount
            ):
                # Success! Confirm the customer's payment
                transaction_details.status = "success"
                messages.success(request, 'Transaction successful, item will be delivered to your address!, kindly make sure you update your profile!!')
            else:
                transaction_details.status = "failed"
                messages.error(request, 'Transaction Failed!!')

        else:
            transaction_details.status = "failed"
            messages.error(request, 'Transaction failed')

        transaction_details.save()
    except Payments.DoesNotExist:
        messages.error(request, f'Failed in getting transaction reference!!')

    except Exception as e:
        messages.error(request, f'An error occurred while performing verification!!')


class VerifyPayment(LoginRequiredMixin, View):

    def get(self, request):

        if request.GET.get('status') == 'successful':
            tx_ref = request.GET.get('tx_ref')
            transaction_id = request.GET.get('transaction_id')

            verify_payment(request, tx_ref, transaction_id, True)
        else:
            messages.error(request, f'Transaction Failed!!')

        if request.user.is_staff:
            return redirect('payment:all_payments')

        return redirect('payment:my_payments')

class ManageReceiptView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = PaymentReceipt
    queryset = PaymentReceipt.objects.all().order_by('-date_uploaded')
    template_name = "backend/payment/manage_receipts.html"

    form_class = UploadReceiptForm
    form_second_class = VerifyUploadedReceiptForm

    def get_queryset(self):
        if self.request.user.is_staff:
            return PaymentReceipt.objects.all().order_by('-date_uploaded')
        return PaymentReceipt.objects.filter(user=self.request.user).order_by('-date_uploaded')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['form'] = self.form_second_class
        else:
            context["form"] = self.form_class
        return context

class UploadReceiptView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PaymentReceipt
    form_class = UploadReceiptForm
    template_name = "backend/payment/manage_receipts.html"
    success_message = "Your payment is been processed and will reflect on your account shortly! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def get_success_url(self):
        return reverse("payment:manage_receipts")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form = super().form_valid(form)
        return form

class VerifyReceiptView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Payments
    form_class = VerifyUploadedReceiptForm
    template_name = "backend/payment/manage_receipts.html"
    success_message = "Payment Status Updated! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def get_success_url(self):
        return reverse("payment:manage_receipts")

    def form_valid(self, form):
        receipt_id = self.request.POST['receipt_id']
        status = self.request.POST['status']

        quantity =  form.instance.quantity
        amount = Product.objects.first().amount
        total  = amount * quantity

        payment_receipt = PaymentReceipt.objects.filter(receipt_id=receipt_id)[0]
        payment_receipt.status = status
        payment_receipt.save()

        form.instance.user = payment_receipt.user
        form.instance.description = "SWAG Game Purchase"
        form.instance.amount = total
        form.instance.quantity = quantity
        form.instance.status = status

        print(f"user: {form.instance.user}")
        print(f"amount: {form.instance.amount}")
        print(f"status: {form.instance.status}")

        form = super().form_valid(form)
        return form
