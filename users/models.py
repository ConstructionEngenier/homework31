from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


USER_MIN_AGE = 9


def check_birth_date(value: date):
    user_age = relativedelta(date.today(), value).years
    if user_age < USER_MIN_AGE:
        raise ValidationError(
            '%(value)s too small',
            params={'value': user_age}
        )


class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLES = [
        (MEMBER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    ]

    role = models.CharField(max_length=13, choices=ROLES, default="member")
    age = models.PositiveIntegerField(null=True)
    birth_date = models.DateField(validators=[check_birth_date], null=True)
    email = models.EmailField(unique=True, null=True)
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
