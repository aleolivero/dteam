from django import template

register = template.Library()

@register.simple_tag
def get_attr(obj, attr_name):
    # Usa la función getattr de Python para obtener el valor del atributo y devuelve el resultado
    return getattr(obj, attr_name, None)

@register.filter
def items(value):
    return {k: v for k, v in value.__dict__.items() if not k.startswith('_')}.items()

@register.simple_tag
def define(val=None):
  return val

@register.filter
def url(attr):
    try:
        _url = attr.url
    except:
        _url = '/media/players/default/default.png'

    return _url

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)