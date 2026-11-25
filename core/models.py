from django.db import models
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import CustomUser
# Create your models here.
class OfferProduct(models.Model):
    title=models.CharField(max_length=200)
    desc=CKEditor5Field('Text', config_name='extends')
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_available=models.BooleanField(default=True)
    image=CloudinaryField("images")
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    desc=CKEditor5Field('Text', config_name='extends')
    image=CloudinaryField("product_images")
    mark_price=models.DecimalField(max_digits=10,decimal_places=2)
    discount_percent=models.DecimalField(max_digits=4,decimal_places=2)
    price=models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #price=100*(1-10/100) --> 100*0.9 --->90
    #mark_price*(1-discount_percent/100)

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        self.price=self.mark_price*(1-self.discount_percent/100)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    image=CloudinaryField('product_image')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

class Review(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveSmallIntegerField()
    feedback=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)