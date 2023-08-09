from django import template
from core.models import Item
register = template.Library()
import json

@register.filter
def filtered_and_length(value, delimiter):
    
    returned_val=len(Item.objects.filter(article_id=value))
    # Split the string using the given delimiter and return its length
    return returned_val


@register.filter
def parse_json(value):
    return json.loads(value)

@register.filter
def total_withship(value1 , value2 ):
     
    return value1  + float(value2)