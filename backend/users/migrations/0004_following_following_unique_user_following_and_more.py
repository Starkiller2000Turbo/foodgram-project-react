# Generated by Django 4.2.3 on 2023-07-27 21:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Following",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="автор",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follower",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="following",
            constraint=models.UniqueConstraint(
                fields=("user", "following"), name="unique_user_following"
            ),
        ),
        migrations.AddConstraint(
            model_name="following",
            constraint=models.CheckConstraint(
                check=models.Q(("user", models.F("following")), _negated=True),
                name="user_not_following",
            ),
        ),
    ]