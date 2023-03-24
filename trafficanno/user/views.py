from pyexpat.errors import messages

from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, UpdateView
from .forms import AdvertiserSignUpForm, PublisherSignUpForm, PasswordConfirm, EmailAuthenticationForm,  \
    ForgotPasswordForm
from django.core.mail import EmailMessage
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
        template = render_to_string('user/email_submitting.html', {'name': self.request.user.email})
        email = EmailMessage(
            'Email message activation',
            template,
            settings.EMAIL_HOST_USER,
            [self.request.user.email]
        )

        email.fail_silently = False
        email.send()

        return redirect('email_submit')


class PublisherRegistration(CreateView):
    model = User
    form_class = PublisherSignUpForm
    template_name = 'user/publ_registration.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        template = render_to_string('user/email_message.html', {'name': self.request.user.email})
        email = EmailMessage(
            'Email message activation',
            template,
            settings.EMAIL_HOST_USER,
            [self.request.user.email]
        )

        email.fail_silently = False
        email.send()
        return redirect('email_submit')


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
            return redirect('user/advert_registration.html')
        else:

            return render(self.request, 'user/login.html', {'form': form})


class ForgotPassword(View):
    def get(self, *args, **kwargs):
        form = ForgotPasswordForm()
        return render(self.request, 'user/forgot_password.html', {'form': form})

    def post(self,*args, **kwargs):
        form = ForgotPasswordForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if user:
                    template = 'user/forgot_password_message.html'
                    cont = {
                        'email': email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Trafficanno',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    msg_html = render_to_string(template, cont)
                    email = EmailMessage(
                        'Email message activation',
                        'Link:',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        msg_html
                    )
                    email.fail_silently = False
                    email.send()

            except (Exception,):
                print('Ошибка')

        return render(self.request, 'user/forgot_password.html', {'from': form})






