import shlex

from django import template

register = template.Library()


@register.filter
def htmlattributes(value, arg):
    """
        Adds html attributes to a form field.
        On your template:
            field|htmlattributes:'class="a class name" data-example="an example"'
    """
    attrs = value.field.widget.attrs
    attributes = shlex.split(str(arg))

    for attribute in attributes:
        attr = attribute.split('=')

        attr_name = attr[0]
        attr_value = '='.join(attr[1:])

        attrs[attr_name] = attr_value

    return unicode(value)
