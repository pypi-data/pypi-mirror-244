import dataclasses as _dataclasses

import wonderparse.execution as _execution
import wonderparse.parser as _parser
import wonderparse.process_namespace as _process_namespace


@_dataclasses.dataclass
class Outfiler:
    dest:str='outfile'
    option_strings:tuple=('-o', '--outfile')
    open_outfile:callable
    help:str | None
    required:bool=False
    default
    @property
    def optional(self):
        return bool(len(self.option_strings))
    def to_argumentDict(self):
        ans = dict()
        ans['dest'] = self.dest
        ans['option_strings'] = self.option_strings
        ans['help'] = self.help
        if self.optional:



def simple_run(*, 
    args, 
    program_object,
    endgame='print',
    **kwargs,
):
    endgame = _endgame(endgame)
    parser = _parser.by_object(program_object, **kwargs)
    ns = parser.parse_args(args)
    funcInput = _process_namespace.by_object(
        program_object, 
        namespace=ns,
    )
    if len(vars(ns)):
        raise ValueError(f"Some arguments in the namespace were not processed: {ns}")
    try:
        result = _execution.by_object(program_object, funcInput=funcInput)
    except Exception as exc:
        msg = _exit_msg(
            prog=kwargs.get('prog'),
            exc=exc,
        )
        raise SystemExit(msg)
    return endgame(result)

def outfile_run(*, 
    args, 
    program_object,
    outfiler,
    **kwargs,
):
    parser = _parser.by_object(program_object, outfiler=outfiler, **kwargs)
    ns = parser.parse_args(args)
    funcInput = _process_namespace.by_object(
        program_object, 
        namespace=ns, 
        outfile_dest=outfiler.dest,
    )
    if len(vars(ns)):
        raise ValueError(f"Some arguments in the namespace were not processed: {ns}")
    outfile = funcInput.pop(outfiler.dest)
    result = _execution_by_object(program_object, funcInput=funcInput)
    with outfiler.open_outfile(outfile) as outstream:
        outstream.write(result)

def _execution_by_object(value, /, *, funcInput):
    try:
        return _execution.by_object(value, funcInput=funcInput)
    except Exception as exc:
        msg = _exit_msg(
            prog=kwargs.get('prog'),
            exc=exc,
        )
        raise SystemExit(msg)


def _exit_msg(
    *,
    prog,
    exc,
):
    if prog is None:
        msgA = f"{type(exc)}"
    else:
        msgA = f"Running {prog} failed because of {type(exc)}"
    msg = f"{msgA}: {exc}"
    return msg

def _endgame(value):
    if type(value) is not str:
        return value
    if value == 'print':
        return print
    if value == 'iterprint':
        return iterprint
    if value == 'return':
        return _return
    raise ValueError(f"{value.__repr__()} is not a legal value for endgame.")
    
def iterprint(values):
    for value in values:
        print(value)

def _return(value):
    return value

