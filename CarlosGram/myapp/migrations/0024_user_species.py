# Generated by Django 4.2.6 on 2023-12-31 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='species',
            field=models.CharField(blank=True, choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('fish', 'Fish'), ('rabbit', 'Rabbit'), ('hamster', 'Hamster'), ('turtle', 'Turtle'), ('horse', 'Horse'), ('snake', 'Snake'), ('lizard', 'Lizard'), ('pig', 'Pig'), ('monkey', 'Monkey'), ('other', 'Other')], max_length=10, null=True),
        ),
    ]
