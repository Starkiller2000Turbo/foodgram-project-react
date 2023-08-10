from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from core.constants import EMAIL_FIELD_LENGTH, USER_FIELDS_LENGTH


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='логин',
        max_length=USER_FIELDS_LENGTH,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')],
    )
    email = models.EmailField(
        verbose_name='почта',
        max_length=EMAIL_FIELD_LENGTH,
        unique=True,
    )
    first_name = models.CharField(  # type: ignore[assignment]
        verbose_name='имя',
        max_length=USER_FIELDS_LENGTH,
    )
    last_name = models.CharField(  # type: ignore[assignment]
        verbose_name='фамилия',
        max_length=USER_FIELDS_LENGTH,
    )
    password = models.CharField(
        verbose_name='пароль',
        max_length=USER_FIELDS_LENGTH,
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username', 'email')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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
        related_name='followings',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='автор',
        related_name='followers',
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
