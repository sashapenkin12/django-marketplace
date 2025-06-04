from django.db import models

class Order(models.Model):
    """
    Represents order.

    Meta:
        verbose_name: representing name of the model.
        verbose_name_plural: plural form of the verbose_name.

    Attributes:
        date: When order was created.
        products: What products does this order contains.
        fullName: Customer full name.
        email: Customer e-mail.
        phone: Customer phone number.
        city: Customer living city.
        address: Address of the delivery.
        deliveryType: Type of the delivery (free or not)
        paymentType: Type of the payment.
        status: Current order status.
    """
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    products = models.ManyToManyField('products.Product', related_name='orders', verbose_name='Товары')
    fullName = models.CharField(max_length=100, null=True, verbose_name='Полное имя')
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=15, null=True, verbose_name='Город')
    address = models.CharField(max_length=40, null=True, verbose_name='Адрес')
    deliveryType = models.IntegerField(null=True, default=0, verbose_name='Тип доставки')
    paymentType = models.IntegerField(null=True, default=0, verbose_name='Тип платежа')
    status = models.IntegerField(null=True, default=0, verbose_name='Статус')
