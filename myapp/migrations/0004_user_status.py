# Generated by Django 3.0 on 2021-03-10 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default='inactive', max_length=100),
        ),
    ]
