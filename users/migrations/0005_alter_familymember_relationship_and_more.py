# Generated by Django 5.1.4 on 2025-01-08 23:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_managers_remove_customuser_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='relationship',
            field=models.CharField(choices=[('spouse', 'Spouse'), ('child', 'Child'), ('parent', 'Parent'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='user',
            field=models.ForeignKey(help_text='The user to whom this family member belongs.', on_delete=django.db.models.deletion.CASCADE, related_name='user_family_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
