# Generated by Django 3.1.3 on 2021-10-19 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_board_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='modefy_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
