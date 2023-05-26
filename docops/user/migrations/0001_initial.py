# Generated by Django 4.1.7 on 2023-05-26 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import location_field.models.plain
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('HOSPITAL', 'Hospital'), ('PATIENT', 'Patient')], max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('patient_id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('dob', models.DateField()),
                ('pic', models.ImageField(blank=True, null=True, upload_to=user.models.PathAndRename('patient/'), verbose_name='Patient_Profile_Pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HospitalProfile',
            fields=[
                ('hospital_id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('hospital_name', models.CharField(blank=True, max_length=150)),
                ('address', models.CharField(blank=True, max_length=150)),
                ('website', models.CharField(blank=True, max_length=150)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('location', location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to=user.models.PathAndRename('hospital/'), verbose_name='Hospital_Profile_Pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hospital', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.user',),
            managers=[
                ('hospital', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.user',),
            managers=[
                ('patient', django.db.models.manager.Manager()),
            ],
        ),
    ]
