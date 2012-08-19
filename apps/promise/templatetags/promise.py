from django.template import Library, Node, TemplateSyntaxError
from ..models import user_promise_state, PromiseUserState


register = Library()


@register.tag
def userpromise(parser, token):
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
