# Generated by Django 3.2.16 on 2022-10-21 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('degreed2', '0015_degreed2learnerdatatransmissionaudit_api_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='degreed2learnerdatatransmissionaudit',
            name='content_title',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='degreed2learnerdatatransmissionaudit',
            name='progress_status',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='degreed2learnerdatatransmissionaudit',
            name='user_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]