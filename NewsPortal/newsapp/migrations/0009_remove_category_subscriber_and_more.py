# Generated by Django 4.0.5 on 2022-09-01 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsapp', '0008_rename_subscriber_through_categorysubscribe_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscriber',
        ),
        migrations.RemoveField(
            model_name='categorysubscribe',
            name='category',
        ),
        migrations.AddField(
            model_name='categorysubscribe',
            name='categorySubscribed',
            field=models.ManyToManyField(to='newsapp.category'),
        ),
        migrations.AlterField(
            model_name='categorysubscribe',
            name='subscriber',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
