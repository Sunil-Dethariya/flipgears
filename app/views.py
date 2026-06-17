import random

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import RepairRequest, RegisterModel, CategoryModel, ProductModel, Cart, Ordermodel, Wishlist, Freequote, \
    CustomizationRequest, Feedback, OrderItem
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User

from django.shortcuts import render, redirect
from .models import User
import razorpay
from django.shortcuts import render, redirect
from .models import CustomizationRequest
from django.shortcuts import render
from .models import ProductModel, RegisterModel, Wishlist, CategoryModel
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import RegisterModel
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RepairRequest, Feedback



# Common_start



def profile(request):

    role = request.session.get("log_role")

    if role == "User":
        return render(request, "user/profile-page.html")

    elif role == "Seller":
        return render(request, "seller/profile-page.html")

    elif role == "Technician":
        return render(request, "technician/profile-page.html")

    return redirect("login")



def edit_profile(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])
    role = request.session.get("log_role")

    if request.method == "POST":

        user.Name = request.POST.get("name")
        user.Email = request.POST.get("email")
        user.Phone = request.POST.get("phone")

        # IMAGE
        if request.FILES.get("photo"):
            user.photo = request.FILES.get("photo")

        user.save()

        request.session["log_name"] = user.Name
        request.session["log_email"] = user.Email

        return redirect("profile")

    # 🔥 ROLE BASED TEMPLATE
    if role == "User":
        return render(request, "user/edit_profile.html", {"user": user})

    elif role == "Seller":
        return render(request, "seller/edit_profile.html", {"user": user})

    elif role == "Technician":
        return render(request, "technician/edit_profile.html", {"user": user})

    return redirect("login")


# Commonend




# Authentications_start




def register(request):
    return render(request,"auth/register.html")

