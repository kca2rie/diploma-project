# Generated by Django 4.0.4 on 2022-06-05 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
