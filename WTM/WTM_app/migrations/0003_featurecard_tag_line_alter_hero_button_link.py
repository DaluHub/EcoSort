# Generated by Django 5.2.1 on 2025-06-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WTM_app', '0002_featurecard_hero'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurecard',
            name='tag_line',
            field=models.CharField(default='Smart Sorting Tagline', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hero',
            name='button_link',
            field=models.CharField(blank=True, null=True),
        ),
    ]
