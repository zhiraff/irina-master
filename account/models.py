from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from datetime import date, timedelta

class CustomUser(AbstractUser):
    third_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    fio = models.CharField(max_length=350, verbose_name='ФИО', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    pass_expire_date = models.DateField(verbose_name='Дата истечения пароля', blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=15, blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # функция проверяет не истек ли срок действия пароля. True - истёк
    def expired_password(self):
        if self.pass_expire_date:
            return self.pass_expire_date <= date.today()
        else:
             return True

    # функция проверяет сколько дней осталось до истечения пароля. Число - количество дней, 0 - ещё много
    def notice_password(self):
        if self.pass_expire_date:
            remind_days = self.pass_expire_date - date.today()
            if remind_days.days < 5:
                return remind_days.days
            else:
                return 0
        else:
            return 0

    # функция продлевает срок действия пароля на 42 дня
    def add_life_password(self):
        if self.pass_expire_date:
            self.pass_expire_date = date.today() + timedelta(days=42)
        else:
            self.pass_expire_date = date.today() + timedelta(days=42)
        self.save()
        return ''

    def get_absolute_url(self):
        return reverse_lazy('user_detail')
