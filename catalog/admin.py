from django.contrib import admin



from .models import Item, Order, OrderItem,Address,Category,ProductReview

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=[
        'title',
        'price',
        'discount_price'
    ]

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'street_address',
                    'apartment_address',
                    'default',
                    'country']

class CategoryAdmin(admin.ModelAdmin):
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

admin.site.register(Item,ItemAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
