from django.db import models

class Categoty(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering=["name"]
        indexes=[models.Index(fields=["name"])]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    
    category = models.ForeignKey(Categoty,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank = True)
    description = models.TextField(blank=True)
    price = models.IntegerField(max_length=6)
    available = models.BooleanField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


    class Meta:
        ordering = ['name']
        indexes=[models.Index(fields=['id', 'slug']),
                 models.Index(fields=['name']),
                 models.Index(fields=['-created']),]

    def __str__(self) -> str:
        return str(self.name)
