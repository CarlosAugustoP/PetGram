# Generated by Django 4.2.6 on 2023-12-12 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_demand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='title',
        ),
        migrations.AddField(
            model_name='demand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
