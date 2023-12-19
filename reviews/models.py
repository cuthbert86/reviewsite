from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    average_cost = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    product_photo = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f'[{self.category}] {self.name}'

    @property
    def get_number_of_reviews(self):
        return self.review_set.count()

    @property
    def get_average_rating(self):
        return (
            self
            .review_set
            .aggregate(
                Avg('rating')
            )
            ['rating__avg']
        )


class Review(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        help_text='Score 0-10',
        validators=[MaxValueValidator(10)],
    )
    description = models.TextField()
    user = models.ForeignKey(to='reviews.Profile', on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review #{self.pk} for {self.product.name}'


class Profile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    photo = models.ImageField(null=True, blank=True, upload_to='user_photographs')

    def __str__(self):
        return self.user.username


class ContactSubmission(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()

    def __str__(self):
        return f'{self.datetime} - {self.subject}'
