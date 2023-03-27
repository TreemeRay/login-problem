from pyexpat.errors import messages

from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, UpdateView
from .forms import AdvertiserSignUpForm, PublisherSignUpForm, PasswordConfirm, EmailAuthenticationForm, \
    ForgotPasswordForm, ResetSetPasswordForm
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()


class AdvertiserRegistration(CreateView):
    model = User
    form_class = AdvertiserSignUpForm
    template_name = 'user/advert_registration.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if form.is_valid():
            email = form.cleaned_data['email']

            user = User.objects.get(email=email)

            if user:
                subject = 'Confirm Password'
                email_template_name = 'user/pass_confirm_message.html'
                cont = {
                    'email': user,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'OnlineShop',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                msg_html = render_to_string(email_template_name, cont)
                send_mail(subject, 'link', settings.EMAIL_HOST_USER, [email], fail_silently=False,
                          html_message=msg_html)
                # messages.success(self.request, 'Mail was sent successfully!')

        return render(self.request, 'user/email_submitting.html')


class PublisherRegistration(CreateView):
    model = User
    form_class = PublisherSignUpForm
    template_name = 'user/publ_registration.html'


    def form_valid(self, form):
        self.form
        user = form.save()
        login(self.request, user)
        subject = 'Confirm Password'
        email_template_name = 'user/pass_confirm_message.html'
        cont = {
            'email': self.request.user.email,
            'domain': '127.0.0.1:8000',
            'site_name': 'OnlineShop',
            'uid': urlsafe_base64_encode(force_bytes(self.request.user.pk)),
            'user': user,
            'token': default_token_generator.make_token(self.request.user),
            'protocol': 'http',
        }
        msg_html = render_to_string(email_template_name, cont)
        send_mail(subject, 'link', settings.EMAIL_HOST_USER, [self.request.user.email], fail_silently=False,
                  html_message=msg_html)
        # messages.success(self.request, 'Mail was sent successfully!')

        return render(self.request, 'user/email_submitting.html')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs



class Registration(CreateView):
    def get(self, request):
        return render(request, 'user/registration.html')


class EmailSubmitting(CreateView):
    def get(self, request):
        return render(request, 'user/email_submitting.html')


class PasswordSubmit(UpdateView):
    model = User
    form_class = PasswordConfirm
    template_name = 'user/password_confirm.html'
    success_url = reverse_lazy('sign-up')

    def get_object(self, queryset=None):
        return self.request.user


class Login(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = AuthenticationForm()
            return render(self.request, 'user/login.html', {'form': form})
        else:
            return redirect(self.request.path)

    def post(self, *args, **kwargs):
        form = AuthenticationForm(data=self.request.POST)

        if form.is_valid():
            user = form.get_user()
            login(self.request, user)

            if user.is_advertiser:
                return redirect(reverse('advert_profile'))

            elif user.is_publisher:
                return redirect(reverse('publ_profile'))
        else:
            return render(self.request, 'user/login.html', {'form': form})


class ForgotPassword(View):
    def get(self, *args, **kwargs):
        form = ForgotPasswordForm()
        return render(self.request, 'user/forgot_password.html', {'form': form})

    def post(self, *args, **kwargs):
        form = ForgotPasswordForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user = User.objects.get(email=email)

            if user:
                subject = 'Requested password reset'
                email_template_name = 'user/forgot_password_message.html'
                cont = {
                    'email': email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'OnlineShop',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                msg_html = render_to_string(email_template_name, cont)
                send_mail(subject, 'link', settings.EMAIL_HOST_USER, [email], fail_silently=False,
                          html_message=msg_html)
                # messages.success(self.request, 'Mail was sent successfully!')

        return render(self.request, 'user/forgot_password.html', {'form': form})


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = ResetSetPasswordForm


class AdvertProfile(CreateView):
    def get(self, request):
        return render(request, 'user/user_inc/advert_profile.html')


class PublProfile(CreateView):
    def get(self, request):
        return render(request, 'user/user_inc/publ_profile.html')
