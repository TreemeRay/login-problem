# Generated by Django 4.1.7 on 2023-05-23 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_messenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='messenger',
            field=models.CharField(blank=True, choices=[('option1', 'Skype'), ('option2', 'Telegram')], default='option2', max_length=50),
        ),
    ]