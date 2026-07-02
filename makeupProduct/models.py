from django.db import models

#name of the product
#description of the product
#price of the product
#image of the product
#owner of the product (foreign key to the user model)
class MakeupProduct(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField()
    colour = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='makeup_products/')
    owner = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE, related_name='products')
    def __str__(self):
        return self.name

# Create your models here.