from django import template
from django.utils.safestring import mark_safe
from django.utils import translation
from core.models import Slide

register = template.Library()


@register.simple_tag
def slides():
    items_div = ""
    try:
        
        
        items = Slide.objects.filter(is_active=True).order_by('pk')
        
        for i in items:
            if translation.get_language() == 'en':
                items_div += """<div class="item-slick1 item2-slick1" style="background-image: url(/media/{});"><div class="wrap-content-slide1 sizefull flex-col-c-m p-l-15 p-r-15 p-t-150 p-b-170">
                <span style="font-family: 'Roboto Condensed-bold', sans-serif !important;" class="caption1-slide1 m-text1 t-center animated visible-false m-b-15" data-appear="rollIn">{}</span>
                <h2 style="font-family: 'Roboto Condensed-bold', sans-serif !important;" class="caption2-slide1 xl-text1 t-center animated visible-false m-b-37" data-appear="lightSpeedIn">{}</h2><div class="wrap-btn-slide1 w-size1 animated visible-false" data-appear="slideInUp"><a href="{}" class="flex-c-m size2 bo-rad-23 s-text2 bgwhite hov1 trans-0-4">Shop Now</a></div></div></div>""".format(i.image, i.caption1_en, i.caption2_en, i.link)
            if translation.get_language() == 'ar':
                items_div += """<div class="item-slick1 item2-slick1" style="background-image: url(/media/{});"><div class="wrap-content-slide1 sizefull flex-col-c-m p-l-15 p-r-15 p-t-150 p-b-170">
                <span style="font-family: 'Roboto Condensed-bold', sans-serif !important;" class="caption1-slide1 m-text1 t-center animated visible-false m-b-15" data-appear="rollIn">{}</span>
                <h2 style="font-family: 'Roboto Condensed-bold', sans-serif !important;" class="caption2-slide1 xl-text1 t-center animated visible-false m-b-37" data-appear="lightSpeedIn">{}</h2><div class="wrap-btn-slide1 w-size1 animated visible-false" data-appear="slideInUp"><a href="{}" class="flex-c-m size2 bo-rad-23 s-text2 bgwhite hov1 trans-0-4">Shop Now</a></div></div></div>""".format(i.image, i.caption1_ar, i.caption2_ar, i.link)
            
            else:
                items_div += """<div class="item-slick1 item2-slick1" data-img="/media/{}" data-imgphone="/media/{}" style="background-image: url(/media/{});"><div class="wrap-content-slide1 sizefull flex-col-c-m p-l-15 p-r-15 p-t-150 p-b-170">
                <span style="font-family: 'Roboto Condensed-bold', sans-serif !important;" class="caption1-slide1 m-text1 t-center animated visible-false m-b-15" data-appear="rollIn">{}</span>
                <h2 style="font-family: 'Roboto Condensed-bold', sans-serif !important;" class="caption2-slide1 xl-text1 t-center animated visible-false m-b-37" data-appear="lightSpeedIn">{}</h2><div class="wrap-btn-slide1 w-size1 animated visible-false" data-appear="slideInUp"><a href="{}" class="flex-c-m size2 bo-rad-23 s-text2 bgwhite hov1 trans-0-4">Shop Now</a></div></div></div>""".format(i.image,i.image_mob,i.image, i.caption1, i.caption2, i.link)
                
    except:
        pass
    return mark_safe(items_div)


