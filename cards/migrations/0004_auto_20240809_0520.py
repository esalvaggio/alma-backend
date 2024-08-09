# Generated by Django 4.2.8 on 2024-08-09 05:20
from django.conf import settings
from django.db import migrations, models
from django.db import migrations

def delete_cards(apps, schema_editor):
    Card = apps.get_model('cards', 'Card')
    Card.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_card_percent_through'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.RunPython(delete_cards),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
