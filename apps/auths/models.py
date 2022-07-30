from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
import datetime
from django.db.models import Q, QuerySet


class CustomUserManager(BaseUserManager):

    def create_user(self, email: str, password: str) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_special_user(self) -> QuerySet['CustomUser']:
        """Get special users after 2022.07.01"""
        DATE = datetime.date(2022, 7, 1)
        users: QuerySet[CustomUser] = self.filter(
            Q(is_staff=True) & Q(date_joined__gte=DATE)
        )
        return users

    def get_users_hobbies(self) -> list['CustomUser']:
        """Get users who have more than 3 hobbies"""
        HOBBIES_COUNT: int = 3
        users: QuerySet[CustomUser] = self.all()
        result: list[CustomUser] = []
        for user in users:
            user_hobbies: QuerySet[UserHobbies] = UserHobbies.objects.filter(
                user=user
            )
            if len(user_hobbies) >= HOBBIES_COUNT:
                result.append(user)
        return result

    def get_undeleted_users(self) -> QuerySet['CustomUser']:
        """Get undeleted users"""
        users: QuerySet[CustomUser] = self.filter(is_active=True)
        return users


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Почта/Логин',
        unique=True
    )
    number = models.CharField(
        'Номер телефона',
        max_length=11,
    )
    is_active: models.BooleanField(
        'Активность',
        default=True
    )
    is_staff = models.BooleanField(
        'Статус менеджера',
        default=False
    )

    data_joined = models.DateTimeField(
        'Время создания',
        default=timezone.now
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'data_joined',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserHobbies(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    hobbies = models.CharField(
        'Введите ваши хобби через заяптую',
        max_length=255
    )

    class Meta:
        verbose_name = 'Хобби'
        verbose_name_plural = 'Хобби'
