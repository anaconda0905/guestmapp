# Generated by Django 3.0.8 on 2020-09-28 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200812_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='socialToken',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
