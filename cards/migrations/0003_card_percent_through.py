# Generated by Django 4.2.8 on 2024-04-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_alter_card_essay'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='percent_through',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
