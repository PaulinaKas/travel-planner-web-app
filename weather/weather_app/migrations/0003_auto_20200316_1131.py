# Generated by Django 2.2.6 on 2020-03-16 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0002_auto_20200316_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('list', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='weather_app.List')),
            ],
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
