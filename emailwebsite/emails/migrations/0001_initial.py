# Generated by Django 3.0.4 on 2020-04-11 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_data', models.TextField()),
                ('spam_data', models.TextField()),
            ],
        ),
    ]