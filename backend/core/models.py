from django.db import models


class UserRecipeModel(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    class Meta:
        abstract = True
        default_related_name = 'user_recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_user',
            ),
        ]

    def __str__(self) -> str:
        """Задание текстового представления избранного.

        Returns:
            Строку вида 'Избранное <пользователь> содержит <рецепт>'
        """
        return ' '.join(
            [
                f'{self._meta.get_field("user").verbose_name}-{self.user},',
                f'{self._meta.get_field("recipe").verbose_name}-{self.recipe}',
            ],
        )
