from django.db import models
from authorization.models import User
from myClothes.models import Outfit, Image
from django.utils import timezone


class Post(models.Model):
    """
    Модель для постов.

    Атрибуты:
        user (User): Пользователь, создавший пост.
        outfit (Outfit): Одежда, связанная с постом.
        title (str): Заголовок поста.
        create_date (datetime): Дата создания поста.
        text (str): Текст поста.
        images (ManyToManyField): Изображения, связанные с постом.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    images = models.ManyToManyField(Image)

    def __str__(self):
        """
        Возвращает строковое представление объекта Post.

        Если у поста есть заголовок, возвращает его.
        В противном случае возвращает пустую строку.

        Returns:
            str: Строковое представление объекта Post.
        """
        return self.title or ''


class Comment(models.Model):
    """
    Модель для комментариев к постам.

    Атрибуты:
        user (User): Пользователь, оставивший комментарий.
        post (Post): Пост, к которому оставлен комментарий.
        create_date (datetime): Дата создания комментария.
        text (str): Текст комментария.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    create_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=100)


class Like(models.Model):
    """
    Модель для лайков к постам.

    Атрибуты:
        user (User): Пользователь, поставивший лайк.
        post (Post): Пост, которому поставлен лайк.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
