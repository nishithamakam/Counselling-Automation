# Generated by Django 4.2.1 on 2023-06-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0003_alter_counsellor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='counsellor',
            name='c_id',
            field=models.IntegerField(default=0),
        ),
    ]
