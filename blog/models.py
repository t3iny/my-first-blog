from django.conf import settings
from django.db import models
from django.utils import timezone


# Это моя первая модель
class Post(models.Model):  # Объявление новой модели Post(наследуется от класса Model Django)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Настройки user-а из ForeignKey.
    # on_delete=models.CASCADE при удалении user-a, связанного с этим сообщением все его сообщения также будут удалены.
    title = models.CharField(max_length=200)  # Заголовок = наследуется символьное поле(НЕ БОЛЬШЕ 200).
    text = models.TextField(max_length=700)  # Текст = наследуется текстовое поле(НЕ БОЛЬШЕ 700).
    created_date = models.DateTimeField(default=timezone.now)  # Наследуется из models. Поле даты и
    # времени(устанавливает значение поля по умолчанию на текущую дату и время при создании публикации).
    published_date = models.DateTimeField(blank=True, null=True)  # blank=True: в формах поле может быть пустым.
    # Null=True: в базе данных поле может быть пустым. (Означает, что публикация может существовать в
    # черновике и не быть опубликованной).

    def publish(self):  # Метод публикации класса Post.
        self.published_date = timezone.now()  # Устанавливает в поле published_date текущую дату и время.
        self.save()  # Сохраняет изменения в бд, а не только в памяти.

    def __str__(self):  # Скрытый метод (с двойным подчёркиванием). Этот метод управляет тем, что должно отображаться
        # при попытке представить объект Post в виде строки (например, при выводе объекта Post).
        return self.title  # Возвращает title сообщения.


class Comment(models.Model):  # Объявление новой модели Comment, наследуемую от (Model).
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")  # С помощью FK связываем
    # C моделью Post (если она существует). on_delete=models.CASCADE: Как я понял если Post удаляется, то и комменты.
    # related_name="comments" Тобиш покажет все связанные комментарии в публикации.
    author_name = models.CharField(verbose_name="Автор комментария", max_length=100)  # Поле автора в 100 символов.
    text = models.TextField(verbose_name="Текс комментария", max_length=700)  # Текст комментария.
    created_date = models.DateTimeField(default=timezone.now)  # DateTimeField команда сохраняет как дату, так и время.
    # default=timezone.now: Тобиш по умолчанию равно времени создания.
    is_deleted = models.BooleanField(verbose_name="Видимость статьи", default=False, null=True)  # Флаг для удаления.

    def __str__(self):  # То что отображается
        author_display = self.author_name if self.author_name else "Аноним"  # Если имя не указано, выставить Аноним.
        return f"Комментарий {author_display} в '{self.post.title}': {self.text[:50]}..."  # Сократил для удобства.


class Like(models.Model):
    pass
