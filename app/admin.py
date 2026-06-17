from django.contrib import admin
from .models import TechnicianProfile, RegisterModel
from .models import RepairRequest
from .models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id","full_name","device_name",
        "mobile","status","created_at"
        )

class RegisterModelAdmin(admin.ModelAdmin):
    list_display = ["Name","Email","Phone","Password","Role"]

admin.site.register(RegisterModel,RegisterModelAdmin)

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["catname"]

admin.site.register(CategoryModel,CategoryModelAdmin)

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["name","cat_id","admin_photo","price","desc","status"]

admin.site.register(ProductModel,ProductModelAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ["userid","productid","quantity","total_amount","order_status","orderid"]

admin.site.register(Cart,CartAdmin)

def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['userid', 'final_total', 'paymode','timestamp']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.userid, obj.final_total, obj.paymode,obj.timestamp])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"

class OrderAdmin(admin.ModelAdmin):
    list_display = ["userid","final_total","phone","address","paymode","timestamp","status","orderstatus","razorpay_order_id"]
    list_filter = ["timestamp"]
    actions = [export_to_pdf]
admin.site.register(Ordermodel,OrderAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ["userid","productid","created_at"]

admin.site.register(Wishlist,WishlistAdmin)



from django.contrib import admin



class FreequoteAdmin(admin.ModelAdmin):
    list_display = ["userid","name","email","mobile","subject","message"]

admin.site.register(Freequote,FreequoteAdmin)

from django.contrib import admin
from .models import CustomizationRequest

class CustomizationRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_id",
        "type",
        "product_name",
        "full_name",
        "mobile",
        "physical_cust",
        "software_cust",
        "status",
        "created_at"
    ]

    list_filter = ["status", "physical_cust", "software_cust","product_name"]

    search_fields = ["full_name", "mobile", "email"]

    list_editable = ["status"]  # admin me direct status change

admin.site.register(CustomizationRequest, CustomizationRequestAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["user","repair_request","product","order","rating","message","created_at"]

admin.site.register(Feedback, FeedbackAdmin)
