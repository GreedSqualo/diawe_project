# Generated by Django 2.1.5 on 2021-08-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diawe', '0006_auto_20210805_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logpost',
            name='picture',
            field=models.ImageField(blank=True, upload_to='avatar/%Y%m%d/'),
        ),
    ]
