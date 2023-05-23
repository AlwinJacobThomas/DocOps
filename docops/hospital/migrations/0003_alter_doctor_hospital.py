# Generated by Django 4.1.7 on 2023-05-23 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_hospitalprofile_location'),
        ('hospital', '0002_alter_doctor_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='user.hospital'),
        ),
    ]
