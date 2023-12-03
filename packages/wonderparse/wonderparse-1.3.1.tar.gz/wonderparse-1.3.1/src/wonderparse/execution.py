import inspect as _ins
import typing as _typing


def by_object(value, /, *, funcInput):
    func = by_holder if hasattr(value, "_dest") else by_func
    return func(value, funcInput=funcInput)

def by_holder(value, /, *, funcInput):
    funcInput = funcInput.copy()
    cmd = funcInput.pop(0)
    value = getattr(value, cmd)
    return by_object(
        value, 
        funcInput=funcInput,
    )

def by_func(value, /, *, funcInput):
    ans = funcInput.exec(value)
    sig = _ins.signature(value)
    outtype = sig.return_annotation
    if outtype in [_ins.Parameter.empty, _typing.Any]:
        return ans
    if outtype is not None:
        return outtype(ans)
    if ans is None:
        return None
    raise ValueError(f"""\
The function {value.__name__} returned {ans}, \
but it's return annotation is None.""")

