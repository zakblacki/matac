from django import template
from django.utils.safestring import mark_safe

from core.models import Category , Item , OrderItem, Order, TopCategory,GenderCategory

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
def gendercat():
    try:
        items = GenderCategory.objects.all()
    except:
        items=[]
    return  items
    
    
    
@register.simple_tag
def categories():
    
    context={} 
    items_li = ""
    items =GenderCategory.objects.all()
    
        
        
    for indx,i in enumerate(items):
        
        if indx ==0:
            
            items_li+="""<ul id="{}" class="menu" style="padding: 10px;">""".format(i.title)
        else:
            items_li+="""<ul id="{}" class="menu" style="padding: 10px;display:none">""".format(i.title)

        if i.categories.all():
            for itml in i.categories.all():    
                # items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
                items_li += """ <li class="submenu">
                            <a class="subcat-name" href="{}" role="button">{}</a>
                            <ul class="megamenu" aria-labelledby="navbarDropdown" >
                                <div class="row " style="visibility: visible;">
                                    <div class="col-lg-3">
                                        <ul class="two-column">""".format(itml.slug, itml.title)
                for itm in itml.items.all():
                        
                    items_li += """<li class="mega-sub-cat">
                                <a href="/category/{}">{}</a>
                            </li>""".format( itm.slug,itm.title)
                        

                items_li +="""</ul>
                                </div>
                                </div>
                            </ul>
                        </li>"""
        
        else:   
            items_li += """<li><a href="{}">{}</a></li>""".format(i.slug, i.title)
    
        items_li +="""<div class="header-search hs-simple">
							<form action="/shop/" class="input-wrapper">
								<input type="text" class="form-control" name="search" autocomplete="off" placeholder="&nbsp; &nbsp; &nbsp; &nbsp; Rechercher par mot clés..." required="">
								<button class="btn btn-search" type="submit">
									<i class="d-icon-search"></i>
								</button>
							</form>
						</div>
					</ul>"""
    
    context["items"]=mark_safe(items_li )
    context["header"]="dd"
    return context

@register.simple_tag
def categories_mobile():
    items_li = ""
    items =GenderCategory.objects.all()
    
        
    for indx,itt in enumerate(items) :    
        for i in itt.categories.all():
        
                
            if i.items.all():
                    
                # items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
                items_li += """ <li id='{}1' class="removblelist" >
                            <a id="menu_tel"  >{}
                                <img style="height: 15px;
                                position: absolute;
                                top: 15px;
                                opacity:0.8;
                                right: 5px;" src="/static/images/chev.png" alt="">
                        </a>
                            <ul>""".format(itt.title,i.title)
                for itm in i.items.all():
                        
                    items_li += """<li style="padding:10px;">
                                    <a href="/category/{}"> 	
                                    <img sty class="icon-category" src="{}" alt="Category" loading="lazy">
                                        {}
                                    </a>
                                </li>""".format( itm.slug,itm.image.url,itm.title)
                        

                items_li +="""</ul>
                        </li>"""
            
            else:   
                items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    
    return mark_safe(items_li )





@register.simple_tag
def categories_mobile1():
    items_li = ""
    items =GenderCategory.objects.all()
    
        
        
    for i in items:
       items_li += """
        <li class="nav-item" style="width: 100px;">
                            <a data-id="{}1" class="nav-link nav-link-phone"   style="text-decoration: none;">{}</a>
                        </li>
       """.format(i.title,i.title)
            
        
        
         
    return mark_safe(items_li )




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
