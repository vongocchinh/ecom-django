from django.contrib import admin



from .models import Item, Order, OrderItem,Brand,ProductReview,Bills,BillsDetail

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=[
        'title',
        'id',
        'price',
        'discount_price'
    ]

# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['user',
#                     'street_address',
#                     'name',
#                     'phone',
#                     'email']
class BillsAdmin(admin.ModelAdmin):
    list_display=['id','name','phone','checkout_date']

class BrandAdmin(admin.ModelAdmin):
    # prepopulated_fields={'slug':('name',)}
    list_display=[
        'name'
    ]
class ProductReviewAdmin(admin.ModelAdmin):
    # prepopulated_fields={'slug':('title',)}
    list_display=[
            'item',
            'name',
            'review_date',
            'ratting',
            'email',
        ]


class BillDetailAdmin(admin.ModelAdmin):
    list_display=[
        'id','user','bill','quantity','total'
    ]
admin.site.register(Item,ItemAdmin)
# admin.site.register(Address,AddressAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Brand,BrandAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Bills,BillsAdmin)


admin.site.register(BillsDetail)