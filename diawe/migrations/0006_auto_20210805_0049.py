# Generated by Django 2.1.5 on 2021-08-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diawe', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='logpost',
            name='picture',
            field=models.ImageField(blank=True, upload_to='avatar/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='avatar/%Y%m%d/'),
        ),
    ]