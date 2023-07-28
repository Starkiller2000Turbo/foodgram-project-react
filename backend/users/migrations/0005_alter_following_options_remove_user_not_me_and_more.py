# Generated by Django 4.2.3 on 2023-07-28 21:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_following_following_unique_user_following_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="following",
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
        migrations.RemoveConstraint(
            model_name="user",
            name="not_me",
        ),
        migrations.AddField(
            model_name="user",
            name="followings",
            field=models.ManyToManyField(
                related_name="followers",
                through="users.Following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
