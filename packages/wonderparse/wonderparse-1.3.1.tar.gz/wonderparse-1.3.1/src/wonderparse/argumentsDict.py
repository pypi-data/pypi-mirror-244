import inspect as _ins

from . import argumentDict as _argumentDict
from . import option_string as _option_string


def organized(value, /):
    optional = dict()
    non_optional = dict()
    value = dict(value)
    for dest, argumentDict in value.items():
        if _argumentDict.is_optional(argumentDict):
            optional[dest] = argumentDict
        else:
            non_optional[dest] = argumentDict
    ans = dict(**optional, **non_optional)
    return ans

def by_parameter(parameter, /, *, prefix_char=None):
    if parameter.name.startswith('_'):
        raise ValueError(parameter.name)
    annotation = parameter.annotation
    kind = parameter.kind
    if kind is _ins.Parameter.VAR_KEYWORD:
        if annotation is _ins.Parameter.empty:
            return dict()
        else:
            return organized(annotation)
    argumentDictA = _argumentDict.by_annotation(annotation)
    argumentDictB = dict()
    if kind in (_ins.Parameter.POSITIONAL_ONLY, _ins.Parameter.POSITIONAL_OR_KEYWORD):
        if parameter.default is not _ins.Parameter.empty:
            argumentDictB['nargs'] = '?'
            argumentDictB['default'] = parameter.default
    elif kind is _ins.Parameter.VAR_POSITIONAL:
        argumentDictB['nargs'] = '*'
        argumentDictB['default'] = tuple()
    elif kind is _ins.Parameter.KEYWORD_ONLY:
        if 'option_strings' not in argumentDictA.keys():
            option_string = _option_string.by_dest_metavar_and_prefix_char(
                dest=parameter.name,
                metavar=argumentDictA.get('metavar'),
                prefix_char=prefix_char,
            )
            argumentDictA['option_strings'] = [option_string]
        if parameter.default is _ins.Parameter.empty:
            argumentDictB['required'] = True
        else:
            argumentDictB['required'] = False
            argumentDictB['default'] = parameter.default
    else:
        raise ValueError
    argumentDict = dict(
        **argumentDictB, 
        **argumentDictA,
    )
    ans = {parameter.name:argumentDict}
    return ans

def by_func(value, /, prefix_char=None):
    ans = dict()
    signature = _ins.signature(value)
    for n, p in signature.parameters.items():
        part = by_parameter(p, prefix_char=prefix_char)
        ans = dict(**ans, **part)
    ans = organized(ans)
    return ans

def add_to_parser(value, /, parser):
    value = organized(value)
    for dest, argumentDict in value.items():
        _argumentDict.add_to_parser(
            argumentDict, 
            dest=dest,
            parser=parser, 
        )