def fetchregisterdata(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # 🔹 1. Username validation
        if not name or not name.strip():
            messages.error(request, "Username is required")
            return redirect("register")

        # 🔹 2. Email validation
        if not email or not email.strip():
            messages.error(request, "Email is required")
            return redirect("register")

        # 🔹 3. Phone validation
        if not phone or not phone.strip():
            messages.error(request, "Phone number is required")
            return redirect("register")

        # 🔹 4. Password validation
        if not password or len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect("register")

        # 🔹 5. Check UNIQUE Email
        if RegisterModel.objects.filter(Email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # 🔹 6. Check UNIQUE Phone
        if RegisterModel.objects.filter(Phone=phone).exists():
            messages.error(request, "Phone already registered!")
            return redirect("register")

        try:
            # 🔹 7. Save data
            RegisterModel.objects.create(
                Name=name,
                Email=email,
                Phone=phone,
                Password=password,
                Role=role
            )

            messages.success(request, "Registration successful!")
            return redirect("login")

        except IntegrityError:
            messages.error(request, "Something went wrong. Try again.")
            return redirect("register")

    return render(request, "auth/register.html")



def login_view(request):
    return render(request,"auth/login.html")

def fetchlogindata(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        fetchdata = RegisterModel.objects.get(Email=email, Password=password)

        request.session["log_id"] = fetchdata.id
        request.session["log_name"] = fetchdata.Name
        request.session["log_email"] = fetchdata.Email
        request.session["log_role"] = fetchdata.Role

    except:
        fetchdata = None

    if fetchdata is not None:

        # ✅ FIXED HERE
        if fetchdata.Role == "User":
            return redirect("/")

        elif fetchdata.Role == "Seller":
            return redirect("seller")

        elif fetchdata.Role == "Technician":
            return redirect("technician")

        else:
            return redirect("/")


    else:

        messages.error(request, "Invalid email or password")

        return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("/")




# Authentications_end


# Admin_start



def assign_technician(request):
    if request.method == "POST":
        repair_id = request.POST.get("repair_id")
        tech_id = request.POST.get("technician_id")

        repair = RepairRequest.objects.get(id=repair_id)
        repair.technician_id = tech_id
        repair.status = "Assigned"
        repair.save()

        return redirect("admin_request_list")

    return redirect("admin_request_list")


def admin_request_list(request):
    requests = RepairRequest.objects.filter(status="Pending")
    return render(request, "admin/request_list.html", {
        "requests": requests
    })

def admin_request_detail(request, id):
    repair = get_object_or_404(RepairRequest, id=id)

    # sirf technicians lao
    technicians = RegisterModel.objects.filter(Role="Technician")

    return render(request, "admin/request_list_details.html", {
        "repair": repair,
        "technicians": technicians
    })




# Admin_end


# User_start



def base(request):
    return render(request, "user/base.html")

def index(request):
    feedbacks = list(Feedback.objects.filter(
        repair_request__status="Completed"
    ).select_related("user", "repair_request"))

    random.shuffle(feedbacks)  # 🔥 shuffle

    return render(request, "user/index.html", {
        "feedbacks": feedbacks[:6]  # only 6 show
    })

def about(request):
    feedbacks = list(Feedback.objects.filter(
        repair_request__status="Completed"
    ).select_related("user", "repair_request"))

    random.shuffle(feedbacks)  # 🔥 shuffle

    return render(request, "user/about.html", {
        "feedbacks": feedbacks[:6]  # only 6 show
    })

def contact(request):
    return render(request, "user/contact.html")

def services(request):
    return render(request, "user/services.html")



def add_repair_request(request):
    if not request.session.get("log_id"):
        return redirect("login")

    if request.method == "POST":
        RepairRequest.objects.create(
            user_id=request.session["log_id"],
            full_name=request.POST.get("full_name"),
            mobile=request.POST.get("mobile"),
            email=request.POST.get("email"),
            gender=request.POST.get("gender"),
            device_name=request.POST.get("device_name"),
            brand=request.POST.get("brand"),
            model=request.POST.get("model"),
            issue_type=request.POST.get("issue_type"),
            issue_description=request.POST.get("issue_description"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
            latitude=request.POST.get("latitude"),
            longitude=request.POST.get("longitude"),
            payment_method="COD",
            service_charge=299
        )

        messages.success(request, "Your repair request has been submitted. Our technician will reach out shortly!")

        return redirect("view_repair_requests")

    return render(request, "user/add_request.html")


def view_repair_requests(request):
    if not request.session.get("log_id"):
        return redirect("login")

    requests = RepairRequest.objects.filter(
        user_id=request.session["log_id"]
    )

    feedbacks = list(Feedback.objects.filter(
        repair_request__status="Completed"
    ).select_related("user", "repair_request"))

    random.shuffle(feedbacks)  # 🔥 shuffle


    return render(request, "user/view_request.html", {"requests": requests,"feedbacks": feedbacks[:6]})


def customize(request):

    if request.method == "POST":

        product = request.POST.get("product")

        request.session["selected_product"] = product

        if product == "mobile":
            return render(request,"user/customize/customization_details.html")

        elif product == "laptop":
            return render(request,"user/customize/customization_details.html")

        # elif product == "headphone":
        #     return render(request,"user/customize/headphone.html")
        #
        # elif product == "gaming":
        #     return render(request,"user/customize/gaming.html")

    return render(request,"user/customize/cust_add_request.html")



def add_customizations_request(request):

    if not request.session.get("log_id"):
        return redirect("login")

    if request.method == "POST":

        CustomizationRequest.objects.create(
            user_id=request.session["log_id"],
            product_name = request.session.get("selected_product"),
            # 🔹 Personal
            full_name=request.POST.get("full_name"),
            mobile=request.POST.get("mobile"),
            email=request.POST.get("email"),
            gender=request.POST.get("gender"),

            # 🔹 Customization
            physical_cust=request.POST.get("physical_cust"),
            software_cust=request.POST.get("software_cust"),

            physical_other_cust=request.POST.get("physical_other_cust"),
            software_other_cust=request.POST.get("software_other_cust"),

            customization_description=request.POST.get("Customization description"),

            # 🔹 File
            cover_image=request.FILES.get("cover_image"),

            # 🔹 Address
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
            latitude=request.POST.get("latitude"),
            longitude=request.POST.get("longitude"),

            # 🔹 Payment
            payment_method="Cash on Delivery",
            service_charge=299
        )

        return redirect("view_cust_request")

    return render(request, "user/customize/customization_details.html")


def view_cust_request(request):
    if not request.session.get("log_id"):
        return redirect("login")

    requests = CustomizationRequest.objects.filter(
        user_id=request.session["log_id"]
    )

    feedbacks = list(Feedback.objects.filter(
        repair_request__status="Completed"
    ).select_related("user", "repair_request"))

    random.shuffle(feedbacks)  # 🔥 shuffle


    return render(request, "user/customize/cust_view_request.html", {"requests": requests,"feedbacks": feedbacks[:6]})


def cart(request):
    fetchdata = ProductModel.objects.all()
    context = {
        "data":fetchdata
    }
    return render(request, 'user/cart.html',context)



def products(request):

    # ✅ Base Query
    fetchdata = ProductModel.objects.filter(status="active")

    # =========================
    # 🔍 SEARCH
    # =========================
    search = request.GET.get("search")
    if search:
        fetchdata = fetchdata.filter(name__icontains=search)

    # =========================
    # 📂 CATEGORY FILTER
    # =========================
    category = request.GET.get("category")
    if category:
        fetchdata = fetchdata.filter(cat_id=category)

    # =========================
    # 💰 PRICE SORT
    # =========================
    price = request.GET.get("price")
    if price == "low":
        fetchdata = fetchdata.order_by("price")
    elif price == "high":
        fetchdata = fetchdata.order_by("-price")

    # =========================
    # ↕ SORTING
    # =========================
    sort = request.GET.get("sort")
    if sort == "latest":
        fetchdata = fetchdata.order_by("-id")
    elif sort == "popular":
        fetchdata = fetchdata.order_by("-views")  # optional field

    # =========================
    # ❤️ WISHLIST
    # =========================
    wishlist_ids = []

    if request.session.get("log_id"):
        user = RegisterModel.objects.get(id=request.session["log_id"])
        wishlist_ids = Wishlist.objects.filter(userid=user)\
                                       .values_list('productid_id', flat=True)

    # =========================
    # 📂 CATEGORY LIST (for dropdown)
    # =========================
    categories = CategoryModel.objects.all()

    # =========================
    # FINAL CONTEXT
    # =========================
    return render(request, "user/products_home.html", {
        "data": fetchdata,
        "wishlist_ids": wishlist_ids,
        "categories": categories
    })



def checkout(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    # 🔥 BUY NOW CASE
    if request.session.get("buy_now_product"):
        product_id = request.session["buy_now_product"]
        product = ProductModel.objects.get(id=product_id)

        cart_items = [{
            "productid": product,
            "quantity": 1,
            "total_amount": product.price
        }]

        grand_total = product.price

    else:
        # 🛒 NORMAL CART
        cart_items = Cart.objects.filter(userid=user, order_status=0)

        grand_total = 0
        for item in cart_items:
            grand_total += item.total_amount

    return render(request, 'user/checkout.html', {
        "cart_items": cart_items,
        "grand_total": grand_total
    })


def order_history(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    orders = Ordermodel.objects.filter(userid=user).order_by("-id")

    feedbacks = list(Feedback.objects.filter(
        repair_request__status="Completed"
    ).select_related("user", "repair_request"))

    random.shuffle(feedbacks)  # 🔥 shuffle

    return render(request, "user/order_history.html", {
        "orders": orders,
        "feedbacks": feedbacks[:6]
    })

def add_request(request):
    return render(request,"user/add_request.html")

def cust_add_request(request):
    return render(request,"user/customize/cust_view_request.html")


def single_page_product(request, id):
    product = ProductModel.objects.get(id=id)

    # 🔥 increase view count
    product.views += 1
    product.save()

    return render(request, "user/single_page_product.html", {
        "product": product
    })



def add_to_cart(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])
    product = ProductModel.objects.get(id=id)

    # check already exists in cart
    cart_item = Cart.objects.filter(
        userid=user,
        productid=product,
        order_status=0
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.total_amount = cart_item.quantity * product.price
        cart_item.save()
    else:
        Cart.objects.create(
            userid=user,
            productid=product,
            quantity=1,
            total_amount=product.price,
            order_status=0,
            orderid=0
        )

    return redirect("cart")


def cart(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    cart_items = Cart.objects.filter(userid=user, order_status=0)

    grand_total = 0
    for item in cart_items:
        grand_total += item.total_amount

    return render(request, "user/cart.html", {
        "cart_items": cart_items,
        "grand_total": grand_total
    })

def increase_qty(request, id):

    cart_item = Cart.objects.get(id=id)

    cart_item.quantity += 1
    cart_item.total_amount = cart_item.quantity * cart_item.productid.price
    cart_item.save()

    return redirect("cart")


def decrease_qty(request, id):

    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_amount = cart_item.quantity * cart_item.productid.price
        cart_item.save()
    else:
        cart_item.delete()   # remove if qty becomes 0

    return redirect("cart")

def remove_cart(request, id):

    cart_item = Cart.objects.get(id=id)
    cart_item.delete()

    return redirect("cart")


def placeorder(request):

    if not request.session.get("log_id"):
        return redirect("login")

    userid = request.session["log_id"]
    user = RegisterModel.objects.get(id=userid)

    phone = request.POST.get("phone")
    address = request.POST.get("address")
    payment = request.POST.get("payment_method")

    # ============================
    # 🔥 BUY NOW CASE
    # ============================
    if request.session.get("buy_now_product"):

        product_id = request.session["buy_now_product"]
        product = ProductModel.objects.get(id=product_id)

        grand_total = product.price

        # ✅ COD
        if payment == "COD":

            order = Ordermodel.objects.create(
                userid=user,
                final_total=grand_total,
                phone=phone,
                address=address,
                paymode="COD",
                orderstatus="Placed"
            )

            # 🔥 OrderItem create
            OrderItem.objects.create(
                order=order,
                product=product,
                seller=product.seller,
                quantity=1,
                price=product.price
            )

            del request.session["buy_now_product"]

            messages.success(request, "Order placed successfully")
            return redirect("order_history")

        # ✅ ONLINE
        else:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

            order_amount = int(float(grand_total) * 100)

            razorpay_order = client.order.create({
                "amount": order_amount,
                "currency": "INR",
                "receipt": f"order_rcptid_{userid}",
                "payment_capture": "1",
            })

            order = Ordermodel.objects.create(
                userid=user,
                final_total=grand_total,
                phone=phone,
                address=address,
                paymode="Online",
                orderstatus="Placed",
                razorpay_order_id=razorpay_order["id"]
            )

            # 🔥 OrderItem create
            OrderItem.objects.create(
                order=order,
                product=product,
                seller=product.seller,
                quantity=1,
                price=product.price
            )

            del request.session["buy_now_product"]

            return render(request, "user/payment.html", {
                "razorpay_order_id": razorpay_order["id"],
                "amount": order_amount,
                "key": settings.RAZORPAY_KEY_ID,
                "currency": "INR"
            })

    # ============================
    # 🛒 CART CASE
    # ============================
    cart_items = Cart.objects.filter(userid=user, order_status=0)

    grand_total = 0
    for item in cart_items:
        grand_total += item.total_amount

    # ✅ COD
    if payment == "COD":

        order = Ordermodel.objects.create(
            userid=user,
            final_total=grand_total,
            phone=phone,
            address=address,
            paymode="COD",
            orderstatus="Placed"
        )

        # 🔥 MULTI SELLER SUPPORT
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.productid,
                seller=item.productid.seller,
                quantity=item.quantity,
                price=item.total_amount
            )

        # 🔥 cart clear
        cart_items.delete()

        messages.success(request, "Order placed successfully")
        return redirect("order_history")

    # ✅ ONLINE
    else:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

        order_amount = int(float(grand_total) * 100)

        razorpay_order = client.order.create({
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{userid}",
            "payment_capture": "1",
        })

        order = Ordermodel.objects.create(
            userid=user,
            final_total=grand_total,
            phone=phone,
            address=address,
            paymode="Online",
            orderstatus="Placed",
            razorpay_order_id=razorpay_order["id"]
        )

        # 🔥 MULTI SELLER SUPPORT
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.productid,
                seller=item.productid.seller,
                quantity=item.quantity,
                price=item.total_amount
            )

        # 🔥 cart clear
        cart_items.delete()

        return render(request, "user/payment.html", {
            "razorpay_order_id": razorpay_order["id"],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR"
        })
def payment_success(request):
    return redirect("/")

def payment(request):
    return render(request,"user/payment.html")

def freequote(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        userid = None

        if request.session.get("log_id"):
            userid = RegisterModel.objects.get(id=request.session["log_id"])

        insertquery = Freequote(
            userid=userid,
            name=name,
            email=email,
            mobile=mobile,
            subject=subject,
            message=message
        )
        insertquery.save()

        messages.success(request, "Quote submitted successfully!")

    return render(request,"user/contact.html")



def add_to_wishlist(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])
    product = ProductModel.objects.get(id=id)

    existing = Wishlist.objects.filter(userid=user, productid=product).first()

    if existing:
        # ❌ already hai → remove karo
        existing.delete()
    else:
        # ✅ nahi hai → add karo
        Wishlist.objects.create(userid=user, productid=product)

    return redirect('products')
def wishlist_view(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    wishlist_items = Wishlist.objects.filter(userid=user).select_related('productid')

    return render(request, 'user/wishlist.html', {
        'wishlist_items': wishlist_items
    })

def remove_from_wishlist(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    item = Wishlist.objects.get(id=id)
    item.delete()

    return redirect("wishlist")

def buy_now(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    request.session["buy_now_product"] = id

    return redirect("checkout")

def give_feedback(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    # 🔥 FORCE PRODUCT (NULL nahi hoga)
    product = get_object_or_404(ProductModel, id=id)

    if request.method == "POST":

        rating = request.POST.get("rating")
        message = request.POST.get("message")

        Feedback.objects.create(
            user=user,
            product=product,   # ✅ FIXED
            order=None,
            repair_request=None,
            rating=rating,
            message=message
        )

        messages.success(request, "Feedback submitted successfully")

        return redirect("order_history")

    return render(request, "user/feedback.html", {
        "product": product
    })

def order_detail(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    order = Ordermodel.objects.get(id=id)

    return render(request, "user/order_detail.html", {
        "order": order
    })



def cancel_order(request, id):

    order = Ordermodel.objects.get(id=id)

    order.orderstatus = "Cancelled"
    order.save()

    return redirect("order_history")



from django.shortcuts import get_object_or_404

def give_repair_feedback(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    # 🔥 repair fetch
    repair = get_object_or_404(RepairRequest, id=id)

    if request.method == "POST":

        rating = request.POST.get("rating")
        message = request.POST.get("message")

        Feedback.objects.create(
            user=user,
            product=None,            # ❌ product nahi
            order=None,              # ❌ order nahi
            repair_request=repair,   # ✅ repair
            rating=rating,
            message=message
        )

        messages.success(request, "Feedback submitted successfully")

        return redirect("view_repair_requests")

    return render(request, "user/feedback.html", {
        "repair": repair
    })

# User_end
# Seller_start

def base_seller(request):
    return render(request, "seller/base.html")

def seller(request):
    return render(request, "seller/seller.html")

from django.shortcuts import render, redirect
from .models import ProductModel, CategoryModel

def add_product(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    if request.method == "POST":

        name = request.POST.get("name")
        catid = request.POST.get("catid")
        price = request.POST.get("price")
        desc = request.POST.get("desc")
        status = request.POST.get("status")
        img = request.FILES.get("img")

        category = CategoryModel.objects.get(id=catid)

        ProductModel.objects.create(
            seller=user,   # 🔥 IMPORTANT
            name=name,
            cat_id=category,
            img=img,
            price=price,
            desc=desc,
            status=status
        )

        return redirect("manage_product")

    data = CategoryModel.objects.all()
    return render(request, "seller/add_product.html", {"data": data})


def manage_product(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    fetchdata = ProductModel.objects.filter(seller=user)  # 🔥 FILTER

    return render(request, "seller/manage_product.html", {
        "data": fetchdata
    })


def manage_order(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    orders = Ordermodel.objects.filter(
        orderitem__seller=user
    ).distinct()

    return render(request,"seller/manage_order.html",{
        "orders":orders
    })

def update_order_status(request,id):

    order = Ordermodel.objects.get(id=id)

    if request.method == "POST":

        orderstatus = request.POST.get("status")

        order.orderstatus = orderstatus
        order.save()

    return redirect("manage_order")

def delete_product(request, id):
    product = ProductModel.objects.get(id=id)
    product.delete()
    return redirect("manage_product")

def edit_product(request, id):

    product = ProductModel.objects.get(id=id)
    categories = CategoryModel.objects.all()

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.desc = request.POST.get("desc")
        product.status = request.POST.get("status")

        catid = request.POST.get("catid")
        product.cat_id = CategoryModel.objects.get(id=catid)

        if request.FILES.get("img"):
            product.img = request.FILES.get("img")

        product.save()
        return redirect("manage_product")

    return render(request, "seller/edit_product.html", {
        "product": product,
        "categories": categories
    })

def view_feedback(request):

    if not request.session.get("log_id"):
        return redirect("login")

    user = RegisterModel.objects.get(id=request.session["log_id"])

    # 🔥 ONLY SELLER PRODUCTS FEEDBACK
    feedback = Feedback.objects.filter(product__seller=user)

    return render(request, "seller/view_feedback.html", {
        "feedback": feedback
    })


def delete_feedback(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    feedback = get_object_or_404(Feedback, id=id)

    # 🔥 SECURITY: sirf apne product ka delete kar sake
    if feedback.product and feedback.product.seller.id == request.session["log_id"]:
        feedback.delete()
        messages.success(request, "Feedback deleted successfully ")
    else:
        messages.error(request, "You are not allowed to delete this feedback ")

    return redirect("view_feedback")



def order_detail_seller(request,id):

    if not request.session.get("log_id"):
        return redirect("login")

    order = Ordermodel.objects.get(id=id)

    return render(request,"seller/order_detail.html",{
        "order": order
    })

# Seller_end


# Technician_start



def technician_dashboard(request):
    if not request.session.get("log_id"):
        return redirect("login")

    if request.session.get("log_role") != "Technician":
        return redirect("/")

    requests = RepairRequest.objects.filter(
        technician_id=request.session["log_id"],
        status="Assigned"
    )

    return render(request, "technician/request.html", {
        "requests": requests
    })


def technician_completed(request):
    if not request.session.get("log_id"):
        return redirect("login")

    # sirf technician allow
    if request.session.get("log_role") != "Technician":
        return redirect("login")

    completed = RepairRequest.objects.filter(
        technician_id=request.session["log_id"],
        status="Completed"
    )

    return render(request, "technician/completed.html", {
        "requests": completed,
        "active": "completed"
    })

def technician_request_detail(request, id):
    repair = get_object_or_404(RepairRequest, id=id)
    return render(request, "technician/request_detail.html", {"repair": repair})



def update_request_status(request, id):
    if not request.session.get("log_id"):
        return redirect("login")

    if request.session.get("log_role") != "Technician":
        return redirect("/")

    if request.method == "POST":
        repair = RepairRequest.objects.get(
            id=id,
            technician_id=request.session["log_id"]
        )

        repair.status = request.POST.get("status")
        repair.save()

        return redirect("technician_dashboard")

    return redirect("technician_dashboard")

def technician(request):
    return render(request,"technician/technician.html")




def technician_feedback_list(request):

    # Login check
    if not request.session.get("log_id"):
        return redirect("login")

    if request.session.get("log_role") != "Technician":
        return redirect("/")

    technician_id = request.session.get("log_id")

    # Sirf us technician ke feedback
    feedbacks = Feedback.objects.filter(
        repair_request__technician_id=technician_id
    ).select_related("user", "repair_request").order_by("-created_at")

    return render(request, "technician/view_feedback.html", {
        "feedbacks": feedbacks
    })


def delete_repair_feedback(request, id):

    if not request.session.get("log_id"):
        return redirect("login")

    if request.session.get("log_role") != "Technician":
        return redirect("/")

    feedback = get_object_or_404(Feedback, id=id)

    # 🔥 TECHNICIAN CHECK
    if feedback.repair_request and feedback.repair_request.technician_id == request.session["log_id"]:
        feedback.delete()
        messages.success(request, "Feedback deleted successfully ")
    else:
        messages.error(request, "You are not allowed to delete this feedback ")

    return redirect("technician_feedback_list")
    # Technician_end








from django.shortcuts import render, redirect
from .models import *

def admin_dashboard(request):
    return render(request, 'admin/admin.html', {
        'products': ProductModel.objects.all(),
        'users': RegisterModel.objects.all(),
        'orders': Ordermodel.objects.all(),
        'repairs': RepairRequest.objects.all(),
    })


def admin_add_product(request):
    if request.method == "POST":
        ProductModel.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            status=request.POST['status']
        )
    return redirect('admin_dashboard')


def admin_delete_product(request, id):
    ProductModel.objects.get(id=id).delete()
    return redirect('admin_dashboard')


def admin_edit_product(request, id):
    product = ProductModel.objects.get(id=id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.status = request.POST['status']
        product.save()
        return redirect('admin_dashboard')

    return render(request, 'admin/admin.html', {'product': product})