# Generated by Django 4.2.3 on 2023-07-27 18:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0009_rename_amounts_recipeingredient_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredient",
            name="amount",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
