# Generated by Django 3.2 on 2024-01-24 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_rate', '0002_alter_cost_of_currency_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost_of_currency',
            name='value',
            field=models.FloatField(),
        ),
    ]