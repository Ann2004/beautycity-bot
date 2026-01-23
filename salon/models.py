from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    name = models.CharField(
        verbose_name='ФИО',
        max_length=255
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} ({self.phone})'


class Salon(models.Model):
    name = models.CharField(
        verbose_name='Имя салона',
        max_length=255
    )
    address = models.TextField(
        verbose_name='Адрес салона'
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} ({self.address})'


class Service(models.Model):
    name = models.CharField(
        verbose_name='Название услуги',
        max_length=255
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    duration = models.PositiveIntegerField(
        verbose_name='Длительность (мин)'
    )

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(
        verbose_name='Имя мастера',
        max_length=255
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        verbose_name='Салон'
    )
    services = models.ManyToManyField(
        Service,
        verbose_name='Услуги',
        blank=True
    )

    def __str__(self):
        return self.name


class Promo(models.Model):
    code = models.CharField(
        verbose_name='Промокод',
        max_length=10,
        unique=True
    )
    discount_percent = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    def __str__(self):
        return self.code


class Appointment(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга'
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        verbose_name='Мастер'
    )
    appointment_date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')

    def __str__(self):
        return f'{self.client} — {self.service} ({self.appointment_date} {self.time})'


class Feedback(models.Model):
    feedback = models.TextField(
        verbose_name='Отзыв'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        verbose_name='Мастер',
        related_name='reviews'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Клиент',
        related_name='client_reviews'
    )

    def __str__(self):
        if self.feedback:
            return f'Отзыв от {self.created_at.strftime("%d.%m.%Y")}'
        return f'Отзыв #{self.id}'
