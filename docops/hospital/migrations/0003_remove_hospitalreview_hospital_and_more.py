# Generated by Django 4.1.7 on 2023-05-26 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitalreview',
            name='hospital',
        ),
        migrations.RemoveField(
            model_name='hospitalreview',
            name='patient',
        ),
        migrations.DeleteModel(
            name='DoctorReview',
        ),
        migrations.DeleteModel(
            name='HospitalReview',
        ),
    ]