from django.conf import settings
from django.db import models
from django.utils import timezone


# Это моя первая модель
class Post(models.Model):  # Объявление нового класса Post(наследуется от класса Model Django)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Настройки user-а из ForeignKey.
    # on_delete=models.CASCADE при удалении user-a, связанного с этим сообщением все его сообщения также будут удалены.
    title = models.CharField(max_length=200)  # Заголовок = наследуется символьное поле(максимальная длина = 200)
    text = models.TextField(max_length=700)  # Текст = наследуется текстовое поле.
    created_date = models.DateTimeField(default=timezone.now)  # Наследуется из models. Поле даты и
    # времени(устанавливает значение поля по умолчанию на текущую дату и время при создании публикации)
    published_date = models.DateTimeField(blank=True, null=True)  # blank=True: в формах поле может быть пустым.
    # Null=True: в базе данных поле может быть пустым. (Означает, что публикация может существовать в
    # черновике и не быть опубликованной).

    def publish(self):  # Метод публикации класса Post.
        self.published_date = timezone.now()  # Устанавливает в поле published_date текущую дату и время.
        self.save()  # Сохраняет изменения в бд, а не только в памяти.

    def __str__(self):  # Скрытай метод (с двойным подчёркиванием). Этот метод управляет тем, что должно отображаться
        # при попытке представить объект Post в виде строки (например, при выводе объекта Post).
        return self.title  # Возвращает title сообщения.
