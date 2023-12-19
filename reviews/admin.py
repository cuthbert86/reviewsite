from django.contrib import admin
from reviews.models import Category, ContactSubmission, Profile, Review


# Register your models here.
admin.site.register(Category)
admin.site.register(ContactSubmission)
admin.site.register(Profile)
admin.site.register(Review)
