# Generated by Django 5.2.1 on 2025-06-19 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WTM_app', '0004_companyrating_upgraderequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upgraderequest',
            old_name='requested_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='upgraderequest',
            name='approved_at',
        ),
        migrations.RemoveField(
            model_name='upgraderequest',
            name='status',
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='business_type',
            field=models.CharField(default='Waste Management', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='certifications',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='city',
            field=models.CharField(default='City Name', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='company_name',
            field=models.CharField(default='Company Name', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='contact_email',
            field=models.EmailField(default='email', max_length=50),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='contact_name',
            field=models.CharField(default='Primary Contact', max_length=255),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='contact_phone',
            field=models.CharField(default='none', max_length=20),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='country',
            field=models.CharField(default='Country Name', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='declined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='justification',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='num_employees',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='postal_code',
            field=models.CharField(default='Postal Code', max_length=20),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='privacy_agreed',
            field=models.BooleanField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='registration_number',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='service_areas',
            field=models.TextField(blank=True, default='Service Areas', null=True),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='state',
            field=models.CharField(default='State Name', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='street_address',
            field=models.CharField(default='none', max_length=255),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='sustainability_practices',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='tax_id',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='terms_agreed',
            field=models.BooleanField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='waste_type',
            field=models.CharField(default='none', max_length=255),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='upgraderequest',
            name='years_in_operation',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
