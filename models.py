from django.contrib.auth.models import User
from django.db import models
import json
from bulk_update.manager import BulkUpdateManager

SHORT_TEXT_LEN = 1000

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > SHORT_TEXT_LEN:
            return self.text[:SHORT_TEXT_LEN]
        else:
            return self.text


class Comment(models.Model):
    text = models.TextField()
    article = models.ForeignKey(Article)


class OcLanguage(models.Model):
    language = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=5)
    locale = models.CharField(max_length=255)
    image = models.CharField(max_length=64)
    directory = models.CharField(max_length=32)
    sort_order = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oc_language'


class OcProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=64)
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=64)
    upc = models.CharField(max_length=12)
    ean = models.CharField(max_length=14)
    jan = models.CharField(max_length=13)
    isbn = models.CharField(max_length=17)
    mpn = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    quantity = models.IntegerField(default=0)
    stock_status_id = models.IntegerField(default=0)
    image = models.CharField(max_length=255, blank=True, null=True)
    manufacturer_id = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    points = models.IntegerField(default=0)
    tax_class_id = models.IntegerField(default=0)
    date_available = models.DateField(auto_now_add=True)
    weight = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    weight_class_id = models.IntegerField(default=0)
    length = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    width = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    length_class_id = models.IntegerField(default=0)
    subtract = models.IntegerField(default=0)
    minimum = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    #description = models.ManyToManyField(OcProductDescription)

    class Meta:
        managed = False
        db_table = 'oc_product'


class OcProductDescription(models.Model):
    product = models.ForeignKey(OcProduct, primary_key=True)
    language_id = models.IntegerField(OcLanguage)
    name = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.TextField()
    meta_title = models.CharField(max_length=255)
    meta_h1 = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=255)
    meta_keyword = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oc_product_description'
        unique_together = (('product', 'language_id'),)


class OcProductImage(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(OcProduct)
    image = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'oc_product_image'


class OcProductToStore(models.Model):
    product = models.ForeignKey(OcProduct)
    store_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oc_product_to_store'
        unique_together = (('product', 'store_id'),)


class OcCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(default=0)
    top = models.IntegerField(default=0)
    column = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(OcProduct, through='OcProductToCategory')

    class Meta:
        managed = False
        db_table = 'oc_category'


class OcCategoryDescription(models.Model):
    category = models.ForeignKey(OcCategory, primary_key=True)
    language_id = models.IntegerField(OcLanguage)
    name = models.CharField(max_length=255)
    description = models.TextField()
    meta_title = models.CharField(max_length=255)
    meta_h1 = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=255)
    meta_keyword = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oc_category_description'
        unique_together = (('category', 'language_id'),)


class OcProductToCategory(models.Model):
    product = models.ForeignKey(OcProduct)
    category = models.ForeignKey(OcCategory)
    main_category = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'oc_product_to_category'
        unique_together = (('product', 'category'),)


class OcCategoryToStore(models.Model):
    category = models.ForeignKey(OcCategory)
    store_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oc_category_to_store'
        unique_together = (('category', 'store_id'),)


class OcCategoryPath(models.Model):
    category = models.ForeignKey(OcCategory)
    path_id = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'oc_category_path'
        unique_together = (('category', 'path_id'),)


class Product(models.Model):
    category = models.CharField(max_length=50)
    url = models.CharField(max_length=250)
    description = models.TextField()
    images = models.TextField()
    title = models.CharField(max_length=255)
    cost_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    item_code = models.CharField(max_length=50, default=0)
    sku = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    is_parse = models.IntegerField(default=0)
    is_difference = models.IntegerField(default=0)

    objects = BulkUpdateManager()

    def images_list(self):
        return json.loads(self.images)

    class Meta:
        managed = False
        db_table = 'product'


class DifferenceProduct(models.Model):
    category = models.CharField(max_length=50)
    url = models.CharField(max_length=250)
    description = models.TextField()
    images = models.TextField()
    title = models.CharField(max_length=255)
    cost_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    item_code = models.CharField(max_length=50, default=0)
    sku = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    is_parse = models.IntegerField(default=0)
    is_difference = models.IntegerField(default=0)

    objects = BulkUpdateManager()

    def images_list(self):
        return json.loads(self.images)

    class Meta:
        managed = False
        db_table = 'difference_product'



