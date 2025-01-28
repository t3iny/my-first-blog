from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="", max_length=200)
    text = models.TextField(verbose_name="", max_length=700)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to="post_images", null=True, blank=True, verbose_name='',)


    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(verbose_name="Добавьте свой комментарий:", max_length=100)
    text = models.TextField(verbose_name="", max_length=700)
    created_date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(verbose_name="", default=False, null=True)


    def __str__(self):
        author_display = self.author_name if self.author_name else "Аноним"
        return f"{author_display}:'{self.post.title}':{self.text[:50]}..."
