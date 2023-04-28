# Generated by Django 4.1.7 on 2023-04-28 09:52

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalprofile',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.PathAndRename('hospital/'), verbose_name='Hospital_Profile_Pic'),
        ),
    ]
