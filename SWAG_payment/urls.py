from django.urls import path

app_name = "payment"

from SWAG_payment.views import *

urlpatterns = [
    path('make_payment', MakePaymentView.as_view(), name='make_payment'),
    path('initialize_payment/<str:type>', GetPaymentLink.as_view(), name='initialize_payment'),

    path('my_payments', MyPaymentView.as_view(), name='my_payments'),
    path('all_payments', AllPaymentView.as_view(), name='all_payments'),

    path('verify_payment', VerifyPayment.as_view(), name='verify_payment'),
    path('re_verify_payment/<str:payment_id>', ReVerifyPayment.as_view(), name='re_verify_payment'),

    path('upload_receipt', UploadReceiptView.as_view(), name='upload_receipt'),
    path('manage_receipts', ManageReceiptView.as_view(), name='manage_receipts'),
    path('verify_receipts', VerifyReceiptView.as_view(), name='verify_receipts'),

    path('compete_for_box', CompeteForBoxView.as_view(), name='compete_for_box'),
]
