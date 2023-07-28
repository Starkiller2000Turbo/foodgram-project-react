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
        blank=True,
        null=True,
    )
    last_name = models.CharField(  # type: ignore[assignment]
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        null=True,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='username_email',
            ),
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='not_me',
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
        related_name='follower',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='автор',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
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
            Строку вида 'подписка <имя пользователя> на <имя автора>'
        """
        return f'подписка {self.user} на {self.following}'
