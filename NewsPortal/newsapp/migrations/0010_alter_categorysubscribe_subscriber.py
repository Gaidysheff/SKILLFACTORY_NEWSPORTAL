# Generated by Django 4.0.5 on 2022-09-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0009_remove_category_subscriber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorysubscribe',
            name='subscriber',
            field=models.EmailField(max_length=254),
        ),
    ]