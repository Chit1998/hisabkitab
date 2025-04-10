from django.db import models

# Create your models here.
import datetime
from django.db import models
from django.core.validators import MinLengthValidator


# iterable 
USER_TYPE = (
    ("1", "Customer"), 
    ("2", "Retailer"),
    ("3", "Vendor"),
    ("4", "Admin"),
)

PROVIDER = (
    ("1","SELF")
    ("2","GMAIL")
)

DEVICE_STATUS = (
    ("1","ANDROID"),
    ("2","WEB"),
    ("3","IOS"),
)

class User(models.Model):
    uid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='uid')
    name = models.CharField (max_length = 45)
    provider = models.CharField (max_length = 45, default="SELF")
    user_type = models.CharField (max_length = 45, default="")
    shop_name = models.CharField (max_length = 100, default="", null= True, blank= True)
    email = models.EmailField (max_length = 50,unique = True)
    pwd = models.CharField (max_length=15, validators=[MinLengthValidator(6)],default="")
    phone_number = models.CharField (max_length = 20, validators=[MinLengthValidator(8)], null= True, blank= True)
    fcm_token = models.TextField(max_length = 300, null = True, blank= True, default="")
    device_token = models.CharField(max_length = 100, default= "", null= True, blank= True)
    sign_in_token = models.CharField (max_length = 40, default="", null= True, blank= True)
    status = models.BooleanField (default = True) # account active or inactive user
    device_status = models.CharField (max_length = 45, default="") # user device status
    date_joined = models.DateTimeField(default= datetime.datetime.now)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('User')
        verbose_name_plural = "User"

class Category(models.Model):
    cid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='cid')
    name = models.CharField (max_length = 45)
    image = models.ImageField(upload_to ='category', blank=True, null = True, default="")
    status = models.BooleanField (default = True)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('category')
        verbose_name_plural = "Category"

class SubCategory(models.Model):
    scid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='scid')
    name = models.CharField (max_length = 45)
    brand_name = models.CharField(max_length = 200, default = "", blank = True, null = True)
    description = models.CharField(max_length = 200, default = "", blank = True, null = True)
    status = models.BooleanField (default = True)
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = ('sub_category')
        verbose_name_plural = "Sub_Category"

class QtyType(models.Model):
    qid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='qid')
    name = models.CharField (max_length = 45)
    value = models.CharField(max_length = 45)

    class Meta:
        db_table = ('qty_type')
        verbose_name_plural = "Qty_Type"

class Offers(models.Model):
    oid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='oid')
    name = models.CharField (max_length = 45)
    image = models.ImageField(upload_to ='offer', blank=True)
    status = models.BooleanField (default = True)
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    last_date = models.DateTimeField(default = datetime.datetime.now)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('offers')
        verbose_name_plural = "Offers"

class Inventory(models.Model):
    nid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='nid')
    name = models.CharField (max_length = 100)
    status = models.BooleanField (default = True)
    price = models.DecimalField(decimal_places = 2,max_digits= 10)
    qty = models.IntegerField(default=0)
    total_qty_price = models.DecimalField(decimal_places = 2, max_digits= 10)
    retail_price = models.DecimalField(decimal_places = 2, max_digits= 10)
    sub_category_id = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    qty_type_id = models.ForeignKey(QtyType, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    last_date = models.DateTimeField(default = datetime.datetime.now)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('inventory')
        verbose_name_plural = "Inventory"

class Notification(models.Model):
    nid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='nid')
    title = models.CharField (max_length = 100)
    sub_title = models.CharField (max_length = 300)
    image = models.ImageField(upload_to ='notifications/', blank=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(default = datetime.datetime.now)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('notification')
        verbose_name_plural = "Notification"

class Borrow(models.Model):
    bid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='bid')
    title = models.CharField (max_length = 45)
    qty = models.CharField(max_length = 45)
    status = models.BooleanField (default = True)
    price = models.DecimalField(decimal_places = 2, max_digits= 10)
    sub_category_id = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    qty_type_id = models.ForeignKey(QtyType, on_delete = models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('borrow')
        verbose_name_plural = "Borrow"

class Expense(models.Model):
    eid = models.BigAutoField(auto_created=True, primary_key = True, serialize = False, verbose_name ='eid')
    title = models.CharField (max_length = 45)
    price = models.DecimalField(decimal_places = 2, max_digits= 10)
    status = models.BooleanField (default = True)
    sub_category_id = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default= datetime.datetime.now)
    updated_to = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ('expense')
        verbose_name_plural = "Expense"
