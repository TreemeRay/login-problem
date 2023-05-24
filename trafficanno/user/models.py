from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    username = models.CharField(max_length=50, verbose_name='First Name', unique=False)
    country_of_residence = models.CharField(max_length=350,
                                            verbose_name='Country of residence')
    city = models.CharField(max_length=230, verbose_name='City')
    address = models.CharField(max_length=400, verbose_name='Address')
    email = models.EmailField(unique=True, verbose_name='Email')
    messenger_choices = [('Skype', 'Skype'), ('Telegram', "Telegram")]
    messenger = models.CharField(max_length=50, choices=messenger_choices, blank=True, null=False)
    messenger_nickname = models.CharField(max_length=270, verbose_name='Messenger nickname')
    is_advertiser = models.BooleanField(default=False, verbose_name='Is advertiser?')
    is_publisher = models.BooleanField(default=False, verbose_name='Is publisher?')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.username = slugify(self.first_name)
        return super(User, self).save(*args, **kwargs)


class AdvertiserAccount(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                verbose_name='User',
                                related_name='advertiser')
    short_desc = models.TextField(max_length=5000,
                                  verbose_name='Advertising campaign short description')
    bonus_code = models.CharField(max_length=350, verbose_name='Bonus code')
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'advertiser'
        verbose_name_plural = 'Advertisers'

    def __str__(self):
        return f'User: {self.user}'


class PublisherAccount(models.Model):
    TRAFFIC_AMOUNT = (
        (1, '<5k daily'),
        (2, '5-10k daily'),
        (3, '>10k daily')
    )
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                verbose_name='User',
                                related_name='publisher')
    website = models.TextField(max_length=5000,
                               verbose_name='Website')
    traffic_amount = models.PositiveSmallIntegerField(choices=TRAFFIC_AMOUNT,
                                                      verbose_name='Daily traffic amount')

    total_income = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    available_payout = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    usdt_trc = models.CharField(max_length=40, blank=True, null=True)
    custom = models.CharField(max_length=60, blank=True, null=True)
    wire_swift = models.CharField(max_length=50, blank=True, null=True)
    wire_comments = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    bank_address = models.CharField(max_length=40, blank=True, null=True)
    bank_country = models.CharField(max_length=15, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return f'User: {self.user}'
