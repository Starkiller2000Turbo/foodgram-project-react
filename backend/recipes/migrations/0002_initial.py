# Generated by Django 3.2.16 on 2023-08-09 17:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='recipes',
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор',
            ),
        ),
        migrations.AddField(
            model_name='purchase',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='buyers',
                to='recipes.recipe',
                verbose_name='избранное',
            ),
        ),
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='purchases',
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('name', 'measurement_unit')},
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='favorited',
                to='recipes.recipe',
                verbose_name='избранное',
            ),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='favorites',
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='recipetag',
            unique_together={('tag', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='recipeingredient',
            unique_together={('ingredient', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('user', 'recipe')},
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_user_favorite'
            ),
        ),
    ]
