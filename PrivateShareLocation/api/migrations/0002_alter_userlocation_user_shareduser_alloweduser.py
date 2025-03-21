# Generated by Django 4.2.19 on 2025-03-17 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SharedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_viewed', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_users', to=settings.AUTH_USER_MODEL)),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner', 'shared_with')},
            },
        ),
        migrations.CreateModel(
            name='AllowedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_viewed', models.DateTimeField(auto_now=True, null=True)),
                ('allowed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_by', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner', 'allowed_to')},
            },
        ),
    ]
