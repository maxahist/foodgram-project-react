from django.contrib.auth.models import (
    AbstractUser,
    UserManager
)
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('first_name', username)
        extra_fields.setdefault('last_name', username)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('guest', 'Guest'),
        ('user', 'User')
    )
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=255,
                            default='user',
                            verbose_name='статус')

    username = models.CharField(max_length=255,
                                unique=True,
                                verbose_name='логин')

    password = models.CharField(max_length=255,
                                verbose_name='пароль')

    email = models.EmailField(max_length=255,
                              unique=True,
                              verbose_name='почта')

    first_name = models.CharField(max_length=50,
                                  verbose_name='имя')

    last_name = models.CharField(max_length=100,
                                 verbose_name='фамилия')

    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'user'

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='автор',
                               related_name='subscr',
                               on_delete=models.CASCADE)
    sub = models.ForeignKey(User,
                            verbose_name='подписчик',
                            related_name='subb',
                            on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        constraints = [models.UniqueConstraint(
            fields=['author', 'sub'],
            name='нельзя подписаться на себя'
        )]
