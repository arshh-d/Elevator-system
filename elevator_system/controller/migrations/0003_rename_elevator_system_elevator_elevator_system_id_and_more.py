# Generated by Django 4.1.5 on 2023-01-26 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("controller", "0002_alter_elevatorsystem_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="elevator",
            old_name="elevator_system",
            new_name="elevator_system_id",
        ),
        migrations.RenameField(
            model_name="elevatorsystem",
            old_name="id",
            new_name="elevator_system_id",
        ),
    ]