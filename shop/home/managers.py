from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(access = True)
    
class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(access = True)
    
class FeatureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(access = True)