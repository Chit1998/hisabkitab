from django.contrib import admin

from .models import *

# Register your models here.

class Users(admin.ModelAdmin):
    list_display= ('uid', 'name', 'email','provider', 'phone_number','status','date_joined','created_at')
admin.site.register(User, Users)

class OffersAdmin(admin.ModelAdmin):
    list_display= ('oid', 'name', 'status','category_id', 'last_date','created_at','updated_to')
admin.site.register(Offers, OffersAdmin)

class QtyTypeAdmin(admin.ModelAdmin):
    list_display= ('qid', 'name', 'value')
admin.site.register(QtyType, QtyTypeAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display= ('cid', 'name', 'status','created_at','updated_to')
admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display= ('scid', 'name', 'status','category_id','created_at','updated_to')
admin.site.register(SubCategory, SubCategoryAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display= ('nid', 'name', 'status','price','qty','total_qty_price','retail_price','sub_category_id','user_id','last_date','created_at','updated_to')
admin.site.register(Inventory, InventoryAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display= ('nid', 'title', 'sub_title','user_id','time','created_at','updated_to')
admin.site.register(Notification, NotificationAdmin)

class BorrowAdmin(admin.ModelAdmin):
    list_display= ('bid', 'title','qty','status','price','sub_category_id','user_id','qty_type_id','created_at','updated_to')
admin.site.register(Borrow, BorrowAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display= ('eid', 'title','price','status','sub_category_id','user_id','created_at','updated_to')
admin.site.register(Expense, ExpenseAdmin)
