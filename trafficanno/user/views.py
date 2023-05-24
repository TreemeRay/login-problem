from pyexpat.errors import messages

from django.contrib.auth import get_user_model, login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView
from .forms import AdvertiserSignUpForm, PublisherSignUpForm, PasswordConfirm, EmailAuthenticationForm, \
    ForgotPasswordForm, ResetSetPasswordForm, PublProfileForm, ChangePassword, AdvertProfileForm
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
import datetime

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


class Registration(CreateView):
    def get(self, request):
        return render(request, 'user/registration.html')


class EmailSubmitting(CreateView):
    def get(self, request):
        return render(request, 'user/email_submitting.html')


class PasswordSubmit(View):
    def get(self ,*args ,**kwargs):
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = User.objects.get(pk=uid)
        except(Exception,):
            user = None

        form = PasswordConfirm()
        return render(self.request, 'user/password_confirm.html', {'form': form})

    def post(self, *args , **kwargs):
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = User.objects.get(pk=uid)
        except(Exception,):
            user = None

        form = PasswordConfirm(self.request.POST, user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password2']
            user.set_password(new_password)
            user.save()
            login(self.request, user)

            if user.is_advertiser:
                return redirect(reverse('advert_profile'))

            elif user.is_publisher:
                return redirect(reverse('publ_profile'))


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


class PublProfile(CreateView):
    def get(self, request):
        users_form = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'country_of_residence': request.user.country_of_residence,
            'city': request.user.city,
            'address': request.user.address,
            'email': request.user.email,
            'messenger': request.user.messenger,
            'messenger_nickname': request.user.messenger_nickname,
            'website': request.user.publisher.website,
            'traffic_amount': request.user.publisher.traffic_amount
        }
        form = PublProfileForm(initial=users_form)
        form_pass = ChangePassword(user=request.user, data=request.POST)

        return render(request, 'user/user_inc/publ_profile.html', {'form': form, 'form_pass': form_pass})


class AdvertProfile(CreateView):
    def get(self, request):
        users_form = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'country_of_residence': request.user.country_of_residence,
            'city': request.user.city,
            'address': request.user.address,
            'email': request.user.email,
            'messenger': request.user.messenger,
            'messenger_nickname': request.user.messenger_nickname,
            'short_desc': request.user.advertiser.short_desc,
            'bonus_code': request.user.advertiser.bonus_code
        }
        form = AdvertProfileForm(initial=users_form)
        form_pass = ChangePassword(user=request.user, data=request.POST)

        return render(request, 'user/user_inc/advert_profile.html', {'form': form, 'form_pass': form_pass})


def registered_users(request):
    user = request.user
    context = {'user': user}
    return render(request, 'templates/user/user_inc/vertical_nav/publ_nav_profile.html', context)


class PublFormProfile(View):

    def post(self, *args, **kwargs):
        form = PublProfileForm(self.request.POST)
        if form.is_valid():
            form.save()


class AdvertFormProfile(View):
    def post(self, *args, **kwargs):
        form = AdvertProfileForm(self.request.POST)
        if form.is_valid():
            form.save()


class RessetPass(View):
    def get(self, *args, **kwargs):
        form = ChangePassword()
        return render(self.request, 'user/user_inc/publ_profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePassword(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            return redirect(reverse('publ_profile'))
        else:
            form_errors = form.errors.as_data()
            return render(request, 'user/user_inc/publ_profile.html', {'form': form, 'form_errors': form_errors})


def logout_view(request):
    logout(request)
    return redirect('login')


def time_view(request):
    today = datetime.date.today()
    context = {
        'today': today
    }
    return render(request, 'advert_profile', context)
