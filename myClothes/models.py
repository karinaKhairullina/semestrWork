from django.db import models
from authorization.models import User


class Category(models.Model):
    """
    Модель категории.

    Args:
        models.Model: Базовый класс модели.

    Attributes:
        name (CharField): Название категории.

    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Возвращает строковое представление категории.

        Returns:
            str: Строковое представление категории.

        """
        return self.name



class Image(models.Model):
    """
    Модель изображения.

    Args:
        models.Model: Базовый класс модели.

    Attributes:
        image (ImageField): Изображение.

    """
    image = models.ImageField(upload_to='clothing_images/')


class Subcategory(models.Model):
    """
    Модель подкатегории.

    Args:
        models.Model: Базовый класс модели.

    Attributes:
        category (ForeignKey): Категория, к которой относится подкатегория.
        name (CharField): Название подкатегории.

    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Возвращает строковое представление подкатегории.

        Returns:
            str: Строковое представление подкатегории.

        """
        return self.name


class ClothingItem(models.Model):
    """
    Модель предмета одежды.

    Args:
        models.Model: Базовый класс модели.

    Attributes:
        user (ForeignKey): Пользователь, которому принадлежит предмет одежды.
        category (ForeignKey): Категория предмета одежды.
        subcategory (ForeignKey): Подкатегория предмета одежды (может быть пустым).
        images (ManyToManyField): Изображения, связанные с предметом одежды.
        description (TextField): Описание предмета одежды.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    images = models.ManyToManyField(Image)
    description = models.TextField()

    def __str__(self):
        """
        Возвращает строковое представление предмета одежды.

        Returns:
            str: Строковое представление предмета одежды.

        """
        return self.description


class Recommendation(models.Model):
    """
    Модель рекомендации.

    Args:
        models.Model: Базовый класс модели.

    Attributes:
        category (ForeignKey): Категория рекомендации.
        subcategory (ForeignKey): Подкатегория рекомендации.
        image (ImageField): Изображение рекомендации.
        description (TextField): Описание рекомендации.
        purchase_link (URLField): Ссылка на покупку рекомендации.

    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='recommendation_images/')
    description = models.TextField()
    purchase_link = models.URLField()

    def __str__(self):
        """
        Возвращает строковое представление рекомендации.

        Returns:
            str: Строковое представление рекомендации.

        """
        return self.description


class Outfit(models.Model):
    """
    Модель комплекта.

    Args:
        models.Model: Базовый класс модели.

    Attributes:
        user (ForeignKey): Пользователь, которому принадлежит комплект.
        name (CharField): Название комплекта.
        items (ManyToManyField): Предметы одежды, входящие в комплект.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(ClothingItem)

    def __str__(self):
        """
        Возвращает строковое представление комплекта.

        Returns:
            str: Строковое представление комплекта.

        """
        return self.name


