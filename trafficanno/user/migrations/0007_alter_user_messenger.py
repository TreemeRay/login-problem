# Generated by Django 4.1.7 on 2023-05-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_messenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='messenger',
            field=models.CharField(blank=True, choices=[('Skype', 'Skype'), ('Telegram', 'Telegram')], max_length=50),
        ),
    ]