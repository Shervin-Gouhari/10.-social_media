# Generated by Django 4.2 on 2023-09-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='location',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
