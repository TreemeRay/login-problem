from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm
from django.db import transaction
from .models import AdvertiserAccount, PublisherAccount
from django.forms import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

User = get_user_model()


class AdvertiserSignUpForm(UserCreationForm):
    short_desc = forms.CharField(label='Short description of your advertising campaign',
                                 widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': 3}))
    bonus_code = forms.CharField(label='Bonus code',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    agree_privacy = forms.BooleanField(
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
            'messenger': forms.Select(attrs={'class': 'form-control'}),
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
    agree_privacy = forms.BooleanField(
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
            'messenger': forms.Select(attrs={'class': 'form-control'}),
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
        user.set_unusable_password()
        user.save()

        try:
            PublisherAccount.objects.create(user=user,
                                            website=self.cleaned_data['website'],
                                            traffic_amount=self.cleaned_data['traffic_amount'])
        except (Exception,):
            raise ValidationError('When creating advertiser account, something went wrong')

        return user


class PasswordConfirm(forms.Form):
    new_password1 = forms.CharField(
        label=_("Set Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'password'}))


class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}))


class ResetSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "form-control"}),
    )


class PublProfileForm(forms.ModelForm):
    website = forms.CharField(label='Website',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    traffic_amount = forms.ChoiceField(choices=PublisherAccount.TRAFFIC_AMOUNT,
                                       label='Daily traffic amount',
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country_of_residence', 'city',
                  'address', 'email', 'messenger', 'messenger_nickname',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': True}),
            'messenger': forms.TextInput(attrs={'class': 'form-control'}),
            'messenger_nickname': forms.TextInput(attrs={'class': 'form-control'})

        }


class AdvertProfileForm(forms.ModelForm):
    short_desc = forms.CharField(label='Short description of your advertising campaign',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'rows': 3, 'disabled': True}))
    bonus_code = forms.CharField(label='Bonus code',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country_of_residence', 'city',
                  'address', 'email', 'messenger', 'messenger_nickname', 'short_desc',
                  'bonus_code')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': True}),
            'messenger': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'messenger_nickname': forms.TextInput(attrs={'class': 'form-control', 'disabled': True})
        }


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


