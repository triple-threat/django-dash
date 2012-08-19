# Promise.ly -- social commitment platform
#
# Copyright (C) 2012  Promise.ly authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
