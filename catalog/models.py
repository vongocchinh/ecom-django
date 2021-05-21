# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# from django.shortcuts import reverse
from django_countries.fields import CountryField

from django.db import models
# from django_countries.fields import CountryField
from django.shortcuts import reverse
from django.contrib.auth.models import User

CATEGORY_CHOICES={
    ('S',"Shirt"),
    ('SW','SportWear'),
    ('Ow','OutWear')
}

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


LABEL_CHOICES={
    ('S',"secondary"),
    ('P','primary'),
    ('D','danger')
}

class Category(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(
        default='default.jpg', upload_to='static/cat_imgs')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Item(models.Model):
    title=models.CharField(max_length=200)
    price=models.IntegerField()
    discount_price=models.IntegerField(blank=True, null=True)
    slug=models.SlugField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    label=models.CharField(choices=LABEL_CHOICES,max_length=2)
    description=models.TextField()
    status=models.CharField(max_length=20)
    image=models.ImageField(default='default.jpg',upload_to='static/images')
    def __str__(self):
        return self.title
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug})
    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'slug': self.slug})
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug': self.slug})


class ProductReview(models.Model):
    message=models.CharField(max_length=10000)
    email=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    ratting=models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    review_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title} "
    def get_amount_saved(self):
        return self.get_item_price() - self.get_item_final_price()

    def get_item_discount_price(self):
        return self.item.discount_price * self.quantity

    def get_item_price(self):
        return self.item.price * self.quantity

    def get_item_final_price(self):
        if self.item.discount_price:
            return self.get_item_discount_price()
        else:
            return self.get_item_price()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=250)
    apartment_address = models.CharField(max_length=300, blank=True, null=True)
    country = CountryField(blank_label='(Select country)')
    zip = models.CharField(max_length=5)
    default = models.BooleanField(default=False)
    save_info = models.BooleanField(default=False)
    use_default = models.BooleanField()
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=1)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,blank=True,null=True)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    items = models.ManyToManyField(OrderItem)
    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total




