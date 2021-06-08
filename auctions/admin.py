from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, List, Bid, Comment, WahchList


class ListAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'title','category', 'start_bid', 'description', 'img_url', 'date', 'user_id')

class BidAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'bid', 'item_id')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'item_id', 'created_on')
    search_fields = ('name', 'body')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WahchList)