from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.db import transaction
from .models import AdvertiserAccount, PublisherAccount
from django.forms import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

User = get_user_model()


class AdvertiserSignUpForm(UserCreationForm):
    short_desc = forms.CharField(label='Short description of your advertising campaign',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'rows': 3}))
    bonus_code = forms.CharField(label='Bonus code',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(
        label='I agree with my data processing and i accept Terms & Conditions and Privacy policy', required=True)
    receive_newsletter = forms.BooleanField(
        label='I agree to recieve special offers,financial,techinical and other helpful information', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country_of_residence', 'city',
                  'address', 'email', 'messenger', 'messenger_nickname', 'short_desc',
                  'bonus_code')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'messenger': forms.TextInput(attrs={'class': 'form-control'}),
            'messenger_nickname': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AdvertiserSignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

    def clean(self):
        self.cleaned_data['password1'] = 'Passoerdq213123f'
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_advertiser = True
        user.set_unusable_password()
        user.save()

        try:
            AdvertiserAccount.objects.create(user=user,
                                             short_desc=self.cleaned_data['short_desc'],
                                             bonus_code=self.cleaned_data['bonus_code'])
        except (Exception,):
            raise ValidationError('When creating advertiser account, something went wrong')

        return user


class PublisherSignUpForm(UserCreationForm):
    website = forms.CharField(label='Website',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    traffic_amount = forms.ChoiceField(choices=PublisherAccount.TRAFFIC_AMOUNT,
                                       label='Daily traffic amount',
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(
        label='I agree with my data processing and i accept Terms & Conditions and Privacy policy', required=True)
    receive_newsletter = forms.BooleanField(
        label='I agree to recieve special offers,financial,techinical and other helpful information', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country_of_residence', 'city',
                  'address', 'email', 'messenger', 'messenger_nickname',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'messenger': forms.TextInput(attrs={'class': 'form-control'}),
            'messenger_nickname': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(PublisherSignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

    def clean(self):
        self.cleaned_data['password1'] = 'Passoerdq2asdasdajsdjaidj13123f'
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_publisher = True
        user.is_active = False
        user.set_unusable_password()
        user.save()

        try:
            PublisherAccount.objects.create(user=user,
                                            website=self.cleaned_data['website'],
                                            traffic_amount=self.cleaned_data['traffic_amount'])
        except (Exception,):
            raise ValidationError('When creating advertiser account, something went wrong')

        return user


class PasswordConfirm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'password'}))


class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}))
