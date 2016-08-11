import reg
from functools import wraps
from . import generic


class delegate(object):

    name_map = dict(
        permits='permits',
    )

    def __init__(self, *predicates):
        self.predicates = predicates

    def __call__(self, func):
        generic_name = self.name_map[func.__name__]

        if not hasattr(generic, generic_name):
            setattr(generic, generic_name,
                    reg.dispatch(*self.predicates)(func))

        @wraps(func)
        def delegator(self, *args, **kw):
            return getattr(generic, generic_name)(
                self, lookup=self.lookup, *args, **kw)

        return delegator


def fix_signature(func):
    args = reg.arginfo(func)
    if args.args and args.args[0] == 'app':
        return func

    signature = ', '.join(
        args.args +
        (['*' + args.varargs] if args.varargs else []) +
        (['**' + args.keywords] if args.keywords else []))

    code_template = """\
def wrapper(app, {signature}):
    return _func({signature})
"""

    code_source = code_template.format(signature=signature)
    namespace = {'_func': func}
    exec(code_source, namespace)
    return namespace['wrapper']
