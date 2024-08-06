from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''


#para los calculos dentro del index en el carrusell de imagenes (asi se puede manejar n imagenes que el usuario ingrese)