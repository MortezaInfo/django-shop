from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, IpAddress
from .managers import ProductManager, CommentManager, FeatureManager


class Category(models.Model):
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="scategory",
        null=True,
        blank=True,
    )
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = (
            "sub_category__id",
            "name",
        )
        verbose_name = "category"
        verbose_name_plural = "categoreis"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:category_detail", args=[self.slug])

    def sub_count(self):
        return self.products.filter(access=True).count()


class Brands(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = (
            "name",
            "id",
        )
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:category_detail", args=[self.slug])

    


class ProductFeatures(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    access = models.BooleanField(default=False)
    admin_objects = models.Manager()
    objects = FeatureManager()
    class Meta:
        ordering = ("-name",)

    def __str__(self) -> str:
        return self.name
    


class ProductHit(models.Model):
    product = models.ForeignKey('Products', on_delete = models.CASCADE)
    ip_address = models.ForeignKey(IpAddress, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)


class Products(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userproducts", default = 1
    )
    category = models.ManyToManyField(Category, related_name="products")
    pfeature = models.ManyToManyField(
        ProductFeatures, related_name="pfeature", default=None
    )
    brand = models.ForeignKey(Brands, on_delete = models.CASCADE, related_name = 'brands', blank=True, null = True, default=None)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    star = models.IntegerField(default=0)
    discount = models.IntegerField(blank=True, null=True, default=None)
    available = models.BooleanField(default=True)
    hits = models.ManyToManyField(IpAddress,through = 'ProductHit' , blank=True, related_name="hits")
    comment = GenericRelation("Comment")
    vote = GenericRelation("Vote")
    access = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    admin_objects = models.Manager()
    objects = ProductManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def product_like(self):
        return self.vote.filter(like=True).count()

    def product_dislike(self):
        return self.vote.filter(like=False).count()

    def get_total_price(self):
        if self.discount:
            discount_price = ((100 - self.discount) / 100) * self.price
            return int(discount_price)
        else:
            return self.price


class ProductImageis(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="productimage"
    )
    images = models.ImageField()

    class meta:
        db_table = "product_images"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomments")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")  # in views
    reply = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        related_name="rcomments",
        blank=True,
        null=True,
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    vote = GenericRelation("Vote")
    created = models.DateTimeField(auto_now_add=True)
    access = models.BooleanField(default=False)

    admin_objects = models.Manager()
    objects = CommentManager()

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"

    def comment_like(self):
        return self.vote.filter(like=True).count()

    def comment_dislike(self):
        return self.vote.filter(like=False).count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    like = models.BooleanField(default=None, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return f"{self.user} liked by {self.content_object} id {self.object_id}"
