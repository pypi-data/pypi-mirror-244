import argparse as _ap
import inspect as _ins

from . import argumentsDict as _argumentsDict


def _get_prefix_char(parser):
    prefix_chars = parser.prefix_chars
    try:
        return prefix_chars[0]
    except IndexError:
        return None

def by_object(value, /, **kwargs):
    func = by_holder if hasattr(value, "_dest") else by_func
    return func(value, **kwargs)

def by_holder(obj, /, **kwargs):
    parents_kwargs = dict(kwargs)
    ans = _ap.ArgumentParser(
        description=obj.__doc__,
        **kwargs,
    )
    subparsers = ans.add_subparsers(dest=obj._dest, required=True)
    for n, m in _ins.getmembers(obj):
        if n.startswith("_"):
            continue
        cmd = n
        prefix_char = _get_prefix_char(ans)
        if prefix_char is not None:
            cmd = cmd.replace('_', prefix_char)
        parents_kwargs['prog'] = cmd
        parent = by_object(
            m,
            prog=cmd,
            **parents_kwargs,
        )
        subparser = subparsers.add_parser(
            cmd,
            parents=[parent],
            add_help=False,
            prog=parent.prog,
            description=parent.description,
        )
    return ans

def by_func(
    value, 
    /, 
    *,
    outfiler=None,
    **kwargs,
):
    ans = _ap.ArgumentParser(
        description=value.__doc__,
        **kwargs,
    )
    prefix_char = _get_prefix_char(ans)
    argumentsDict = _argumentsDict.by_func(
        value, 
        prefix_char=prefix_char,
    )
    _argumentsDict.add_to_parser(
        argumentsDict,
        parser=ans,
    )
    if outfiler is None:
        return ans
    return_annotation = _ins.signature(value).return_annotation
    if return_annotation is None:
        return ans
    ans.add_argument(
        *outfiler.option_strings,
        default=outfiler.default,
        dest=outfiler.dest,
        help=outfiler.help,
        required=outfiler.required,
    )
    return ans

def by_parameter(value, /, **kwargs):
    ans = _ap.ArgumentParser(
        **kwargs,
    )
    prefix_char = _get_prefix_char(ans)
    argumentsDict = _argumentsDict.by_parameter(
        value, 
        prefix_char=prefix_char,
    )
    _argumentsDict.add_to_parser(
        argumentsDict,
        parser=ans,
    )
    return ans

def by_argumentsDict(value, /, **kwargs):
    ans = _ap.ArgumentParser(**kwargs)
    _argumentsDict.add_to_parser(
        value, 
        parser=ans,
    )
    return ans
