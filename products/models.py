from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.


class Industry(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Industry, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    regular_price = models.PositiveIntegerField()
    stoc = models.PositiveIntegerField(default=10)
    out_of_stoc = models.BooleanField(default=False)
    discounted_parcent = models.PositiveIntegerField()
    description = RichTextField(max_length=2000)
    modle = models.CharField(max_length=50)
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    tag = models.CharField(max_length=50, help_text="enter your tag coma separated")
    details_description = RichTextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def discounted_price(self):
        price = (
            self.regular_price - (self.regular_price * self.discounted_parcent) / 100
        )
        # format(price, ".2f")
        return price

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.CharField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class ProductAditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=70)
    details = models.CharField(max_length=150)

    def __str__(self):
        return self.product.title


class CuponCodeGenaration(models.Model):
    name = models.CharField(max_length=50)
    cupon_code = models.CharField(max_length=50)
    discoun_parcent = models.PositiveIntegerField()
    up_to = models.PositiveIntegerField(help_text="Limit of Discount Amaount")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cupon_applaied = models.BooleanField(default=False)
    cupon_code = models.ForeignKey(
        CuponCodeGenaration,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    last_updated = models.DateTimeField(auto_now_add=True)

    @property
    def total_product_price(self):
        price = self.product.discounted_price * self.quantity
        # price = f"{price:.2f}"
        return price

    @classmethod
    def subtotal_product_price(cls, user):
        carts = Cart.objects.filter(user=user)
        subtotal_price = 0.00
        if carts:
            subtotal_price = sum(cart.total_product_price for cart in carts)
        if carts:
            cart_item = carts[0]
            if cart_item.cupon_applaied:
                subtotal_price = subtotal_price - (
                    cart_item.cupon_code.discoun_parcent * subtotal_price / 100
                )

        return subtotal_price

    def __str__(self):
        return self.product.title


class CustomerAddress(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    zip_code = models.PositiveIntegerField()
    street_address = models.CharField(max_length=250)
    mobile = models.PositiveIntegerField()
    is_billing = models.BooleanField(default=True)
    is_shipping = models.BooleanField(default=True)

    def __str__(self):
        # return f"{self.state}"
        return f"{self.user.first_name} - {self.street_address}, {self.city}, {self.state}, {self.zip_code}"


class PlacedOder(models.Model):
    STATUS = [
        ("Oder Recived", "Oder Recived"),
        ("Oder Packed", "Oder Packed"),
        ("Oder OnTheWay", "Oder OnTheWay"),
        ("Oder Shipped", "Oder Shipped"),
    ]
    # order_number = models.BigAutoField()
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.DO_NOTHING, related_name='shipping_address')
    sub_total_price = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default="Oder Recived")
    paid = models.BooleanField(default=False)
    placed_date = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=12, blank=True, null=True)
    sample = models.OneToOneField(CustomerAddress, on_delete=models.CASCADE, default=None, blank=True, null=True)

    @property
    def oder_id(self):
        return f'OID{str(self.id).zfill(6)}'
    
    def save(self, *args, **kwargs):
        self.order_number = self.oder_id
        super(PlacedOder, self).save(*args, **kwargs)
    
    @classmethod
    def placed_oders_by_user(cls, user):
        oders = PlacedOder.objects.filter(user=user)
        placed_oder_items_dict = {}

        for oder in oders:
            placed_oder_list = []

            placed_oder_details = {}
            placed_oder_details['sub_total_price'] = oder.sub_total_price
            placed_oder_details['status'] = oder.status
            placed_oder_details['placed_date'] = oder.placed_date
            placed_oder_details['paid'] = oder.paid
            placed_oder_list.append(placed_oder_details)

            oder_items = PlacedeOderItem.objects.filter(placed_oder=oder)

            for item in oder_items:
                oder_items_list = []
                print(item.product.title)
                image = item.product.productimage_set.first().image
                title = item.product.title
                quantity = item.quantity
                total_price = item.total_price
                oder_items_list.append(image)
                oder_items_list.append(title)
                oder_items_list.append(quantity)
                oder_items_list.append(total_price)
                placed_oder_list.append(oder_items_list)

            placed_oder_items_dict[oder.oder_id] = placed_oder_list
        return placed_oder_items_dict
        # return 'fg'

    
    def __str__(self):
        return self.order_number
    

class PlacedeOderItem(models.Model):
    placed_oder = models.ForeignKey(PlacedOder, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.placed_oder.user.first_name}--{str(self.placed_oder.id)}--{str(self.placed_oder.placed_date)}"

class CompletedOder(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    sub_total_price = models.FloatField()
    status = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    complete_date = models.DateTimeField(auto_now_add=True)
    oder_number = models.CharField(max_length=12)

    def __str__(self):
        return self.oder_number
    
class CompletedOderItems(models.Model):
    completed_oder = models.ForeignKey(CompletedOder, on_delete=models.CASCADE, related_name='delivered_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return self.product.title[:20] + str(self.product.id)


