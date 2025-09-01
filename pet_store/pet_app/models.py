from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    usertype=models.CharField(max_length=200)
    
class Register(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    gender=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    
class Pet(models.Model):
    REGISTER=models.ForeignKey(Register,on_delete=models.CASCADE)
    pet_name=models.CharField(max_length=200)
    age=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='pet_images/')
    
    @property
    def get_image(self):
        return self.image.url if self.image else ''

    def __str__(self):
        return self.pet_name

class PetFoods(models.Model):
    REGISTER=models.ForeignKey(Register,on_delete=models.CASCADE)
    food_name=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='food_images/')
    
    @property
    def get_image(self):
        return self.image.url if self.image else ''

    def __str__(self):
        return self.food_name
    
class PetAccessories(models.Model):
    REGISTER=models.ForeignKey(Register,on_delete=models.CASCADE)
    accessories_name=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='accessories_images/')
    
    @property
    def get_image(self):
        return self.image.url if self.image else ''

    def __str__(self):
        return self.accessories_name

class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"{self.user.firstname}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return float(self.product.price) * self.quantity
    
    @property
    def product_type(self):
        return self.product.__class__.__name__.capitalize()

    @property
    def image(self):
        return self.product.get_image if hasattr(self.product, 'get_image') else ''

    def __str__(self):
        return f"{self.product} x {self.quantity}"

