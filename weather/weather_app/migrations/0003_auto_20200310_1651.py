# Generated by Django 2.2.6 on 2020-03-10 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0002_travelplan'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TravelPlan',
        ),
        migrations.AddField(
            model_name='city',
            name='schedule_text',
            field=models.TextField(default='Text'),
        ),
    ]
