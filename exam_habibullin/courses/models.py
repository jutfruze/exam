from django.db import models

#пользователь
class User(models.Model):
    surname = models.CharField('Фамилия', max_length=50)
    name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50, blank=True)
    login = models.CharField('Логин', max_length=50, unique=True)
    password = models.CharField('Пароль', max_length=100)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    def __str__(self):
        return f' {self.surname} {self.name}'
    
class Application(models.Model):
    COURSE_CHOICES = [
        ('bus', 'Автобус'),
        ('electrobus','Электробус'),
        ('tram','Трамвай'),
    ]

    PAYMENT_CHOICES = [
        ('cash','Наличные'),
        ('card', 'Карта'),
        ('online', 'Онлайн'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('learning', 'Идет обучение'),
        ('finished', 'Обучение завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course_type = models.CharField('Курс', max_length=20, choices=COURSE_CHOICES)
    payment_type = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES)
    preferred_date = models.DateField('Дата обучения')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.get_course_type_display()}'

#модель для отзыва
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    application = models.OneToOneField(Application, on_delete=models.CASCADE, verbose_name='Заявка')
    text = models.TextField('Отзыв')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    def __str__(self):
        return f' Отзыв от {self.user}'