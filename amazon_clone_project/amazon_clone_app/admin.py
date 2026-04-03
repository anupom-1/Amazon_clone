from django.contrib import admin
from . import models

admin.site.register(models.CustomUser)
admin.site.register(models.Profile)
admin.site.register(models.ProductCategory)
admin.site.register(models.Product)
admin.site.register(models.Post)
admin.site.register(models.Rating)