from django.conf import settings
from django.db import models
from django.utils import timezone


# Это моя первая модель
# todo это круто !
# todo я бы таки ограничил поле text количество символов. Иначе могем словить текст из 524288 символов ))
# todo а давай теперь сделаем вторую твою модель. Есть посты, но мы хотим знать мнение подписчиков !
# todo пора нам делать комментарии !
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
