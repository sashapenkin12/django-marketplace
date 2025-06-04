"""
Users app models.
"""
from django.db import models
from django.contrib.auth.models import User

from users.validators import validate_even, validate_length


def images_dir_path(instance: models.Model, filename: str) -> str:
    """
    Returns image path that bases on filename.

    Args:
        instance: The model instance whose image field will be saved
        filename: The name of the file.

    Returns:
        str: Formatted path with file name.
    """
    return 'media/images/{filename}'.format(
        filename=filename,
    )


class Image(models.Model):
    """
    Represents an image in marketplace system.

    Attributes:
        image: The image itself.
        content (str): The replacing content.
        category: One-to-one relationship to Category instance.
        subcategory: One-to-one relationship to Subcategory instance.
        profile: One-to-one relationship to Profile instance.
    """

    image = models.ImageField(
        upload_to=images_dir_path,
    )
    content = models.CharField(
        null=False,
        max_length=50,
    )
    category = models.OneToOneField(
        to='products.Category',
        on_delete=models.CASCADE,
        related_name='image',
        null=True,
    )
    subcategory = models.OneToOneField(
        to='products.Subcategory',
        on_delete=models.CASCADE,
        related_name='image',
        null=True,
    )
    profile = models.OneToOneField(
        to='Profile',
        on_delete=models.CASCADE,
        related_name='avatar',
        null=True,
        unique=False,
    )


class Profile(models.Model):
    """
    Represents user profile

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    Attributes:
        user: One-to-one relationship to User instance.
        fullName: The full name of the user.
        email: The email of the user.
        phone: The phone number of the user.
    """
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    fullName = models.CharField(max_length=100, null=False, verbose_name='Полное имя')
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона', unique=True)


class Payment(models.Model):
    """
    Represents payment

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    Attributes:
        number: Credit card number.
        name: Name on credit card.
        month: Expiration month.
        year: Expiration year.
        code: CVV/CVC code of the credit card.
    """
    number = models.IntegerField(
        null=False,
        validators=[validate_even, validate_length],
        verbose_name='Номер карты'
    )
    name = models.CharField(max_length=120, null=False, verbose_name='Имя на карте')
    month = models.CharField(max_length=2, null=False, verbose_name='Месяц')
    year = models.CharField(max_length=4, null=False, verbose_name='Год')
    code = models.CharField(max_length=3, null=False, verbose_name='CVV/CVC код')

    class Meta:
        verbose_name = 'Платежная система'
        verbose_name_plural = 'Платежные системы'


class SiteSetting(models.Model):
    """
    Represents site setting

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    Attributes:
        key: Setting key.
        value: Setting value.

    Methods:
        __str__:
            Represents setting key instead of the primary key.
    """
    key = models.CharField(max_length=100, unique=True, verbose_name="Ключ")
    value = models.TextField(verbose_name="Значение")

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return self.key
