# Generated by Django 4.1.7 on 2023-05-27 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='user.hospital'),
        ),
    ]
