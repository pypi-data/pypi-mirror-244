import inspect as _ins

_LEGAL_ACTIONS = [
    'store', 
    'store_const', 
    'append', 
    'append_const', 
    'help', 
    'version',
]

def is_optional(value, /):
    value = dict(value)
    option_strings = value.get('option_strings', [])
    option_strings = list(option_strings)
    return bool(len(option_strings))

def by_annotation(annotation):
    if annotation is _ins.Parameter.empty:
        return {}
    if callable(annotation):
        return {'type': annotation}
    if type(annotation) is str:
        return {'help': annotation}  
    return dict(annotation)

def add_to_parser(value, /, parser, *, dest):
    aa_kwargs = dict(value)
    action = aa_kwargs.get('action', 'store')
    if action not in _LEGAL_ACTIONS:
        raise ValueError
    option_strings = aa_kwargs.pop('option_strings', [])
    parser.add_argument(
        *option_strings, 
        dest=dest, 
        **aa_kwargs
    )