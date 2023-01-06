# Generated by Django 4.1.4 on 2023-01-06 01:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('firstname', models.CharField(default='', max_length=255)),
                ('lastname', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=255)),
                ('password', models.CharField(default='', max_length=255)),
                ('contact', models.CharField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('category_name', models.CharField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('role', models.CharField(default='user', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='saloon',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('saloon_name', models.CharField(default='', max_length=255)),
                ('contact', models.CharField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(default='', upload_to='superadmin/')),
                ('city_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.city')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='section',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('section_name', models.CharField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='service',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('service_name', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default='', max_length=255)),
                ('price', models.FloatField(default=0)),
                ('image', models.ImageField(upload_to='superadmin/')),
                ('Service_Timing', models.DateTimeField(blank=True, null=True)),
                ('before_time', models.TimeField(blank=True, null=True)),
                ('service_type', models.CharField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='whitelistToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='', max_length=255)),
                ('user_agent', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('role_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
        migrations.CreateModel(
            name='subcategory',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('subcategory_name', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(upload_to='superadmin/')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='services_list',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('before_time', models.TimeField(blank=True, null=True)),
                ('service_type', models.CharField(default='', max_length=255)),
                ('price', models.FloatField(default=0)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('saloon_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.saloon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='saloon_image',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('image', models.ImageField(default='', upload_to='superadmin/')),
                ('saloon_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.saloon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='saloon',
            name='service_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.service'),
        ),
        migrations.CreateModel(
            name='package',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('registration_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(default='', max_length=255)),
                ('charges', models.IntegerField(default='')),
                ('packagesStatus', models.BooleanField(default='False', max_length=255)),
                ('packages', models.CharField(choices=[('monthly', 'monthly'), ('yearly', 'yearly')], default='monthly', max_length=20)),
                ('register_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='float_list',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('section_name', models.CharField(default='', max_length=255)),
                ('saloon_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.saloon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='employee',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('contact', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(upload_to='superadmin/')),
                ('Added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.role')),
                ('saloon_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.saloon')),
                ('service_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='country',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('Account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.country'),
        ),
        migrations.AddField(
            model_name='category',
            name='saloon_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.saloon'),
        ),
        migrations.CreateModel(
            name='appointment',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(default='', max_length=255)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('contact', models.CharField(default='', max_length=255)),
                ('facilty_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.service')),
                ('register_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('saloon_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.saloon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='account',
            name='role_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.role'),
        ),
    ]
