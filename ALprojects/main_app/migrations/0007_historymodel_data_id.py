# Generated by Django 4.2.4 on 2023-10-20 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_rename_user_id_swansegdata_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='historymodel',
            name='data_id',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
