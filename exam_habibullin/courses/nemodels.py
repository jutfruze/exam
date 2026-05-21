class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    application = models.OneToOneField(Application, on_delete=models.CASCADE, verbose_name='Заявка')
    text = models.TextField('Отзыв')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    def __str__(self):
        return f'Отзыв от {self.user}'