# Generated by Django 4.1.5 on 2023-06-09 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_item_name_cart_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item_name',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='item_name',
            new_name='item',
        ),
    ]
