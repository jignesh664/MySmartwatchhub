# Generated by Django 3.0 on 2021-03-08 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'male'), ('F', 'female')], default=2, max_length=2),
            preserve_default=False,
        ),
    ]
