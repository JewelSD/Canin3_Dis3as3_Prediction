# Generated by Django 5.0.2 on 2024-04-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appoint', '0005_alter_appointment_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doc_desc',
            field=models.CharField(default='-', max_length=500, null=True),
        ),
    ]
