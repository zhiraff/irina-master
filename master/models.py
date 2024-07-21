from django.db import models
from django.urls import reverse_lazy
from account.models import CustomUser
from django.core.validators import MinValueValidator

class MasterModel(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя мастера')
    surname = models.CharField(max_length=250, verbose_name='Фамилия мастера', blank=True, null=True)
    patronym = models.CharField(max_length=250, verbose_name='Отчество мастера', blank=True, null=True)
    city = models.CharField(max_length=250, verbose_name='Город мастера')
    is_active = models.BooleanField(default=True, verbose_name='Мастер активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f"{self.pk} {self.name} {self.surname} {self.city}"

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class ServiceModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE, related_name='services_by_master',
                              verbose_name='Мастер', limit_choices_to={'is_active': True})
    name = models.CharField(max_length=100, verbose_name='Услуга')
    description = models.CharField(max_length=250, verbose_name='Описание услуги', null=True, blank=True)
    cost = models.IntegerField(verbose_name='Базовая стоимость услуги', validators=[MinValueValidator(0)])

    is_active = models.BooleanField(verbose_name='Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f"{self.pk} {self.master.name} {self.name} {self.cost}"


class AvailableSlotsModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE, related_name='slots_by_master',
                              verbose_name='Мастер', limit_choices_to={'is_active': True})
    date = models.DateField(verbose_name='День')
    time = models.TimeField(verbose_name='Время')
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Слот'
        verbose_name_plural = 'Слоты'

    def __str__(self):
        return f"{self.pk} {self.date} {self.time} "


class ChoosenSlotsModel(models.Model):
    statuses = (
        ('registred', 'Зарегистировано'),
        ('aborted', 'Отклонено'),
        ('confirmed', 'Подтверждено'),
        ('done', 'Выполнено'),
    )
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE,
                               verbose_name='Мастер', limit_choices_to={'is_active': True})
    slot = models.ForeignKey(AvailableSlotsModel, on_delete=models.CASCADE,
                              verbose_name='Слот', limit_choices_to={'is_active': True})
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE,
                              verbose_name='Услуга', limit_choices_to={'is_active': True})
    status = models.CharField(choices=statuses, verbose_name='Статус записи', default='', max_length=100)
    name = models.CharField(max_length=250, verbose_name='Имя Клиента')
    phone = models.CharField(max_length=250, verbose_name='Контактный номер', blank=True, null=True)
    comment = models.CharField(max_length=250, verbose_name='Комментарий', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f"{self.pk} {self.name} {self.slot.date} {self.slot.time} {self.master.name}"


class AnketaMasterModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE,
                               verbose_name='Мастер', limit_choices_to={'is_active': True})
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    educations = models.TextField(verbose_name='Образование', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    def __str__(self):
        return f"{self.pk} {self.master.name} "


class PhotoMasterModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE,
                               verbose_name='Мастер', limit_choices_to={'is_active': True})
    picture = models.FileField(upload_to='masters/photo', verbose_name='Фото', blank=True, null=True)
    description = models.CharField(verbose_name='Название фото', max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Фотокарточка'
        verbose_name_plural = 'Фотокарточки'

    def __str__(self):
        return f"{self.pk} {self.master.name} "


class PortfolioMasterModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE,
                               verbose_name='Мастер', limit_choices_to={'is_active': True})
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE,
                               verbose_name='Услуга', limit_choices_to={'is_active': True})
    picture = models.FileField(upload_to='masters/portfolio', verbose_name='Фото', blank=True, null=True)
    description = models.CharField(verbose_name='Название фото', max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'

    def __str__(self):
        return f"{self.pk} {self.master.name} "
