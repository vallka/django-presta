from django.db import models

# Create your models here.
class Ps17Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    id_supplier = models.PositiveIntegerField(blank=True, null=True)
    id_manufacturer = models.PositiveIntegerField(blank=True, null=True)
    id_category_default = models.PositiveIntegerField(blank=True, null=True)
    id_shop_default = models.PositiveIntegerField()
    id_tax_rules_group = models.PositiveIntegerField()
    on_sale = models.PositiveIntegerField()
    online_only = models.PositiveIntegerField()
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    isbn = models.CharField(max_length=32, blank=True, null=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    ecotax = models.DecimalField(max_digits=17, decimal_places=6)
    quantity = models.IntegerField()
    minimal_quantity = models.PositiveIntegerField()
    low_stock_threshold = models.IntegerField(blank=True, null=True)
    low_stock_alert = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=6)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6)
    unity = models.CharField(max_length=255, blank=True, null=True)
    unit_price_ratio = models.DecimalField(max_digits=20, decimal_places=6)
    additional_shipping_cost = models.DecimalField(max_digits=20, decimal_places=2)
    reference = models.CharField(max_length=64, blank=True, null=True)
    supplier_reference = models.CharField(max_length=32, blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=6)
    height = models.DecimalField(max_digits=20, decimal_places=6)
    depth = models.DecimalField(max_digits=20, decimal_places=6)
    weight = models.DecimalField(max_digits=20, decimal_places=6)
    out_of_stock = models.PositiveIntegerField()
    additional_delivery_times = models.PositiveIntegerField()
    quantity_discount = models.IntegerField(blank=True, null=True)
    customizable = models.IntegerField()
    uploadable_files = models.IntegerField()
    text_fields = models.IntegerField()
    active = models.PositiveIntegerField()
    redirect_type = models.CharField(max_length=12)
    id_type_redirected = models.PositiveIntegerField()
    available_for_order = models.IntegerField()
    available_date = models.DateField(blank=True, null=True)
    show_condition = models.IntegerField()
    condition = models.CharField(max_length=11)
    show_price = models.IntegerField()
    indexed = models.IntegerField()
    visibility = models.CharField(max_length=7)
    cache_is_pack = models.IntegerField()
    cache_has_attachments = models.IntegerField()
    is_virtual = models.IntegerField()
    cache_default_attribute = models.PositiveIntegerField(blank=True, null=True)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    advanced_stock_management = models.IntegerField()
    pack_stock_type = models.PositiveIntegerField()
    state = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ps17_product'




class Ps17ProductLang(models.Model):
    id_product = models.PositiveIntegerField(primary_key=True)
    id_shop = models.PositiveIntegerField()
    id_lang = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    description_short = models.TextField(blank=True, null=True)
    link_rewrite = models.CharField(max_length=128)
    meta_description = models.CharField(max_length=512, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_title = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=128)
    available_now = models.CharField(max_length=255, blank=True, null=True)
    available_later = models.CharField(max_length=255, blank=True, null=True)
    delivery_in_stock = models.CharField(max_length=255, blank=True, null=True)
    delivery_out_stock = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ps17_product_lang'
        unique_together = (('id_product', 'id_shop', 'id_lang'),)
