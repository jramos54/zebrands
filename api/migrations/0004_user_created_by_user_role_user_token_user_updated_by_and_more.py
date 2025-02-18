# Generated by Django 5.1.6 on 2025-02-16 20:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_productquery'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('super_admin', 'Super Admin'), ('admin', 'Admin'), ('anonymous', 'Anonymous')], default='anonymous', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
    ]
