# Generated by Django 4.1.7 on 2023-05-24 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_hospitalprofile_location'),
        ('hospital', '0003_alter_doctor_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.patient'),
        ),
    ]