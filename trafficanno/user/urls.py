from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path

from .views import AdvertiserRegistration, PublisherRegistration, Registration, EmailSubmitting, PasswordSubmit, Login, \
    ForgotPassword, MyPasswordResetConfirmView, AdvertProfile, PublProfile, PublFormProfile, RessetPass, \
    AdvertFormProfile

urlpatterns = [
    path('sign-up/advertiser/', AdvertiserRegistration.as_view(), name='advert-reg'),
    path('sign-up/publisher/', PublisherRegistration.as_view(), name='pub-reg'),
    path('sign-up/', Registration.as_view(),  name='sign-up'),
    path('sign-up/email_submit', EmailSubmitting.as_view(), name='email_submit'),
    path('sign-up/password_confirm' , PasswordSubmit.as_view(), name='password_submit'),
    path('login/', Login.as_view(), name='login'),
    path('forgot_password/', ForgotPassword.as_view(), name="forgot_password"),
    path('reset/<uidb64>/<token>/',MyPasswordResetConfirmView.as_view(template_name='user/confirmation.html'),name='confirmation'),
    path('reset/<uidb64>/<token>/',PasswordSubmit.as_view(template_name='user/password_confirm.html'),name='password_confirm'),
    path('password-reset/complete/', PasswordResetDoneView.as_view(template_name='user/complete.html'),name='password_reset_complete'),
    path('advert-profile', AdvertProfile.as_view() , name="advert_profile"),
    path('publ-profile', PublProfile.as_view() , name="publ_profile"),
    path('publ_profile_form' , PublFormProfile.as_view(), name= "publ_profile_form"),
    path('advert_profile_form', AdvertFormProfile.as_view(), name="advert_profile_form"),
    path('reset_pass', RessetPass.as_view() , name='reset_pass')

]
