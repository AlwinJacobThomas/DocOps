# Generated by Django 4.1.7 on 2023-05-27 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('coreapp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_hospital', to='user.hospital'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_patient', to='user.patient'),
        ),
    ]
