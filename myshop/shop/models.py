from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True,null=True,blank=True)
    slug = models.SlugField(max_length = 200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])
    
    def __str__(self):
        return self.name


class label(models.Model):
    product_label = models.CharField(max_length=200)
    slug = models.SlugField(max_length = 200,unique=True)

    def __str__(self):
        return self.product_label

class Product_SubCategory(models.Model):
    name = models.CharField(max_length=200,db_index = True,null=True,blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True,null=True,blank=True)
    description = models.TextField(blank = True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete = models.CASCADE)
    cost_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    operation_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10,decimal_places=2,blank = True, null=True)
    image = models.ImageField(upload_to = 'product/%Y/%m/%d',blank=True, null=True)
    available = models.BooleanField(blank = True, null=True)
    dateOfEntry = models.DateTimeField(auto_now_add=True, null=True)
    expiryDate = models.DateTimeField(blank = True, null=True)
    size = models.DecimalField(max_digits = 10,decimal_places=3 ,blank=True, null=True)
    weight = models.DecimalField(max_digits = 10,decimal_places=3 ,blank = True, null=True)
    volume = models.DecimalField(max_digits = 10,decimal_places=3, blank = True, null=True)
    company_of_origin = models.CharField(max_length=500,blank = True, null=True)
    country_of_origin = models.CharField(max_length=500,blank = True, null=True)
    Product_Label = models.ManyToManyField(label,related_name='label',blank=True)


    class Meta:
        # ordering = ('name',)
        index_together = (('id','slug'),)
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory',args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=200,db_index = True,null=True,blank=True)
    slug = models.SlugField(max_length=200, db_index=True,null=True,blank=True)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'product/%Y/%m/%d',blank=True)
    cost_price = models.DecimalField(max_digits=10,decimal_places=2)
    operation_price = models.DecimalField(max_digits=10,decimal_places=2)
    selling_price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    dateOfEntry = models.DateTimeField(auto_now_add=True)
    expiryDate = models.DateTimeField()
    size = models.DecimalField(max_digits = 10,decimal_places=3 ,blank=True)
    weight = models.DecimalField(max_digits = 10,decimal_places=3 ,blank = True)
    volume = models.DecimalField(max_digits = 10,decimal_places=3 ,blank = True)
    company_of_origin = models.CharField(max_length=500,blank = True)
    country_of_origin = models.CharField(max_length=500,blank = True)
    Product_Labels = models.ManyToManyField(label,related_name='final_label',blank=True)
    category = models.ForeignKey(Product_SubCategory, related_name='final_products', on_delete = models.CASCADE)



    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory',args=[self.category.category.slug,self.category.slug])

    def __str__(self):
        return self.name


    