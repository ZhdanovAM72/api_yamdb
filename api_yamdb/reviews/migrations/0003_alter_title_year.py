# Generated by Django 3.2 on 2023-06-20 01:01

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230618_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, validators=[reviews.validators.validate_year], verbose_name='год выпуска'),
        ),
    ]
