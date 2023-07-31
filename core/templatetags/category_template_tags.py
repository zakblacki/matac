from django import template
from django.utils.safestring import mark_safe

from core.models import Category , Item , OrderItem, Order

register = template.Library()




@register.simple_tag
def orders(user_ath):
    context={}
    if user_ath:
        total=0
        for order in OrderItem.objects.filter(user=user_ath,ordered=False):
            total += order.item.price * order.quantity
        context["total"] = total
        context["order"]= OrderItem.objects.filter(user=user_ath,ordered=False)
        return context
    else:
        return context
    


@register.simple_tag
def genders():
    
    
    unique_genders = set()
    uniq_categ=[]
    
    obj ={}
    items_li=""
    # Iterate over available items and add their genders to the set
    try:
        available_items = Item.objects.filter(is_active=True)
        for item in available_items:
            uniq_categ=[]
            unique_genders.add(item.get_gender_display())
            category = Item.objects.filter(gender=item.gender)
            for item in category:
                keyy=item.get_gender_display()
                uniq_categ.append(item.category.title)
                obj[keyy]=set(uniq_categ)
        
        items_li=""
        if unique_genders:
            for gender  in unique_genders :
                
                items_li += """<li><a href="">{}</a></li>""".format(gender)
        return mark_safe(items_li)
    except:
        return items_li
    
     
    
    

     
    


@register.simple_tag
def categories():
    items_li = ""
    try:
        items = Category.objects.filter(is_active=True).order_by('title')
    
        if items:
            for i in items:
                items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    except:
        pass   
    return mark_safe(items_li)

@register.simple_tag
def categories_mobile():
    items_li = ""
    try:
            
        items = Category.objects.filter(is_active=True).order_by('title')
        
        for i in items:
            items_li += """<li class="item-menu-mobile"><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    except:
        pass
    
    
    return mark_safe(items_li)


@register.simple_tag
def categories_li_a():
    items_li_a = ""
    try:
        
        items = Category.objects.filter(is_active=True).order_by('title')
        
        for i in items:
            items_li_a += """<li class="p-t-4"><a href="/category/{}" class="s-text13">{}</a></li>""".format(i.slug,i.title)
    except:
        pass
    return mark_safe(items_li_a)


@register.simple_tag
def categories_div():
    """
    section banner
    :return:
    """
    items_div = ""
    item_div_list = ""
    try:
        items = Category.objects.filter(is_active=True).order_by('title')
        
        for i, j in enumerate(items):
            if not i % 2:
                items_div += """<div class="block1 hov-img-zoom pos-relative m-b-30"><img src="/media/{}" alt="IMG-BENNER"><div class="block1-wrapbtn w-size2"><a href="/category/{}" class="flex-c-m size2 m-text2 bg3 hov1 trans-0-4">{}</a></div></div>""".format(
                    j.image, j.slug, j.title)
            else:
                items_div_ = """<div class="block1 hov-img-zoom pos-relative m-b-30"><img src="/media/{}" alt="IMG-BENNER"><div class="block1-wrapbtn w-size2"><a href="/category/{}" class="flex-c-m size2 m-text2 bg3 hov1 trans-0-4">{}</a></div></div>""".format(
                    j.image, j.slug, j.title)
                item_div_list += """<div class="col-sm-10 col-md-8 col-lg-4 m-l-r-auto">""" + items_div + items_div_ + """</div>"""
                items_div = ""
    except:
        pass
    return mark_safe(item_div_list)
