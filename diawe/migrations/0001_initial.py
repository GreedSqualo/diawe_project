# Generated by Django 2.1.5 on 2021-08-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
