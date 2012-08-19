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

from django.template import Library, Node, TemplateSyntaxError
from ..models import user_promise_state, PromiseUserState


register = Library()


@register.tag
def userpromise(parser, token):
    """
    Abstracts whether a visiting user is the creator of a promise, supporter or a promise, or neither.
    """
    try:
        tag, promise = token.contents.split()
    except (ValueError, TypeError):
        # Catches both cases: no arguments, too many arguments
        raise TemplateSyntaxError("'%s' tag requires one argument" % tag)

    default_states = ['owner', 'supporter', 'nothing']
    states = {}

    # Parse until we find one of our default_status items
    parser.parse(default_states)

    # Let's iterate over our context and find our tokens
    token = parser.next_token()
    while token.contents != 'enduserpromise':
        # Let's parse things until our next state token
        current = token.contents
        states[current] = parser.parse(default_states + ['enduserpromise'])
        token = parser.next_token()

    var = parser.compile_filter(promise)
    return UserPromiseNode(var, states)


class UserPromiseNode(Node):
    def __init__(self, var, states):
        self.var = var
        self.states = states

    def render(self, context):
        promise = self.var.resolve(context, True)
        rendered = []

        state = user_promise_state(context['user'], promise)
        for key, val in self.states.items():
            if PromiseUserState.from_string(key) == state:
                return val.render(context)
