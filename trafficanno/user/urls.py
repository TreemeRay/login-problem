from django.urls import path
from .views import AdvertiserRegistration, PublisherRegistration, Registration, EmailSubmitting, PasswordSubmit, Login, \
    ForgotPassword

urlpatterns = [
    path('sign-up/advertiser/', AdvertiserRegistration.as_view(), name='advert-reg'),
    path('sign-up/publisher/', PublisherRegistration.as_view(), name='pub-reg'),
    path('sign-up/', Registration.as_view(),  name='sign-up'),
    path('sign-up/email_submit', EmailSubmitting.as_view(), name='email_submit'),
    path('sign-up/password_confirm' , PasswordSubmit.as_view(), name='password_submit'),
    path('login/', Login.as_view(), name='login'),
    path('forgot_password/', ForgotPassword.as_view(), name="forgot_password")

]
