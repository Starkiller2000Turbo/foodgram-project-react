# Generated by Django 4.2.4 on 2023-08-09 04:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="favorites",
        ),
        migrations.RemoveField(
            model_name="user",
            name="followings",
        ),
        migrations.RemoveField(
            model_name="user",
            name="purchases",
        ),
        migrations.DeleteModel(
            name="Purchase",
        ),
    ]
