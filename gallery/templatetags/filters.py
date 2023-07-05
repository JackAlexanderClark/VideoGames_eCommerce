from django import template

register = template.Library()

# define functions to split strings
# call functions within templates

@register.filter
def split(value):
    return value.split(4)

@register.filter
def myfunc(value):
    return value[1]

@register.filter
def price(value):
    return value[2]
@register.filter
def quantity(value):
    return value[3]

@register.filter
def total(value):
    return int(value[2])*int(value[3])

@register.filter
def processed(value):
    if value[-1]=='False':
        return 0
    else:
        return 1

@register.filter
def total_price(value):
    total=0
    for item in value:
        total+=int(item[2])*int(item[3])
    return total

@register.filter
def total_quantity(value):
    total=0
    for item in value:
        total+=int(item[3])
    return total