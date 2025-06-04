from django.db import models


def product_images_dir_path(instance: 'ProductImage', filename: str) -> str:
    """
    Returns product image path that bases on filename and instance pk.

    Args:
        instance: The model instance whose image field will be saved
        filename: The name of the file.

    Returns:
        str: Formatted path with file name and product pk.
    """
    return 'media/products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )

class ProductImage(models.Model):
    """
    Represents a product image in marketplace system.

    Attributes:
        product: Which product instance represents.
        image: The image itself.
        content (str): The replacing content.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to=product_images_dir_path, verbose_name='Картинка')
    content = models.CharField(null=False, max_length=50, verbose_name='Альтернативная надпись')


class Product(models.Model):
    """
    Represents product

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    Attributes:
        title: Title of the product.
        description: Short description of the product.
        fullDescription: Full product description.
        price: Product price.
        freeDelivery: Is delivery of the product free or not.
        available: Is product available or not.
        index: Index of sorting (used to popularity of product).
        category: Which category product is associated with.
        count: Count of products (used in orders)
        date: Date the product was added.
        rating: Rating of a product.
        limited: Is product limited or not.
    """
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    description = models.CharField(max_length=50, null=False, verbose_name='Описание')
    fullDescription = models.TextField(max_length=1000, null=False, verbose_name='Полное описание')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    available = models.BooleanField(default=True, verbose_name='Доступность')
    index = models.IntegerField(default=1, null=False, verbose_name='Индекс сортировки')
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        null=True,
    )
    count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    limited = models.BooleanField(default=False, verbose_name='Лимитированный')

    def __str__(self):
        return self.title

class Category(models.Model):
    """
    Represents category

    Attributes:
        title: Title of the category.

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    """
    title = models.CharField(max_length=30, null=False, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    """
    Represents subcategory

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    Attributes:
        title: Title of the subcategory.
        category: Which category is related to the subcategory

    """
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    title = models.CharField(max_length=30, null=False, verbose_name='Название')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='subcategories',
                                 verbose_name='Категория')

    def __str__(self):
        return self.title

class Specification(models.Model):
    """
    Represents specification

    Meta:
        verbose_name: representing name of model.
        verbose_name_plural: plural form of verbose_name.

    Attributes:
        product: What product this specification describe.
        name: Specification name.
        value: Specification value.

    """
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', verbose_name='Товар')
    name = models.CharField(max_length=30, verbose_name='Имя')
    value = models.CharField(max_length=40, verbose_name='Значение')

class Tag(models.Model):
    """
    Represents tag

    Meta:
        verbose_name: representing name of the model.
        verbose_name_plural: plural form of the verbose_name.

    Attributes:
        name: Name of the tag.
        products: Which products are marked with this tag.
        category: Which category is related to the tag.
    """
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=20, null=False, verbose_name='Название')
    products = models.ManyToManyField(Product, related_name='tags', verbose_name='Товары')
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    Represents product review.

    Meta:
        verbose_name: representing name of the model.
        verbose_name_plural: plural form of the verbose_name.

    Attributes:
        author: Review author name.
        email: Review author email.
        text: Content of the review.
        rate: Review product rate.
        date: When the review was published.
        product: What product does this review describe.
    """
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    author = models.CharField(max_length=30, verbose_name='Автор')
    email = models.EmailField()
    text = models.TextField(max_length=500, verbose_name='Текст')
    rate = models.IntegerField(verbose_name='Оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')


class Sale(models.Model):
    """
    Represents product sale.

    Meta:
        verbose_name: representing name of the model.
        verbose_name_plural: plural form of the verbose_name.

    Attributes:
        salePrice: New reduced price.
        dateFrom: When does this sale starts.
        dateTo: When does this sale ends.
        product: What product is on sale.
    """
    class Meta:
        verbose_name = 'Распродажа'
        verbose_name_plural = 'Распродажи'

    salePrice = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена по скидке')
    dateFrom = models.CharField(max_length=50, null=False, verbose_name='Начало распродажи')
    dateTo = models.CharField(max_length=50, null=False, verbose_name='Конец распродажи')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='sales', verbose_name='Товар')
