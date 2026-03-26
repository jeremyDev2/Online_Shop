from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Coupon(models.Model):

    code = models.CharField(max_length=50,unique=True)
    discount = models.IntegerField(
        #min/max accepted values
        validators = [MinValueValidator(0), MaxValueValidator(100)],
        help_text = 'Percentage value (o to 100)'
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()
    
    def __str__(self) -> str:
        return self.code
