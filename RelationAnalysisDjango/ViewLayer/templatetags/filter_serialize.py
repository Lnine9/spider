from django import template

register = template.Library()


@register.filter(name='listToStr')
def list_to_str(value: list, conn=' '):
    return conn.join(value)
