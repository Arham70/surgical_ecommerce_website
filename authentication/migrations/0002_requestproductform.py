# Generated by Django 4.2.7 on 2023-11-30 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestProductForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNo', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('companyName', models.CharField(max_length=100)),
                ('productName', models.CharField(max_length=100)),
                ('detail', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
