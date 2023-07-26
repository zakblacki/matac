from django import template
from core.models import Item
register = template.Library()

@register.filter
def filtered_and_length(value, delimiter):
    
    returned_val=len(Item.objects.filter(article_id=value))
    # Split the string using the given delimiter and return its length
    return returned_val