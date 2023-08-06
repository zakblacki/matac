from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
   
    try:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            print("000000000")
            return qs[0].items.count()
        else:
            print("ddddddddd")
            return 0
    except:
        print("ggggggg")
        return 0
    
