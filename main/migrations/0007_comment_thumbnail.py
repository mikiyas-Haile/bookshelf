# Generated by Django 3.2.9 on 2021-11-29 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
