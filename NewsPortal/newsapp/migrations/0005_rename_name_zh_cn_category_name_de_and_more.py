# Generated by Django 4.0.5 on 2022-08-01 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0004_category_name_zh_cn_post_text_zh_cn_post_title_zh_cn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name_zh_CN',
            new_name='name_de',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text_zh_CN',
            new_name='text_de',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='title_zh_CN',
            new_name='title_de',
        ),
    ]
