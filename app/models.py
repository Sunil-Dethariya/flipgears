from datetime import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.db import models




class CategoryModel(models.Model):
    catname = models.CharField(max_length=30)
    def __str__(self):
        return self.catname


# Authentications_start


class RegisterModel(models.Model):
    Name = models.CharField(max_length=30)
    Email = models.EmailField(unique=True)
    Phone = models.BigIntegerField(unique=True)
    Password = models.CharField(max_length=30)
    Role = models.CharField(max_length=10)

    photo = models.ImageField(upload_to="profile/", null=True, blank=True)

    def __str__(self):
        return self.Name



# Seller_start


class ProductModel(models.Model):
    seller = models.ForeignKey(RegisterModel, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=30)
    cat_id = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    img = models.ImageField(upload_to="media/seller")
    price = models.FloatField()
    desc = models.TextField()
    status = models.CharField(max_length=30)
    views = models.IntegerField(default=0,max_length=10)

    def admin_photo(self):
        if self.img:
            return mark_safe(f'<img src="{self.img.url}" width="100"/>')
        return "No Image"

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15,unique=True)
    photo = models.ImageField(upload_to="seller/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# User_start

class RepairRequest(models.Model):

    # User (login user)
    user_id = models.IntegerField()
    technician_id = models.IntegerField(null=True, blank=True)

    # Personal Details
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10)

    # Device Details
    device_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    issue_type = models.CharField(max_length=50)
    issue_description = models.TextField()

    # Address
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    # Payment
    payment_method = models.CharField(max_length=20, default="COD")
    service_charge = models.IntegerField(default=299,max_length=50)


    # Status
    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id} - {self.device_name}"


class CustomizationRequest(models.Model):

    # User (login user)
    user_id = models.IntegerField()
    technician_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, default="Customization")
    product_name = models.CharField(null=True, max_length=50, blank=True)

    # 🔹 STEP 1 - Personal
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    # 🔹 STEP 2 - Device / Customization
    PHYSICAL_CHOICES = [
        ("Phone Cover / Case", "Phone Cover / Case"),
        ("Screen Protection & Look", "Screen Protection & Look"),
        ("Stickers & Skins", "Stickers & Skins"),
        ("Accessories Add-ons", "Accessories Add-ons"),

        ("Laptop Skin / Cover", "Laptop Skin / Cover"),
        ("Screen Protection", "Screen Protection"),
        ("RGB Lighting", "RGB Lighting"),

        ("Accessories Add-ons", "Accessories Add-ons"),
        ("None", "None"),
        ("Other", "Other"),
    ]

    SOFTWARE_CHOICES = [
        ("Home Screen Design", "Home Screen Design"),
        ("Apps for Customization", "Apps for Customization"),

        ("UI Customization", "UI Customization"),
        ("Performance Optimization", "Performance Optimization"),
        ("Software Installation", "Software Installation"),


        ("None", "None"),
        ("Other", "Other"),
    ]

    physical_cust = models.CharField(max_length=50, choices=PHYSICAL_CHOICES, blank=True, null=True)
    software_cust = models.CharField(max_length=50, choices=SOFTWARE_CHOICES, blank=True, null=True)

    # File upload
    cover_image = models.ImageField(upload_to="customization/", blank=True, null=True)

    # Other fields
    physical_other_cust = models.CharField(max_length=200, blank=True, null=True)
    software_other_cust = models.CharField(max_length=200, blank=True, null=True)

    customization_description = models.TextField(blank=True, null=True)

    # 🔹 STEP 3 - Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    # 🔹 STEP 4 - Payment
    payment_method = models.CharField(max_length=50, default="Cash on Delivery")
    service_charge = models.IntegerField(default=299,max_length=50)

    # Status
    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Cart(models.Model):
    userid = models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    productid = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=10)
    total_amount = models.FloatField()
    order_status = models.IntegerField(max_length=10)
    orderid = models.IntegerField()



class Ordermodel(models.Model):

    STATUS = (
        ("Placed","Placed"),
        ("Packed","Packed"),
        ("Shipped","Shipped"),
        ("Delivered","Delivered"),
        ("Cancelled","Cancelled"),
    )

    userid = models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    final_total = models.FloatField()
    phone = models.BigIntegerField()
    address = models.TextField()
    paymode = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default = False)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    productid = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True, blank=True)
    orderstatus = models.CharField(max_length=20,choices=STATUS,default="Placed")

    def __str__(self):
        return self.orderstatus

class Wishlist(models.Model):
    userid = models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    productid = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




class Freequote(models.Model):
    userid = models.ForeignKey(RegisterModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    subject = models.TextField()
    message = models.TextField()


class Feedback(models.Model):
    user = models.ForeignKey(RegisterModel, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Ordermodel, on_delete=models.CASCADE, blank=True, null=True)
    repair_request = models.ForeignKey(RepairRequest, on_delete=models.CASCADE, null=True, blank=True)

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.repair_request:
            return f"Repair Feedback #{self.repair_request.id}"
        elif self.order:
            return f"Order Feedback #{self.order.id}"
        return "Feedback"



class OrderItem(models.Model):
    order = models.ForeignKey(Ordermodel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    seller = models.ForeignKey(RegisterModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=10)
    price = models.FloatField()
    status = models.CharField(max_length=20, default="Placed")
    def __str__(self):
        return self.product.name


# Technician_start


class TechnicianProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="technician_profile"
    )

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15,unique=True)
    photo = models.ImageField(upload_to="technicians/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name




