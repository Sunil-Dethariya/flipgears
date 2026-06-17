"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

from pro import settings
urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    path("dashboard/repair-requests/", views.admin_request_list, name="admin_request_list"),
    path("dashboard/repair-request/<int:id>/", views.admin_request_detail, name="admin_request_detail"),
    path("dashboard/assign-technician/", views.assign_technician, name="assign_technician"),

    #auth
    path('register/',views.register, name='register'),
    path('fetchregisterdata/',views.fetchregisterdata, name='fetchregisterdata'),
    path('login/',views.login_view, name='login'),
    path('fetchlogindata/', views.fetchlogindata, name='fetchlogindata'),
    path('logout/', views.logout_view, name='logout'),


    #user
    path('', views.index, name="index"),
    path('add-request/', views.add_request, name='add_request'),
    path('repair/view/', views.view_repair_requests, name='view_repair_requests'),
    path("add-repair-request/", views.add_repair_request, name="add_repair_request"),
    path('cust_add/', views.customize, name='cust_add'),
    path('cust-add-request/', views.cust_add_request, name='cust_add_request'),
    path('cust/view/', views.view_cust_request, name='view_cust_request'),
    path('add-cust-request/',views.add_customizations_request, name="add_customizations_request"),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.index, name='toggle-wishlist'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('base/', views.base, name='base'),
    path("about/", views.about, name='about'),
    path("products/",views.products, name='products'),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("increase-qty/<int:id>/", views.increase_qty, name="increase_qty"),
    path("decrease-qty/<int:id>/", views.decrease_qty, name="decrease_qty"),
    path("remove-cart/<int:id>/", views.remove_cart, name="remove_cart"),
    path("placeorder/", views.placeorder, name="placeorder"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("payment/", views.payment, name="payment"),
    path('single-page-product/<int:id>/',views.single_page_product, name="single_page_product"),
    path("freequote/",views.freequote,name="freequote"),
    path("profile/",views.profile,name="profile"),
    path("edit-profile/",views.edit_profile,name="edit_profile"),
    path('add-wishlist/<int:id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_wishlist'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    path("checkout/", views.checkout, name="checkout"),
    path("order-history/", views.order_history, name="order_history"),
    path("order-detail/<int:id>/", views.order_detail, name="order_detail"),
    path("cancel-order/<int:id>/", views.cancel_order, name="cancel_order"),
    path('feedback/<int:id>/', views.give_feedback, name='feedback_page'),
    path('repair-feedback/<int:id>/', views.give_repair_feedback, name='give_repair_feedback'),


    #seller
    path("seller/", views.seller, name='seller'),
    path("base_seller",views.base_seller, name='base_seller'),
    path("add_product/", views.add_product, name='add_product'),
    path("manage_product/", views.manage_product, name='manage_product'),
    path("manage_order/", views.manage_order, name='manage_order'),
    path("view_feedback/", views.view_feedback, name='view_feedback'),
    path("edit-product/<int:id>/", views.edit_product, name="edit_product"),
    path("delete-product/<int:id>/", views.delete_product, name="delete_product"),
    path("manage-order/",views.manage_order,name="manage_order"),
    path("update-order-status/<int:id>/",views.update_order_status,name="update_order_status"),
    path("give_feedback/<int:id>", views.give_feedback, name="give_feedback"),
    path('delete-feedback/<int:id>/', views.delete_feedback, name='delete_feedback'),
    path("seller-order-detail/<int:id>/", views.order_detail_seller, name="order_detail_seller"),



    #Technician
    path("technician/",views.technician,name="technician"),
    path("technician/dashboard/", views.technician_dashboard, name="technician_dashboard"),
    path("technician/request/<int:id>/", views.technician_request_detail, name="technician_request_detail"),
    path("technician/update-status/<int:id>/", views.update_request_status, name="update_request_status"),
    path("technician/completed/", views.technician_completed, name="technician_completed"),
    path('technician/feedback/', views.technician_feedback_list, name='technician_feedback_list'),
    path('delete-repair-feedback/<int:id>/', views.delete_repair_feedback, name='delete_repair_feedback'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('add-product/', views.admin_add_product, name='add_product'),

    path('delete-product/<int:id>/', views.admin_delete_product, name='delete_product'),

    path('admin-edit-product/<int:id>/', views.admin_edit_product, name='edit_product'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)