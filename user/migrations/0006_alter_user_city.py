# Generated by Django 4.2 on 2023-09-25 19:04

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('user', '0005_alter_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='country', chained_model_field='cities_light.Country', null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.city'),
        ),
    ]
