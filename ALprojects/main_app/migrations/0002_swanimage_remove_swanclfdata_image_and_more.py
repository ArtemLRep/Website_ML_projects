# Generated by Django 4.2.4 on 2023-10-19 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwanImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='swan_classification/photos/')),
            ],
        ),
        migrations.RemoveField(
            model_name='swanclfdata',
            name='image',
        ),
        migrations.AddField(
            model_name='swanclfdata',
            name='image_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.swanimage'),
        ),
    ]
