# Generated by Django 3.2.16 on 2023-08-10 13:27

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    ),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='date joined',
                    ),
                ),
                (
                    'username',
                    models.CharField(
                        max_length=150,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^[\\w.@+-]+\\Z'
                            )
                        ],
                        verbose_name='логин',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=256, unique=True, verbose_name='почта'
                    ),
                ),
                (
                    'first_name',
                    models.CharField(max_length=150, verbose_name='имя'),
                ),
                (
                    'last_name',
                    models.CharField(max_length=150, verbose_name='фамилия'),
                ),
                (
                    'password',
                    models.CharField(max_length=150, verbose_name='пароль'),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('username', 'email'),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'following',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='followers',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='автор',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='followings',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddConstraint(
            model_name='following',
            constraint=models.UniqueConstraint(
                fields=('user', 'following'), name='unique_user_following'
            ),
        ),
        migrations.AddConstraint(
            model_name='following',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('user', django.db.models.expressions.F('following')),
                    _negated=True,
                ),
                name='user_not_following',
            ),
        ),
    ]
