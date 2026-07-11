from django import template

register = template.Library()


@register.filter
def get_attr(objeto, atributo):
    valor = getattr(objeto, atributo, '')
    if callable(valor):
        return valor()
    return valor
