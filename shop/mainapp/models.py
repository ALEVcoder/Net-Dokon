from PIL import Image
import PIL
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



User = get_user_model()


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass



class LatestproductsManager:
    
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products

class LatestProducts:
    
    objects = LatestproductsManager()

class Category(models.Model):
	name = models.CharField(max_length=255, verbose_name='Ism kategoriyasi')
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name


class Product(models.Model):
    
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728
    
    
    class Meta:
        abstract = True
        
        
    category = models.ForeignKey(Category, verbose_name='kategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Naimovinoai')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Rasmlar')
    description = models.TextField(verbose_name='Opsani', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Narx')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Rasm formati tugri emas!')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Rasm formati tugri emas!')
        return image


class Notebook(Product):
    
    diagonal = models.CharField(max_length=255, verbose_name='Diaganol')
    display_type = models.CharField(max_length=255, verbose_name='tip display')
    processor_freq = models.CharField(max_length=255, verbose_name='Chastota protsessor')
    ram = models.CharField(max_length=255, verbose_name='Operativka')
    video = models.CharField(max_length=255, verbose_name='Vedio karta')
    time_without_charge = models.CharField(max_length=255, verbose_name='vreamiya rabota akumlyator')
    
    def __str__(self):
    		return "{} : {}".format(self.category.name, self.title)



class Smartphone(Product):
    
     
    diagonal = models.CharField(max_length=255, verbose_name='Diaganol')
    display_type = models.CharField(max_length=255, verbose_name='tip display')
    resolution = models.CharField(max_length=255, verbose_name='Razreshena erkrana')
    accum_volume = models.CharField(max_length=255, verbose_name='Obem Batariya')
    ram = models.CharField(max_length=255, verbose_name='Operativka')
    sd  = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Maksimaolniy obem bsravoy pamyatki')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Glavnaya camera')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='frontalnaya camera')
    
    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)



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

