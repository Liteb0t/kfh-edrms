from django import template
register = template.Library()


@register.filter
def list_item(lst, i): #define list item, allows you to loop through every doc to get doc table
    try:
        return lst[i]
    except:
        return None
