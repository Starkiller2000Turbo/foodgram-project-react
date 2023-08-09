from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(  # type: ignore[assignment]
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(  # type: ignore[assignment]
        verbose_name='Фамилия',
        max_length=150,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='username_email',
            ),
        ]

    def __str__(self) -> str:
        """Представление модели при выводе.

        Returns:
            Строка поля name, используемого для представления модели.
        """
        return self.username


class Following(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='followers',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='автор',
        related_name='followings',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='user_not_following',
            ),
        ]

    def __str__(self) -> str:
        """Задание текстового представления подписки.

        Returns:
            Строку вида 'Подписка <пользователь> на <автор>'
        """
        return f'Подписка {self.user} на {self.following}'


class Favorite(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        verbose_name='избранное',
        on_delete=models.CASCADE,
        related_name='favorited',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite',
            ),
        ]

    def __str__(self) -> str:
        """Задание текстового представления избранного.

        Returns:
            Строку вида 'Избранное <пользователь> содержит <рецепт>'
        """
        return f'Избранное {self.user} содержит {self.recipe}'
