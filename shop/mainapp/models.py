from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
User = get_user_model()
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=255, verbose_name='Ism kategoriyasi')
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category, verbose_name='kategory', on_delete=models.CASCADE)
	title = models.CharField(max_length=255, verbose_name='Naimovinoai')
	slug = models.SlugField(unique=True)
	image = models.ImageField(verbose_name='Rasmlar')
	description = models.TextField(verbose_name='Opsani', null=True)
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Narx')

	def __str__(self):
		return self.title


class CartProduct(models.Model):
	user = models.ForeignKey('Customer', verbose_name='Pokipaytel', on_delete=models.CASCADE)
	cart = models.ForeignKey('Cart', verbose_name='Korzinka', on_delete=models.CASCADE, related_name='related_products')
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object =  GenericForeignKey('content_type', 'object_id')
	qty = models.PositiveIntegerField(default=1)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Obshe narx')

	def __str__(self):
		return "Produkt: {} (dlya Korzinka)".format(self.product.title)


class Cart(models.Model):


	owner = models.ForeignKey('Customer', verbose_name='Vladelsiya', on_delete=models.CASCADE)
	products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
	total_product = models.PositiveIntegerField(default=8)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Obshe Narx')



	def __str__(self):
		return str(self.id)
		

class Customer(models.Model):
	user = models.ForeignKey(User, verbose_name='Polizavatel', on_delete=models.CASCADE)
	phone = models.CharField(max_length=28, verbose_name='Nomer Phone')
	address = models.CharField(max_length=255, verbose_name='Adres')

	def __str__(self):
		return "Pokupatel: {} {}".format(self.user.first_name, self.user.last_name)

class Specification(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	name = models.CharField(max_length=255, verbose_name='Tovor ismi va malumoti')

	def __str__(self):
		return "Tovor malumoti: {}".format(self.name)