# Generated by Django 4.2.7 on 2023-12-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]