from django.contrib import admin

# Register your models here.

from auctions.models import User, Listing, Comment, Bid

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'email', 'phone_number', 'address', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'owner__username')
    list_filter = ('is_active', 'category')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'created_at', 'content')
    search_fields = ('listing__title', 'user__username')
    list_filter = ('created_at',)

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'amount', 'created_at')
    search_fields = ('listing__title', 'user__username')
    list_filter = ('created_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)