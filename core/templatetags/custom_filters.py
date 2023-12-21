from django import template
from core.models import Item, Matacor_info
register = template.Library()
import json
import re
from django.utils.safestring import mark_safe

@register.simple_tag
def contact_fo():
    returned_val=Matacor_info.objects.first()
    
    items_li=""
    if returned_val.contact_footer:
        items_li = """ {} """.format(returned_val.contact_footer)
         
            
            
         
    return mark_safe(items_li )
 
     


@register.filter
def filtered_and_length(value, delimiter):
    
    returned_val=len(Item.objects.filter(article_id=value))
    
    # Split the string using the given delimiter and return its length
    return returned_val

@register.filter
def extract_numbers(value):
    return re.sub(r'\D', '', value)

@register.filter
def parse_json(value):
    return json.loads(value)

@register.filter
def total_withship(value1 , value2 ):
     
    return value1  + float(value2)

@register.filter(name='replace')
def replace(value1,value2,value3):
     
    return value1.replace(value2,value3)