# Generated by Django 5.1.4 on 2025-02-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0023_groombrideinfo_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='groombrideinfo',
            name='experience',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
