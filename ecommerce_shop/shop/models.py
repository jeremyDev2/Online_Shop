from django.db import models
from django.urls import reverse
from django.utils import translation
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(max_length=200, unique=True),
    )

    class Meta:
        ordering = ["translations__name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return str(self.safe_translation_getter("name", any_language=True))

    # the convention to retrieve the URL for a given object.
    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(TranslatableModel):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(max_length=200, unique=True),
        description=models.TextField(blank=True),
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    price = models.IntegerField()
    available = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["translations__name"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return str(self.safe_translation_getter("name", any_language=True))

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
