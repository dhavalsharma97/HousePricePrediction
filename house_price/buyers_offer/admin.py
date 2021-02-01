from django.contrib import admin
from .models import Payment, PropertyAddress, Buyer

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_type', 'down_payment')
    list_filter = ['payment_type']

@admin.register(PropertyAddress)
class PropertyAddressAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'street', 'city', 'county')
    list_filter = ['city', 'county']
    fields = [('apartment', 'street'), ('city', 'county')]

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'offer_price')
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Property Details', {
            'fields': ('offer_price', 'property_address', 'payment')
        })
    )