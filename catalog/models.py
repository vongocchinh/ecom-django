# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# from django.shortcuts import reverse
from django_countries.fields import CountryField

from django.db import models
# from django_countries.fields import CountryField
from django.shortcuts import reverse
from django.contrib.auth.models import User




LABEL_CHOICES={
    ('S',"Secondary"),
    ('P','Primary'),
    ('D','Danger'),
    ('B','Black'),
    ('W','White'),
    ('P','Pink')
}


STATUS_CHOICES={
    ('N',"NEW"),
    ('O','OLD')
}


class Brand(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(
        default='default.jpg', upload_to='static/cat_imgs')

    class Meta:
        verbose_name_plural = 'Brand'

    def __str__(self):
        return self.name


class Item(models.Model):
    title=models.CharField(max_length=200)
    price=models.IntegerField()
    discount_price=models.IntegerField(blank=True, null=True)
    slug=models.SlugField()
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, blank=True, null=True)
    label=models.CharField(choices=LABEL_CHOICES,max_length=2)
    description=models.TextField()
    status=models.CharField(choices=STATUS_CHOICES,max_length=20)
    image=models.ImageField(default='default.jpg',upload_to='static/images')
    def __str__(self):
        return self.title
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug})
    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'slug': self.slug})
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug': self.slug})
    def get_item_price(self):
        return self.price

    def get_item_final_price(self):
        if self.discount_price:
            return (self.price - ((self.discount_price/100) * self.price )) 
        else:
            return self.get_item_price()


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
            return (self.item.price - ((self.item.discount_price/100) * self.item.price )) * self.quantity
        else:
            return self.get_item_price()



class Order(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    items = models.ManyToManyField(OrderItem)
    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_final_price()
        return total
    def get_quantity(self):
        count = 0
        for order_item in self.items.all():
            count+=order_item.quantity
        return count



class Bills(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    address = models.CharField('address', max_length=50, blank=True)
    name = models.CharField('name', max_length=50, blank=True)
    phone = models.CharField('phone', max_length=50, blank=True)
    email = models.CharField('email', max_length=50, blank=True)
    country = CountryField('country',blank_label='(Select country)')
    zip = models.CharField('zipcode',max_length=5,blank=True)
    checkout_date=models.DateTimeField('date published')
    total=models.IntegerField(default=0)
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)

class BillsDetail(models.Model):
    user= models.ForeignKey(User,  on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    def __str__(self):
         return "Id bill : " +str(self.bill.id)+"  ----------------------  "+str(self.item.title)+"  -----------------------số lương san phẩm : "+str(self.quantity)