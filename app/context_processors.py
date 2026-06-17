from .models import Cart, RegisterModel

def cart_count(request):

    count = 0

    if request.session.get("log_id"):
        user = RegisterModel.objects.get(id=request.session["log_id"])
        count = Cart.objects.filter(userid=user, order_status=0).count()

    return {"cart_count": count}